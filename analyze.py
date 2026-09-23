"""Run Stockfish over your chess.com games and build the Sensei report.

Reads   data/games/*.json          (from fetch_games.py)
Caches  data/analysis.jsonl        (one line per engine-analyzed game; never redone)
Writes  reports/latest.md          (human-readable report)
        reports/summary.json       (the numbers, for the Claude project to read)
        reports/puzzles.csv        (your own missed moves, as a drill deck)
        reports/history/DATE.md    (dated copy of each report)

Environment knobs (all optional except CHESS_USERNAME):
  CHESS_USERNAME   your chess.com username
  MAX_GAMES        games to engine-analyze per run, newest first (default 200)
  ENGINE_DEPTH     Stockfish search depth per position (default 12)
  TIME_CLASSES     comma list to include, e.g. "blitz,rapid" (default: all)
  STOCKFISH_PATH   engine binary (default: found on PATH or /usr/games/stockfish)
"""
import csv
import datetime as dt
import glob
import io
import json
import math
import os
import shutil
import statistics
import sys
from collections import defaultdict

import chess
import chess.engine
import chess.pgn

USER = os.environ.get("CHESS_USERNAME", "").strip().lower()
MAX_GAMES = int(os.environ.get("MAX_GAMES", "200"))
DEPTH = int(os.environ.get("ENGINE_DEPTH", "12"))
TIME_CLASSES = {t.strip() for t in os.environ.get("TIME_CLASSES", "").split(",") if t.strip()}
CACHE = os.path.join("data", "analysis.jsonl")

# ---- thresholds (ASSUMPTIONS, not measurements; they are echoed in every report) ----
INACCURACY, MISTAKE, BLUNDER = 10, 20, 30     # drop in win-chance points (lichess convention)
SHARP_GAP = 15      # position is "sharp" if best move beats 2nd-best by >= this many win-chance points
WINNING = 80        # "winning position" = engine win chance >= 80% for you
LOSING = 20         # "lost position"    = engine win chance <= 20% for you
PRESSURE_FRAC = 0.10  # "time pressure"  = clock below 10% of starting time before the move
OPENING_MOVES = 12  # opening phase = first 12 full moves (unless already an endgame)
ENDGAME_MATERIAL = 13  # endgame = total non-pawn material of both sides <= 13 (Q9 R5 B3 N3)
BACK_TO_BACK_MIN = 15  # tilt check: next game started within 15 min of the last one ending
MIN_N = 10          # below this many observations a rate is printed as "short"

DRAW_CODES = {"agreed", "repetition", "stalemate", "insufficient", "50move", "timevsinsufficient"}
VALUES = {chess.QUEEN: 9, chess.ROOK: 5, chess.BISHOP: 3, chess.KNIGHT: 3}


# ------------------------------------------------------------------ helpers
def win_pct(cp):
    cp = max(-1000, min(1000, cp))
    return 50 + 50 * (2 / (1 + math.exp(-0.00368208 * cp)) - 1)


def move_accuracy(loss):
    return max(0.0, min(100.0, 103.1668 * math.exp(-0.04354 * loss) - 3.1669))


def result_for(side_result):
    if side_result == "win":
        return 1.0
    if side_result in DRAW_CODES:
        return 0.5
    return 0.0


def parse_tc(tc):
    """'180+2' -> (180, 2); '600' -> (600, 0); daily '1/86400' -> (None, None)."""
    if not tc or "/" in tc:
        return None, None
    base, _, inc = tc.partition("+")
    try:
        return int(base), int(inc or 0)
    except ValueError:
        return None, None


def opening_names(eco_url):
    if not eco_url:
        return "Unknown", "Unknown"
    slug = eco_url.rstrip("/").split("/")[-1]
    words = []
    for w in slug.split("-"):
        if w[:1].isdigit() or w.startswith("..."):
            break
        words.append(w)
    full = " ".join(words) or slug
    family = []
    for w in words:
        family.append(w)
        if w in ("Opening", "Defense", "Game", "Gambit", "Attack", "System"):
            break
    return full, " ".join(family[:4]) or full


def non_pawn_material(board):
    return sum(VALUES[p] * len(board.pieces(p, c)) for p in VALUES for c in (chess.WHITE, chess.BLACK))


def phase(board):
    if non_pawn_material(board) <= ENDGAME_MATERIAL:
        return "endgame"
    if board.fullmove_number <= OPENING_MOVES:
        return "opening"
    return "middlegame"


def is_imbalanced(board):
    """Different piece types on each side while total piece value is close
    (e.g. rook vs bishop+pawns, queen vs two rooks). Simply being a piece up is not counted."""
    counts = {}
    for c in (chess.WHITE, chess.BLACK):
        counts[c] = (len(board.pieces(chess.QUEEN, c)), len(board.pieces(chess.ROOK, c)),
                     len(board.pieces(chess.BISHOP, c)) + len(board.pieces(chess.KNIGHT, c)))
    w, b = counts[chess.WHITE], counts[chess.BLACK]
    if w == b:
        return False
    wv = w[0] * 9 + w[1] * 5 + w[2] * 3
    bv = b[0] * 9 + b[1] * 5 + b[2] * 3
    return abs(wv - bv) <= 2


def start_ts(headers):
    try:
        return dt.datetime.strptime(f"{headers['UTCDate']} {headers['UTCTime']}", "%Y.%m.%d %H:%M:%S").replace(
            tzinfo=dt.timezone.utc).timestamp()
    except (KeyError, ValueError):
        return None


def rate(num, den):
    return None if den == 0 else round(100 * num / den, 1)


def fmt_rate(num, den, unit="%"):
    if den < MIN_N:
        return f"short (n={den})"
    return f"{100 * num / den:.1f}{unit} (n={den})"


# ------------------------------------------------------------------ loading
def load_games():
    games, months = [], sorted(glob.glob(os.path.join("data", "games", "*.json")))
    if not months:
        sys.exit("FAILED: no data/games/*.json files. Run fetch_games.py first.")
    for path in months:
        for g in json.load(open(path)):
            if g.get("rules") != "chess" or not g.get("pgn"):
                continue
            w, b = g["white"]["username"].lower(), g["black"]["username"].lower()
            if USER not in (w, b):
                continue
            if TIME_CLASSES and g.get("time_class") not in TIME_CLASSES:
                continue
            games.append(g)
    seen, out = set(), []
    for g in sorted(games, key=lambda g: g.get("end_time", 0)):
        if g["url"] in seen:
            continue
        seen.add(g["url"])
        out.append(g)
    return out


def load_cache():
    done = {}
    if os.path.exists(CACHE):
        for line in open(CACHE):
            line = line.strip()
            if line:
                rec = json.loads(line)
                done[rec["url"]] = rec
    return done


# ------------------------------------------------------------------ engine pass
def evaluate(engine, board):
    """Win chance for the side to move, plus best/second-best info."""
    if board.is_checkmate():
        return {"wp": 0.0, "best": None, "second": None}
    if board.is_stalemate() or board.is_insufficient_material():
        return {"wp": 50.0, "best": None, "second": None}
    infos = engine.analyse(board, chess.engine.Limit(depth=DEPTH), multipv=2)
    turn = board.turn
    scores = [win_pct(i["score"].pov(turn).score(mate_score=10000)) for i in infos]
    best = infos[0].get("pv", [None])[0]
    return {"wp": scores[0], "best": best, "second": scores[1] if len(scores) > 1 else None}


def analyze_game(engine, g):
    user_white = g["white"]["username"].lower() == USER
    color = chess.WHITE if user_white else chess.BLACK
    me, opp = (g["white"], g["black"]) if user_white else (g["black"], g["white"])
    game = chess.pgn.read_game(io.StringIO(g["pgn"]))
    if game is None or game.errors:
        return {"url": g["url"], "error": "pgn_parse_failed"}
    base, inc = parse_tc(g.get("time_control"))

    boards, nodes = [game.board()], list(game.mainline())
    for n in nodes:
        b = boards[-1].copy(stack=False)
        b.push(n.move)
        boards.append(b)
    if "checkmated" in (me.get("result"), opp.get("result")) and not boards[-1].is_checkmate():
        return {"url": g["url"], "error": "pgn_inconsistent_with_result"}
    evals = [evaluate(engine, b) for b in boards]

    side = {s: {"moves": 0, "inacc": 0, "mist": 0, "blund": 0, "acc": [],
                "sharp_moves": 0, "sharp_errors": 0, "pressure_moves": 0, "pressure_errors": 0,
                "calm_errors": 0, "calm_moves": 0,
                "phase": {p: [0, 0] for p in ("opening", "middlegame", "endgame")}}
            for s in ("me", "opp")}
    spent_sharp, spent_calm = [], []
    puzzles, missed_punish, sharp_positions, counted_positions = [], 0, 0, 0
    castled, imbalanced_plies = {}, 0
    clocks = {chess.WHITE: base, chess.BLACK: base}
    my_wp_curve = []
    prev_opp_blunder = False

    for i, node in enumerate(nodes):
        b, move = boards[i], node.move
        mover = b.turn
        who = "me" if mover == color else "opp"
        e0, e1 = evals[i], evals[i + 1]
        wp_before = e0["wp"]
        wp_after = 100 - e1["wp"]
        loss = max(0.0, wp_before - wp_after)
        sharp = e0["second"] is not None and (e0["wp"] - e0["second"]) >= SHARP_GAP
        if b.fullmove_number > 8:
            counted_positions += 1
            sharp_positions += sharp

        s = side[who]
        s["moves"] += 1
        s["acc"].append(move_accuracy(loss))
        err = loss >= MISTAKE
        if loss >= BLUNDER:
            s["blund"] += 1
        elif loss >= MISTAKE:
            s["mist"] += 1
        elif loss >= INACCURACY:
            s["inacc"] += 1
        ph = phase(b)
        s["phase"][ph][0] += 1
        s["phase"][ph][1] += err
        if sharp:
            s["sharp_moves"] += 1
            s["sharp_errors"] += err

        # clock (not for daily games)
        clk = node.clock()
        if base is not None and clk is not None and clocks[mover] is not None:
            before = clocks[mover]
            spent = max(0.0, before - clk + inc)
            if before < PRESSURE_FRAC * base:
                s["pressure_moves"] += 1
                s["pressure_errors"] += err
            else:
                s["calm_moves"] += 1
                s["calm_errors"] += err
            if who == "me":
                (spent_sharp if sharp else spent_calm).append(spent)
            clocks[mover] = clk

        if who == "me":
            if prev_opp_blunder and err:
                missed_punish += 1
            if loss >= MISTAKE and e0["best"] is not None:
                puzzles.append({"fen": b.fen(), "move_no": b.fullmove_number,
                                "side": "white" if mover else "black",
                                "played": b.san(move), "best": b.san(e0["best"]),
                                "loss": round(loss, 1), "sharp": sharp, "phase": ph})
        prev_opp_blunder = who == "opp" and loss >= BLUNDER

        if b.is_castling(move):
            castled[mover] = "K" if b.is_kingside_castling(move) else "Q"
        if i >= 20 and is_imbalanced(boards[i + 1]):
            imbalanced_plies += 1

    for i, e in enumerate(evals):
        my_wp_curve.append(e["wp"] if boards[i].turn == color else 100 - e["wp"])

    eco_url = g.get("eco") or game.headers.get("ECOUrl", "")
    opening, family = opening_names(eco_url)
    for s in side.values():
        s["acc"] = round(statistics.fmean(s["acc"]), 1) if s["acc"] else None

    return {
        "url": g["url"], "end_time": g.get("end_time"), "time_class": g.get("time_class"),
        "time_control": g.get("time_control"), "rated": g.get("rated"),
        "color": "white" if user_white else "black", "my_rating": me.get("rating"),
        "opp_rating": opp.get("rating"), "result": result_for(me.get("result")),
        "my_result_code": me.get("result"), "opp_result_code": opp.get("result"),
        "opening": opening, "family": family, "plies": len(nodes), "depth": DEPTH,
        "me": side["me"], "opp": side["opp"],
        "chaos_index": round(sharp_positions / counted_positions, 3) if counted_positions else None,
        "max_wp": round(max(my_wp_curve[10:] or my_wp_curve), 1),
        "min_wp": round(min(my_wp_curve[10:] or my_wp_curve), 1),
        "opposite_castling": len(castled) == 2 and castled[chess.WHITE] != castled[chess.BLACK],
        "imbalanced": imbalanced_plies >= 6,
        "missed_punish": missed_punish,
        "spent_sharp": round(statistics.fmean(spent_sharp), 2) if spent_sharp else None,
        "spent_calm": round(statistics.fmean(spent_calm), 2) if spent_calm else None,
        "n_spent_sharp": len(spent_sharp), "n_spent_calm": len(spent_calm),
        "puzzles": puzzles,
    }


def find_engine():
    for p in (os.environ.get("STOCKFISH_PATH"), shutil.which("stockfish"), "/usr/games/stockfish"):
        if p and os.path.exists(p):
            return p
    sys.exit("FAILED: Stockfish not found. Install it (apt-get install stockfish) or set STOCKFISH_PATH.")


def run_engine(games, cache):
    todo = [g for g in reversed(games) if g["url"] not in cache][:MAX_GAMES]
    if not todo:
        print("engine: nothing new to analyze")
        return 0
    engine = chess.engine.SimpleEngine.popen_uci(find_engine())
    engine.configure({"Threads": max(1, (os.cpu_count() or 2)), "Hash": 256})
    os.makedirs("data", exist_ok=True)
    done = 0
    try:
        with open(CACHE, "a") as f:
            for n, g in enumerate(todo, 1):
                rec = analyze_game(engine, g)
                cache[rec["url"]] = rec
                f.write(json.dumps(rec) + "\n")
                f.flush()
                done += 1
                if n % 10 == 0:
                    print(f"engine: {n}/{len(todo)} games")
    finally:
        engine.quit()
    return done


# ------------------------------------------------------------------ aggregation
def record_line(results):
    w = sum(r == 1 for r in results)
    d = sum(r == 0.5 for r in results)
    l = sum(r == 0 for r in results)
    return w, d, l


def score_pct(results):
    return None if not results else round(100 * statistics.fmean(results), 1)


def fmt_score(results):
    if len(results) < MIN_N:
        return f"short (n={len(results)})"
    w, d, l = record_line(results)
    return f"{100 * statistics.fmean(results):.1f}% (n={len(results)}; +{w} ={d} -{l})"


def aggregate(games, cache):
    all_recs = [cache[g["url"]] for g in games if g["url"] in cache]
    failed = [r for r in all_recs if "error" in r]
    recs = [r for r in all_recs if "error" not in r and r["plies"] >= 10]
    S = {"generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes"),
         "username": USER, "engine_depth": DEPTH,
         "time_classes_included": sorted(TIME_CLASSES) or "all",
         "assumptions": {"inaccuracy_mistake_blunder_winchance_drop": [INACCURACY, MISTAKE, BLUNDER],
                         "sharp_gap": SHARP_GAP, "winning_threshold": WINNING, "losing_threshold": LOSING,
                         "time_pressure_fraction": PRESSURE_FRAC, "opening_full_moves": OPENING_MOVES,
                         "endgame_material": ENDGAME_MATERIAL, "back_to_back_minutes": BACK_TO_BACK_MIN,
                         "min_sample": MIN_N,
                         "note": "Thresholds are conventions chosen for this report, not measured facts. "
                                 "Engine evals at this depth are approximate. 'Accuracy' here uses the "
                                 "lichess per-move formula averaged; it is NOT chess.com's CAPS number."}}

    # ---- overview from all games (no engine needed)
    by_tc = defaultdict(list)
    for g in games:
        me = g["white"] if g["white"]["username"].lower() == USER else g["black"]
        by_tc[g.get("time_class")].append((g.get("end_time", 0), result_for(me.get("result")), me.get("rating")))
    S["overview"] = {
        "games_on_disk": len(games), "games_engine_analyzed": len(recs),
        "games_failed_parse": len(failed), "games_too_short_skipped": len(all_recs) - len(recs) - len(failed),
        "first_game": dt.datetime.fromtimestamp(games[0]["end_time"], dt.timezone.utc).date().isoformat() if games else None,
        "last_game": dt.datetime.fromtimestamp(games[-1]["end_time"], dt.timezone.utc).date().isoformat() if games else None,
        "analyzed_window": None,
        "by_time_class": {},
    }
    if recs:
        ts = sorted(r["end_time"] for r in recs)
        S["overview"]["analyzed_window"] = [dt.datetime.fromtimestamp(t, dt.timezone.utc).date().isoformat() for t in (ts[0], ts[-1])]
    for tc, rows in sorted(by_tc.items(), key=lambda kv: -len(kv[1])):
        rows.sort()
        res = [r[1] for r in rows]
        w, d, l = record_line(res)
        ratings = [r[2] for r in rows if r[2]]
        S["overview"]["by_time_class"][tc] = {"games": len(rows), "wins": w, "draws": d, "losses": l,
                                              "score_pct": score_pct(res),
                                              "rating_first": ratings[0] if ratings else None,
                                              "rating_last": ratings[-1] if ratings else None,
                                              "rating_peak": max(ratings) if ratings else None}

    if not recs:
        S["engine_sections"] = "FAILED: no engine-analyzed games available"
        return S, recs

    def tot(key, who):
        return sum(r[who][key] for r in recs)

    # ---- CHAOS (Marcelo)
    chaos_vals = sorted(r["chaos_index"] for r in recs if r["chaos_index"] is not None)
    chaos = {"games": len(chaos_vals)}
    if len(chaos_vals) >= 3 * MIN_N:
        ranked = sorted((r for r in recs if r["chaos_index"] is not None), key=lambda r: (r["chaos_index"], r["url"]))
        third = len(ranked) // 3
        lo = [r["result"] for r in ranked[:third]]
        hi = [r["result"] for r in ranked[-third:]]
        chaos.update({"tercile_cuts": [ranked[third - 1]["chaos_index"], ranked[-third]["chaos_index"]], "score_high_chaos": score_pct(hi), "n_high": len(hi),
                      "score_low_chaos": score_pct(lo), "n_low": len(lo)})
    else:
        chaos["terciles"] = f"short (need {3 * MIN_N} games)"
    chaos["median_chaos_index"] = round(statistics.median(chaos_vals), 3) if chaos_vals else None
    for who in ("me", "opp"):
        chaos[f"{who}_sharp_moves"] = tot("sharp_moves", who)
        chaos[f"{who}_sharp_errors"] = tot("sharp_errors", who)
        chaos[f"{who}_sharp_error_rate"] = rate(tot("sharp_errors", who), tot("sharp_moves", who))
        calm_moves = tot("moves", who) - tot("sharp_moves", who)
        calm_err = tot("mist", who) + tot("blund", who) - tot("sharp_errors", who)
        chaos[f"{who}_nonsharp_error_rate"] = rate(calm_err, calm_moves)
    chaos["chaos_dividend_per_game"] = round((tot("sharp_errors", "opp") - tot("sharp_errors", "me")) / len(recs), 2)
    oc = [r["result"] for r in recs if r["opposite_castling"]]
    im = [r["result"] for r in recs if r["imbalanced"]]
    chaos.update({"opposite_castling_games": len(oc), "opposite_castling_score": score_pct(oc),
                  "imbalanced_games": len(im), "imbalanced_score": score_pct(im),
                  "overall_score": score_pct([r["result"] for r in recs])})
    lost_pos = [r for r in recs if r["min_wp"] <= LOSING]
    chaos.update({"games_reached_lost_position": len(lost_pos),
                  "saved_from_lost_rate": rate(sum(r["result"] >= 0.5 for r in lost_pos), len(lost_pos)),
                  "missed_punishes_total": sum(r["missed_punish"] for r in recs),
                  "opp_blunders_total": tot("blund", "opp")})
    S["chaos"] = chaos

    # ---- PRECISION (Fischer)
    won_pos = [r for r in recs if r["max_wp"] >= WINNING]
    prec = {"games_reached_winning_position": len(won_pos),
            "converted_rate": rate(sum(r["result"] == 1 for r in won_pos), len(won_pos)),
            "thrown_to_loss_rate": rate(sum(r["result"] == 0 for r in won_pos), len(won_pos)),
            "my_blunders_per_game": round(tot("blund", "me") / len(recs), 2),
            "my_mistakes_per_game": round(tot("mist", "me") / len(recs), 2),
            "my_inaccuracies_per_game": round(tot("inacc", "me") / len(recs), 2),
            "opp_blunders_per_game": round(tot("blund", "opp") / len(recs), 2),
            "my_avg_accuracy": round(statistics.fmean(r["me"]["acc"] for r in recs if r["me"]["acc"] is not None), 1),
            "opp_avg_accuracy": round(statistics.fmean(r["opp"]["acc"] for r in recs if r["opp"]["acc"] is not None), 1),
            "phase": {}}
    for ph in ("opening", "middlegame", "endgame"):
        mv = sum(r["me"]["phase"][ph][0] for r in recs)
        er = sum(r["me"]["phase"][ph][1] for r in recs)
        omv = sum(r["opp"]["phase"][ph][0] for r in recs)
        oer = sum(r["opp"]["phase"][ph][1] for r in recs)
        prec["phase"][ph] = {"my_moves": mv, "my_errors": er, "my_error_rate": rate(er, mv),
                             "opp_moves": omv, "opp_errors": oer, "opp_error_rate": rate(oer, omv)}
    S["precision"] = prec

    # ---- CLOCK
    timed = [r for r in recs if r["n_spent_sharp"] + r["n_spent_calm"] > 0]
    sharp_t = [(r["spent_sharp"], r["n_spent_sharp"]) for r in timed if r["spent_sharp"] is not None]
    calm_t = [(r["spent_calm"], r["n_spent_calm"]) for r in timed if r["spent_calm"] is not None]
    wavg = lambda xs: round(sum(a * n for a, n in xs) / sum(n for _, n in xs), 2) if xs and sum(n for _, n in xs) else None
    clock = {"timed_games": len(timed),
             "my_pressure_moves": tot("pressure_moves", "me"), "my_pressure_errors": tot("pressure_errors", "me"),
             "my_pressure_error_rate": rate(tot("pressure_errors", "me"), tot("pressure_moves", "me")),
             "my_calm_error_rate": rate(tot("calm_errors", "me"), tot("calm_moves", "me")),
             "my_calm_moves": tot("calm_moves", "me"),
             "avg_seconds_on_sharp_moves": wavg(sharp_t), "n_sharp_timed": sum(n for _, n in sharp_t),
             "avg_seconds_on_other_moves": wavg(calm_t), "n_other_timed": sum(n for _, n in calm_t)}
    tl = [g for g in games if (g["white"] if g["white"]["username"].lower() == USER else g["black"]).get("result") == "timeout"]
    tw = [g for g in games if (g["black"] if g["white"]["username"].lower() == USER else g["white"]).get("result") == "timeout"]
    clock.update({"losses_on_time_all_games": len(tl), "wins_on_time_all_games": len(tw),
                  "losses_all_games": sum(1 for g in games if result_for((g["white"] if g["white"]["username"].lower() == USER else g["black"]).get("result")) == 0)})
    S["clock"] = clock

    # ---- OPENINGS (score from all games; errors from analyzed)
    op = defaultdict(lambda: {"results": [], "early_errors": 0, "analyzed": 0})
    for g in games:
        is_w = g["white"]["username"].lower() == USER
        me = g["white"] if is_w else g["black"]
        _, fam = opening_names(g.get("eco"))
        k = ("white" if is_w else "black", fam)
        op[k]["results"].append(result_for(me.get("result")))
    for r in recs:
        k = (r["color"], r["family"])
        op[k]["analyzed"] += 1
        op[k]["early_errors"] += r["me"]["phase"]["opening"][1]
    rows = []
    for (color, fam), v in op.items():
        n = len(v["results"])
        rows.append({"color": color, "family": fam, "games": n, "score_pct": score_pct(v["results"]),
                     "sample_ok": n >= MIN_N, "analyzed": v["analyzed"],
                     "opening_errors_per_game": round(v["early_errors"] / v["analyzed"], 2) if v["analyzed"] else None})
    rows.sort(key=lambda x: -x["games"])
    S["openings"] = rows

    # ---- TILT (all games)
    seq = []
    for g in games:
        me = g["white"] if g["white"]["username"].lower() == USER else g["black"]
        hdr = chess.pgn.read_headers(io.StringIO(g["pgn"]))
        seq.append((start_ts(hdr) if hdr else None, g.get("end_time"), result_for(me.get("result"))))
    after_loss, after_win, after_draw = [], [], []
    for prev, cur in zip(seq, seq[1:]):
        if cur[0] is None or prev[1] is None:
            continue
        gap = (cur[0] - prev[1]) / 60
        if 0 <= gap <= BACK_TO_BACK_MIN:
            {0.0: after_loss, 1.0: after_win, 0.5: after_draw}[prev[2]].append(cur[2])
    S["tilt"] = {"score_after_loss": score_pct(after_loss), "n_after_loss": len(after_loss),
                 "score_after_win": score_pct(after_win), "n_after_win": len(after_win),
                 "score_after_draw": score_pct(after_draw), "n_after_draw": len(after_draw)}

    # ---- PUZZLES
    puz = []
    for r in sorted(recs, key=lambda r: -(r["end_time"] or 0)):
        for p in r["puzzles"]:
            puz.append({**p, "game": r["url"], "date": dt.datetime.fromtimestamp(r["end_time"], dt.timezone.utc).date().isoformat(),
                        "time_class": r["time_class"], "opening": r["opening"]})
    S["puzzles"] = {"total": len(puz), "sharp": sum(p["sharp"] for p in puz),
                    "by_phase": {ph: sum(p["phase"] == ph for p in puz) for ph in ("opening", "middlegame", "endgame")}}
    return S, puz


# ------------------------------------------------------------------ report
def pct(v):
    return "—" if v is None else f"{v}%"


def write_report(S, puz):
    os.makedirs(os.path.join("reports", "history"), exist_ok=True)
    json.dump(S, open(os.path.join("reports", "summary.json"), "w"), indent=2)
    with open(os.path.join("reports", "puzzles.csv"), "w", newline="") as f:
        cols = ["date", "time_class", "opening", "move_no", "side", "phase", "sharp", "loss", "played", "best", "fen", "game"]
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(puz)

    o = S["overview"]
    L = [f"# Chess report: {S['username']}", "",
         f"Generated {S['generated_at']} UTC · Stockfish depth {S['engine_depth']} · time classes: {S['time_classes_included']}", "",
         f"Games on disk: **{o['games_on_disk']}** ({o['first_game']} → {o['last_game']}). "
         f"Engine-analyzed: **{o['games_engine_analyzed']}**"
         + (f" ({o['analyzed_window'][0]} → {o['analyzed_window'][1]})" if o["analyzed_window"] else "")
         + f". Failed to parse: {o['games_failed_parse']}. Under 10 plies (skipped): {o['games_too_short_skipped']}.", "",
         "> Thresholds below are conventions, not measurements (see `summary.json → assumptions`). "
         f"Any rate on fewer than {MIN_N} observations prints as **short**.", "",
         "## Record by time control", "", "| Time class | Games | W / D / L | Score | Rating first → last (peak) |",
         "|---|---|---|---|---|"]
    for tc, v in o["by_time_class"].items():
        L.append(f"| {tc} | {v['games']} | {v['wins']} / {v['draws']} / {v['losses']} | {pct(v['score_pct'])} | "
                 f"{v['rating_first']} → {v['rating_last']} ({v['rating_peak']}) |")

    if isinstance(S.get("engine_sections"), str):
        L += ["", f"**{S['engine_sections']}**"]
        open(os.path.join("reports", "latest.md"), "w").write("\n".join(L) + "\n")
        return

    c, p, k, t = S["chaos"], S["precision"], S["clock"], S["tilt"]

    def n_ok(rate_v, n):
        return pct(rate_v) if n >= MIN_N else "short"

    L += ["", "## 1. Chaos: do scrambles pay you or them?", "",
          f"A position is *sharp* when the best move beats the second-best by ≥{SHARP_GAP} win-chance points "
          "(miss it and you're in trouble). Chaos index = share of positions after move 8 that are sharp.", "",
          f"- Median chaos index of your games: **{c['median_chaos_index']}**"]
    if "score_high_chaos" in c:
        L.append(f"- Score in your most chaotic third of games: **{pct(c['score_high_chaos'])}** (n={c['n_high']}) "
                 f"vs calmest third: **{pct(c['score_low_chaos'])}** (n={c['n_low']}). Overall: {pct(c['overall_score'])}.")
    else:
        L.append(f"- Chaos terciles: {c['terciles']}")
    L += [f"- Error rate (mistake or blunder) on sharp moves: **you {n_ok(c['me_sharp_error_rate'], c['me_sharp_moves'])}** "
          f"(n={c['me_sharp_moves']}) vs **opponents {n_ok(c['opp_sharp_error_rate'], c['opp_sharp_moves'])}** (n={c['opp_sharp_moves']})",
          f"- Error rate on non-sharp moves: you {pct(c['me_nonsharp_error_rate'])}, opponents {pct(c['opp_nonsharp_error_rate'])}",
          f"- **Chaos dividend**: {c['chaos_dividend_per_game']:+} per game (opponent sharp-move errors minus yours; positive = chaos favors you)",
          f"- Score in opposite-side castling games: {n_ok(c['opposite_castling_score'], c['opposite_castling_games'])}; n={c['opposite_castling_games']}",
          f"- Score in imbalanced-material games: {n_ok(c['imbalanced_score'], c['imbalanced_games'])}; n={c['imbalanced_games']}",
          f"- Reached a lost position (≤{LOSING}% win chance) in {c['games_reached_lost_position']} games; "
          f"saved (drew or won) {n_ok(c['saved_from_lost_rate'], c['games_reached_lost_position'])}",
          f"- Opponent blunders: {c['opp_blunders_total']}. Times you answered one with a mistake of your own (missed punish): **{c['missed_punishes_total']}**",
          "", "## 2. Precision: finishing like Fischer", "",
          f"- Reached a winning position (≥{WINNING}% win chance) in {p['games_reached_winning_position']} games. "
          f"Converted to a win: **{n_ok(p['converted_rate'], p['games_reached_winning_position'])}**. "
          f"Went on to lose: {n_ok(p['thrown_to_loss_rate'], p['games_reached_winning_position'])}.",
          f"- Per game: {p['my_blunders_per_game']} blunders, {p['my_mistakes_per_game']} mistakes, {p['my_inaccuracies_per_game']} inaccuracies "
          f"(opponents: {p['opp_blunders_per_game']} blunders)",
          f"- Average move accuracy (lichess formula, not chess.com CAPS): you {p['my_avg_accuracy']}, opponents {p['opp_avg_accuracy']}", "",
          "| Phase | Your moves | Your error rate | Opp error rate |", "|---|---|---|---|"]
    for ph, v in p["phase"].items():
        L.append(f"| {ph} | {v['my_moves']} | {n_ok(v['my_error_rate'], v['my_moves'])} | {n_ok(v['opp_error_rate'], v['opp_moves'])} |")
    L += ["", "## 3. Clock", "",
          f"- Error rate under time pressure (<{int(PRESSURE_FRAC * 100)}% of starting clock): **{n_ok(k['my_pressure_error_rate'], k['my_pressure_moves'])}** "
          f"(n={k['my_pressure_moves']}) vs otherwise {n_ok(k['my_calm_error_rate'], k['my_calm_moves'])}",
          f"- Average seconds per move on sharp moves: **{k['avg_seconds_on_sharp_moves']}** (n={k['n_sharp_timed']}) "
          f"vs other moves: **{k['avg_seconds_on_other_moves']}** (n={k['n_other_timed']})",
          f"- Losses on time: {k['losses_on_time_all_games']} of {k['losses_all_games']} losses (all games). Wins on time: {k['wins_on_time_all_games']}.",
          "", "## 4. Openings (all games; families with ≥10 games ranked)", "",
          "| Color | Opening family | Games | Score | Opening-phase errors / game (analyzed) |", "|---|---|---|---|---|"]
    for r in [r for r in S["openings"] if r["sample_ok"]][:15]:
        L.append(f"| {r['color']} | {r['family']} | {r['games']} | {pct(r['score_pct'])} | "
                 f"{'—' if r['opening_errors_per_game'] is None else r['opening_errors_per_game']} (n={r['analyzed']}) |")
    small = [r for r in S["openings"] if not r["sample_ok"]]
    L.append(f"\n{len(small)} other families have fewer than {MIN_N} games each (in summary.json, not ranked).")
    L += ["", f"## 5. Tilt (next game started within {BACK_TO_BACK_MIN} min)", "",
          f"- After a loss: {n_ok(t['score_after_loss'], t['n_after_loss'])} (n={t['n_after_loss']})",
          f"- After a win: {n_ok(t['score_after_win'], t['n_after_win'])} (n={t['n_after_win']})",
          f"- After a draw: {n_ok(t['score_after_draw'], t['n_after_draw'])} (n={t['n_after_draw']})",
          "", "## 6. Your drill deck", "",
          f"`puzzles.csv` holds **{S['puzzles']['total']}** of your own mistakes/blunders with the engine's move "
          f"({S['puzzles']['sharp']} in sharp positions; by phase {S['puzzles']['by_phase']}). "
          "Paste a FEN into chess.com → Analysis board to drill it.", ""]
    text = "\n".join(L) + "\n"
    open(os.path.join("reports", "latest.md"), "w").write(text)
    open(os.path.join("reports", "history", dt.date.today().isoformat() + ".md"), "w").write(text)


def main():
    if not USER:
        sys.exit("FAILED: set CHESS_USERNAME.")
    games = load_games()
    if not games:
        sys.exit(f"FAILED: no standard-chess games for '{USER}' in data/games (check username / TIME_CLASSES).")
    cache = load_cache()
    n = run_engine(games, cache)
    print(f"engine: analyzed {n} new games; cache holds {len(cache)}")
    S, puz = aggregate(games, cache)
    write_report(S, puz)
    print("wrote reports/latest.md, reports/summary.json, reports/puzzles.csv")


if __name__ == "__main__":
    main()
