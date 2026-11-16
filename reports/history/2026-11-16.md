# Chess report: swed45

Generated 2026-11-16T21:11+00:00 UTC · Stockfish depth 12 · time classes: all

Games on disk: **6416** (2022-01-18 → 2026-11-16). Engine-analyzed: **1775** (2026-01-29 → 2026-11-16). Failed to parse: 0. Under 10 plies (skipped): 25.

> Thresholds below are conventions, not measurements (see `summary.json → assumptions`). Any rate on fewer than 10 observations prints as **short**.

## Record by time control

| Time class | Games | W / D / L | Score | Rating first → last (peak) |
|---|---|---|---|---|
| rapid | 6401 | 3037 / 291 / 3073 | 49.7% | 1342 → 974 (1457) |
| daily | 14 | 4 / 0 / 10 | 28.6% | 1006 → 1002 (1178) |
| blitz | 1 | 1 / 0 / 0 | 100.0% | 1031 → 1031 (1031) |

## 1. Chaos: do scrambles pay you or them?

A position is *sharp* when the best move beats the second-best by ≥15 win-chance points (miss it and you're in trouble). Chaos index = share of positions after move 8 that are sharp.

- Median chaos index of your games: **0.071**
- Score in your most chaotic third of games: **45.5%** (n=584) vs calmest third: **51.2%** (n=584). Overall: 49.2%.
- Error rate (mistake or blunder) on sharp moves: **you 23.6%** (n=4484) vs **opponents 22.3%** (n=4117)
- Error rate on non-sharp moves: you 3.5%, opponents 3.7%
- **Chaos dividend**: -0.08 per game (opponent sharp-move errors minus yours; positive = chaos favors you)
- Score in opposite-side castling games: 45.6%; n=275
- Score in imbalanced-material games: 51.9%; n=346
- Reached a lost position (≤20% win chance) in 1192 games; saved (drew or won) 29.9%
- Opponent blunders: 1714. Times you answered one with a mistake of your own (missed punish): **576**

## 2. Precision: finishing like Fischer

- Reached a winning position (≥80% win chance) in 1111 games. Converted to a win: **70.0%**. Went on to lose: 25.2%.
- Per game: 0.96 blunders, 0.86 mistakes, 2.62 inaccuracies (opponents: 0.97 blunders)
- Average move accuracy (lichess formula, not chess.com CAPS): you 84.8, opponents 85.3

| Phase | Your moves | Your error rate | Opp error rate |
|---|---|---|---|
| opening | 21048 | 3.0% | 3.4% |
| middlegame | 37331 | 6.2% | 6.0% |
| endgame | 7729 | 3.7% | 3.4% |

## 3. Clock

- Error rate under time pressure (<10% of starting clock): **6.9%** (n=462) vs otherwise 4.9%
- Average seconds per move on sharp moves: **5.43** (n=4484) vs other moves: **6.28** (n=61624)
- Losses on time: 57 of 3083 losses (all games). Wins on time: 316.

## 4. Openings (all games; families with ≥10 games ranked)

| Color | Opening family | Games | Score | Opening-phase errors / game (analyzed) |
|---|---|---|---|---|
| white | Kings Pawn Opening | 1830 | 54.4% | 0.29 (n=429) |
| black | Kings Pawn Opening | 1370 | 49.8% | 0.36 (n=355) |
| black | Queens Pawn Opening | 504 | 41.8% | 0.45 (n=133) |
| white | Scandinavian Defense | 282 | 45.4% | 0.44 (n=68) |
| black | Bishops Opening | 273 | 47.6% | 0.4 (n=81) |
| white | Sicilian Defense | 227 | 47.8% | 0.52 (n=61) |
| white | Caro Kann Defense | 221 | 47.7% | 0.23 (n=64) |
| white | French Defense | 213 | 50.5% | 0.26 (n=68) |
| black | Vienna Game | 150 | 51.7% | 0.36 (n=44) |
| black | French Defense | 148 | 48.0% | 0.55 (n=40) |
| black | Center Game | 103 | 51.0% | 0.8 (n=10) |
| white | Pirc Defense | 99 | 42.9% | 0.32 (n=28) |
| black | English Opening | 79 | 48.1% | 0.41 (n=29) |
| black | Philidor Defense | 74 | 59.5% | 0.27 (n=66) |
| black | Van t Kruijs Opening | 73 | 42.5% | 0.57 (n=14) |

39 other families have fewer than 10 games each (in summary.json, not ranked).

## 5. Tilt (next game started within 15 min)

- After a loss: 50.0% (n=1253)
- After a win: 50.5% (n=1477)
- After a draw: 53.1% (n=127)

## 6. Your drill deck

`puzzles.csv` holds **3233** of your own mistakes/blunders with the engine's move (1057 in sharp positions; by phase {'opening': 624, 'middlegame': 2321, 'endgame': 288}). Paste a FEN into chess.com → Analysis board to drill it.

