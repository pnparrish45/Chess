# Chess report: swed45

Generated 2026-11-09T21:30+00:00 UTC · Stockfish depth 12 · time classes: all

Games on disk: **6365** (2022-01-18 → 2026-11-09). Engine-analyzed: **1576** (2026-02-19 → 2026-11-09). Failed to parse: 0. Under 10 plies (skipped): 24.

> Thresholds below are conventions, not measurements (see `summary.json → assumptions`). Any rate on fewer than 10 observations prints as **short**.

## Record by time control

| Time class | Games | W / D / L | Score | Rating first → last (peak) |
|---|---|---|---|---|
| rapid | 6350 | 3023 / 289 / 3038 | 49.9% | 1342 → 1140 (1457) |
| daily | 14 | 4 / 0 / 10 | 28.6% | 1006 → 1002 (1178) |
| blitz | 1 | 1 / 0 / 0 | 100.0% | 1031 → 1031 (1031) |

## 1. Chaos: do scrambles pay you or them?

A position is *sharp* when the best move beats the second-best by ≥15 win-chance points (miss it and you're in trouble). Chaos index = share of positions after move 8 that are sharp.

- Median chaos index of your games: **0.071**
- Score in your most chaotic third of games: **46.4%** (n=518) vs calmest third: **52.2%** (n=518). Overall: 49.7%.
- Error rate (mistake or blunder) on sharp moves: **you 23.2%** (n=4031) vs **opponents 22.2%** (n=3708)
- Error rate on non-sharp moves: you 3.5%, opponents 3.7%
- **Chaos dividend**: -0.07 per game (opponent sharp-move errors minus yours; positive = chaos favors you)
- Score in opposite-side castling games: 46.0%; n=249
- Score in imbalanced-material games: 51.3%; n=297
- Reached a lost position (≤20% win chance) in 1047 games; saved (drew or won) 29.9%
- Opponent blunders: 1507. Times you answered one with a mistake of your own (missed punish): **503**

## 2. Precision: finishing like Fischer

- Reached a winning position (≥80% win chance) in 994 games. Converted to a win: **70.5%**. Went on to lose: 24.8%.
- Per game: 0.95 blunders, 0.86 mistakes, 2.59 inaccuracies (opponents: 0.96 blunders)
- Average move accuracy (lichess formula, not chess.com CAPS): you 84.9, opponents 85.4

| Phase | Your moves | Your error rate | Opp error rate |
|---|---|---|---|
| opening | 18690 | 2.9% | 3.4% |
| middlegame | 33269 | 6.2% | 6.0% |
| endgame | 6979 | 3.8% | 3.5% |

## 3. Clock

- Error rate under time pressure (<10% of starting clock): **6.2%** (n=435) vs otherwise 4.8%
- Average seconds per move on sharp moves: **5.32** (n=4031) vs other moves: **6.29** (n=54907)
- Losses on time: 54 of 3048 losses (all games). Wins on time: 315.

## 4. Openings (all games; families with ≥10 games ranked)

| Color | Opening family | Games | Score | Opening-phase errors / game (analyzed) |
|---|---|---|---|---|
| white | Kings Pawn Opening | 1826 | 54.5% | 0.27 (n=376) |
| black | Kings Pawn Opening | 1368 | 49.9% | 0.34 (n=313) |
| black | Queens Pawn Opening | 499 | 42.2% | 0.47 (n=117) |
| white | Scandinavian Defense | 279 | 45.5% | 0.46 (n=61) |
| black | Bishops Opening | 272 | 47.8% | 0.4 (n=77) |
| white | Sicilian Defense | 227 | 47.8% | 0.5 (n=58) |
| white | Caro Kann Defense | 219 | 47.9% | 0.24 (n=55) |
| white | French Defense | 211 | 50.5% | 0.26 (n=62) |
| black | Vienna Game | 150 | 51.7% | 0.32 (n=41) |
| black | French Defense | 146 | 48.6% | 0.53 (n=34) |
| black | Center Game | 103 | 51.0% | 0.67 (n=9) |
| white | Pirc Defense | 99 | 42.9% | 0.33 (n=24) |
| black | English Opening | 78 | 48.7% | 0.46 (n=26) |
| black | Van t Kruijs Opening | 73 | 42.5% | 0.5 (n=12) |
| white | Nimzowitsch Defense | 62 | 53.2% | 0.45 (n=11) |

39 other families have fewer than 10 games each (in summary.json, not ranked).

## 5. Tilt (next game started within 15 min)

- After a loss: 50.3% (n=1238)
- After a win: 50.6% (n=1469)
- After a draw: 52.8% (n=126)

## 6. Your drill deck

`puzzles.csv` holds **2861** of your own mistakes/blunders with the engine's move (935 in sharp positions; by phase {'opening': 541, 'middlegame': 2056, 'endgame': 264}). Paste a FEN into chess.com → Analysis board to drill it.

