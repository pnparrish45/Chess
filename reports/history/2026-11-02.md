# Chess report: swed45

Generated 2026-11-02T20:52+00:00 UTC · Stockfish depth 12 · time classes: all

Games on disk: **6308** (2022-01-18 → 2026-11-02). Engine-analyzed: **1377** (2026-03-04 → 2026-11-02). Failed to parse: 0. Under 10 plies (skipped): 23.

> Thresholds below are conventions, not measurements (see `summary.json → assumptions`). Any rate on fewer than 10 observations prints as **short**.

## Record by time control

| Time class | Games | W / D / L | Score | Rating first → last (peak) |
|---|---|---|---|---|
| rapid | 6293 | 2992 / 287 / 3014 | 49.8% | 1342 → 1074 (1457) |
| daily | 14 | 4 / 0 / 10 | 28.6% | 1006 → 1002 (1178) |
| blitz | 1 | 1 / 0 / 0 | 100.0% | 1031 → 1031 (1031) |

## 1. Chaos: do scrambles pay you or them?

A position is *sharp* when the best move beats the second-best by ≥15 win-chance points (miss it and you're in trouble). Chaos index = share of positions after move 8 that are sharp.

- Median chaos index of your games: **0.073**
- Score in your most chaotic third of games: **46.2%** (n=452) vs calmest third: **53.3%** (n=452). Overall: 49.8%.
- Error rate (mistake or blunder) on sharp moves: **you 22.7%** (n=3531) vs **opponents 21.7%** (n=3231)
- Error rate on non-sharp moves: you 3.5%, opponents 3.7%
- **Chaos dividend**: -0.07 per game (opponent sharp-move errors minus yours; positive = chaos favors you)
- Score in opposite-side castling games: 45.3%; n=215
- Score in imbalanced-material games: 51.7%; n=259
- Reached a lost position (≤20% win chance) in 907 games; saved (drew or won) 29.7%
- Opponent blunders: 1299. Times you answered one with a mistake of your own (missed punish): **422**

## 2. Precision: finishing like Fischer

- Reached a winning position (≥80% win chance) in 875 games. Converted to a win: **70.2%**. Went on to lose: 25.0%.
- Per game: 0.94 blunders, 0.85 mistakes, 2.59 inaccuracies (opponents: 0.94 blunders)
- Average move accuracy (lichess formula, not chess.com CAPS): you 84.9, opponents 85.4

| Phase | Your moves | Your error rate | Opp error rate |
|---|---|---|---|
| opening | 16328 | 2.8% | 3.3% |
| middlegame | 28998 | 6.2% | 6.0% |
| endgame | 5869 | 3.9% | 3.5% |

## 3. Clock

- Error rate under time pressure (<10% of starting clock): **4.8%** (n=392) vs otherwise 4.8%
- Average seconds per move on sharp moves: **5.31** (n=3531) vs other moves: **6.36** (n=47664)
- Losses on time: 52 of 3024 losses (all games). Wins on time: 312.

## 4. Openings (all games; families with ≥10 games ranked)

| Color | Opening family | Games | Score | Opening-phase errors / game (analyzed) |
|---|---|---|---|---|
| white | Kings Pawn Opening | 1824 | 54.5% | 0.26 (n=334) |
| black | Kings Pawn Opening | 1366 | 49.9% | 0.32 (n=275) |
| black | Queens Pawn Opening | 493 | 42.1% | 0.44 (n=101) |
| white | Scandinavian Defense | 276 | 46.0% | 0.42 (n=53) |
| black | Bishops Opening | 269 | 47.2% | 0.39 (n=69) |
| white | Sicilian Defense | 224 | 48.0% | 0.47 (n=49) |
| white | Caro Kann Defense | 219 | 47.9% | 0.24 (n=49) |
| white | French Defense | 209 | 50.5% | 0.23 (n=53) |
| black | Vienna Game | 149 | 51.3% | 0.32 (n=38) |
| black | French Defense | 145 | 48.3% | 0.54 (n=28) |
| black | Center Game | 102 | 50.5% | 0.5 (n=6) |
| white | Pirc Defense | 98 | 42.3% | 0.35 (n=23) |
| black | English Opening | 78 | 48.7% | 0.48 (n=25) |
| black | Van t Kruijs Opening | 72 | 43.1% | 0.36 (n=11) |
| white | Nimzowitsch Defense | 62 | 53.2% | 0.56 (n=9) |

39 other families have fewer than 10 games each (in summary.json, not ranked).

## 5. Tilt (next game started within 15 min)

- After a loss: 50.1% (n=1227)
- After a win: 50.7% (n=1449)
- After a draw: 52.4% (n=125)

## 6. Your drill deck

`puzzles.csv` holds **2465** of your own mistakes/blunders with the engine's move (802 in sharp positions; by phase {'opening': 453, 'middlegame': 1785, 'endgame': 227}). Paste a FEN into chess.com → Analysis board to drill it.

