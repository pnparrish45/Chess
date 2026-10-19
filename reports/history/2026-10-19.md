# Chess report: swed45

Generated 2026-10-19T17:27+00:00 UTC · Stockfish depth 12 · time classes: all

Games on disk: **6131** (2022-01-18 → 2026-10-19). Engine-analyzed: **982** (2026-03-18 → 2026-10-19). Failed to parse: 0. Under 10 plies (skipped): 18.

> Thresholds below are conventions, not measurements (see `summary.json → assumptions`). Any rate on fewer than 10 observations prints as **short**.

## Record by time control

| Time class | Games | W / D / L | Score | Rating first → last (peak) |
|---|---|---|---|---|
| rapid | 6116 | 2901 / 280 / 2935 | 49.7% | 1342 → 974 (1457) |
| daily | 14 | 4 / 0 / 10 | 28.6% | 1006 → 1002 (1178) |
| blitz | 1 | 1 / 0 / 0 | 100.0% | 1031 → 1031 (1031) |

## 1. Chaos: do scrambles pay you or them?

A position is *sharp* when the best move beats the second-best by ≥15 win-chance points (miss it and you're in trouble). Chaos index = share of positions after move 8 that are sharp.

- Median chaos index of your games: **0.075**
- Score in your most chaotic third of games: **43.6%** (n=322) vs calmest third: **53.3%** (n=322). Overall: 48.1%.
- Error rate (mistake or blunder) on sharp moves: **you 23.0%** (n=2553) vs **opponents 21.8%** (n=2365)
- Error rate on non-sharp moves: you 3.5%, opponents 3.7%
- **Chaos dividend**: -0.07 per game (opponent sharp-move errors minus yours; positive = chaos favors you)
- Score in opposite-side castling games: 43.6%; n=165
- Score in imbalanced-material games: 48.9%; n=181
- Reached a lost position (≤20% win chance) in 653 games; saved (drew or won) 28.0%
- Opponent blunders: 926. Times you answered one with a mistake of your own (missed punish): **310**

## 2. Precision: finishing like Fischer

- Reached a winning position (≥80% win chance) in 619 games. Converted to a win: **68.0%**. Went on to lose: 27.0%.
- Per game: 0.96 blunders, 0.86 mistakes, 2.62 inaccuracies (opponents: 0.94 blunders)
- Average move accuracy (lichess formula, not chess.com CAPS): you 84.8, opponents 85.3

| Phase | Your moves | Your error rate | Opp error rate |
|---|---|---|---|
| opening | 11637 | 2.8% | 3.2% |
| middlegame | 20711 | 6.3% | 6.0% |
| endgame | 4347 | 4.0% | 3.6% |

## 3. Clock

- Error rate under time pressure (<10% of starting clock): **5.4%** (n=241) vs otherwise 4.9%
- Average seconds per move on sharp moves: **5.33** (n=2553) vs other moves: **6.31** (n=34142)
- Losses on time: 47 of 2945 losses (all games). Wins on time: 300.

## 4. Openings (all games; families with ≥10 games ranked)

| Color | Opening family | Games | Score | Opening-phase errors / game (analyzed) |
|---|---|---|---|---|
| white | Kings Pawn Opening | 1815 | 54.5% | 0.26 (n=257) |
| black | Kings Pawn Opening | 1360 | 49.9% | 0.32 (n=221) |
| black | Queens Pawn Opening | 478 | 42.4% | 0.49 (n=73) |
| white | Scandinavian Defense | 269 | 46.5% | 0.38 (n=40) |
| black | Bishops Opening | 257 | 46.9% | 0.27 (n=44) |
| white | Sicilian Defense | 220 | 47.0% | 0.53 (n=36) |
| white | Caro Kann Defense | 215 | 48.4% | 0.24 (n=37) |
| white | French Defense | 204 | 49.8% | 0.27 (n=41) |
| black | Vienna Game | 145 | 51.4% | 0.37 (n=27) |
| black | French Defense | 139 | 47.5% | 0.5 (n=20) |
| black | Center Game | 101 | 50.0% | 0.0 (n=2) |
| white | Pirc Defense | 94 | 42.0% | 0.41 (n=17) |
| black | English Opening | 74 | 45.9% | 0.42 (n=12) |
| black | Van t Kruijs Opening | 68 | 42.6% | 0.43 (n=7) |
| white | Nimzowitsch Defense | 61 | 52.5% | 0.71 (n=7) |

39 other families have fewer than 10 games each (in summary.json, not ranked).

## 5. Tilt (next game started within 15 min)

- After a loss: 50.3% (n=1185)
- After a win: 50.3% (n=1388)
- After a draw: 51.7% (n=119)

## 6. Your drill deck

`puzzles.csv` holds **1788** of your own mistakes/blunders with the engine's move (586 in sharp positions; by phase {'opening': 321, 'middlegame': 1295, 'endgame': 172}). Paste a FEN into chess.com → Analysis board to drill it.

