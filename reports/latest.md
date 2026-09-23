# Chess report: swed45

Generated 2026-09-23T02:38+00:00 UTC · Stockfish depth 12 · time classes: all

Games on disk: **5940** (2022-01-18 → 2026-09-23). Engine-analyzed: **193** (2026-07-26 → 2026-09-23). Failed to parse: 0. Under 10 plies (skipped): 7.

> Thresholds below are conventions, not measurements (see `summary.json → assumptions`). Any rate on fewer than 10 observations prints as **short**.

## Record by time control

| Time class | Games | W / D / L | Score | Rating first → last (peak) |
|---|---|---|---|---|
| rapid | 5925 | 2814 / 272 / 2839 | 49.8% | 1342 → 1039 (1457) |
| daily | 14 | 4 / 0 / 10 | 28.6% | 1006 → 1002 (1178) |
| blitz | 1 | 1 / 0 / 0 | 100.0% | 1031 → 1031 (1031) |

## 1. Chaos: do scrambles pay you or them?

A position is *sharp* when the best move beats the second-best by ≥15 win-chance points (miss it and you're in trouble). Chaos index = share of positions after move 8 that are sharp.

- Median chaos index of your games: **0.07**
- Score in your most chaotic third of games: **42.9%** (n=63) vs calmest third: **57.9%** (n=63). Overall: 50.0%.
- Error rate (mistake or blunder) on sharp moves: **you 23.6%** (n=483) vs **opponents 21.4%** (n=449)
- Error rate on non-sharp moves: you 3.5%, opponents 3.8%
- **Chaos dividend**: -0.09 per game (opponent sharp-move errors minus yours; positive = chaos favors you)
- Score in opposite-side castling games: 47.0%; n=33
- Score in imbalanced-material games: 47.5%; n=40
- Reached a lost position (≤20% win chance) in 119 games; saved (drew or won) 26.9%
- Opponent blunders: 190. Times you answered one with a mistake of your own (missed punish): **71**

## 2. Precision: finishing like Fischer

- Reached a winning position (≥80% win chance) in 124 games. Converted to a win: **66.1%**. Went on to lose: 29.0%.
- Per game: 0.94 blunders, 0.85 mistakes, 2.62 inaccuracies (opponents: 0.98 blunders)
- Average move accuracy (lichess formula, not chess.com CAPS): you 84.8, opponents 85.0

| Phase | Your moves | Your error rate | Opp error rate |
|---|---|---|---|
| opening | 2290 | 3.1% | 3.2% |
| middlegame | 3909 | 6.2% | 6.2% |
| endgame | 947 | 3.4% | 3.4% |

## 3. Clock

- Error rate under time pressure (<10% of starting clock): **11.1%** (n=36) vs otherwise 4.8%
- Average seconds per move on sharp moves: **4.98** (n=483) vs other moves: **5.95** (n=6663)
- Losses on time: 42 of 2849 losses (all games). Wins on time: 295.

## 4. Openings (all games; families with ≥10 games ranked)

| Color | Opening family | Games | Score | Opening-phase errors / game (analyzed) |
|---|---|---|---|---|
| white | Kings Pawn Opening | 1785 | 54.3% | 0.34 (n=47) |
| black | Kings Pawn Opening | 1339 | 50.1% | 0.35 (n=43) |
| black | Queens Pawn Opening | 460 | 43.0% | 0.44 (n=16) |
| white | Scandinavian Defense | 259 | 46.7% | 0.23 (n=13) |
| black | Bishops Opening | 251 | 46.8% | 0.33 (n=12) |
| white | Sicilian Defense | 214 | 47.0% | 0.67 (n=9) |
| white | Caro Kann Defense | 208 | 48.1% | 0.4 (n=5) |
| white | French Defense | 199 | 49.5% | 0.29 (n=7) |
| black | Vienna Game | 139 | 51.4% | 0.6 (n=5) |
| black | French Defense | 136 | 48.5% | 0.43 (n=7) |
| black | Center Game | 101 | 50.0% | — (n=0) |
| white | Pirc Defense | 90 | 42.2% | 0.75 (n=4) |
| black | English Opening | 74 | 45.9% | 0.67 (n=3) |
| black | Van t Kruijs Opening | 67 | 41.8% | 1.0 (n=1) |
| white | Nimzowitsch Defense | 61 | 52.5% | 0.5 (n=2) |

40 other families have fewer than 10 games each (in summary.json, not ranked).

## 5. Tilt (next game started within 15 min)

- After a loss: 50.3% (n=1134)
- After a win: 50.5% (n=1346)
- After a draw: 52.6% (n=117)

## 6. Your drill deck

`puzzles.csv` holds **347** of your own mistakes/blunders with the engine's move (114 in sharp positions; by phase {'opening': 71, 'middlegame': 244, 'endgame': 32}). Paste a FEN into chess.com → Analysis board to drill it.

