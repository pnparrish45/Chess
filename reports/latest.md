# Chess report: swed45

Generated 2026-10-26T17:33+00:00 UTC · Stockfish depth 12 · time classes: all

Games on disk: **6224** (2022-01-18 → 2026-10-26). Engine-analyzed: **1179** (2026-03-11 → 2026-10-26). Failed to parse: 0. Under 10 plies (skipped): 21.

> Thresholds below are conventions, not measurements (see `summary.json → assumptions`). Any rate on fewer than 10 observations prints as **short**.

## Record by time control

| Time class | Games | W / D / L | Score | Rating first → last (peak) |
|---|---|---|---|---|
| rapid | 6209 | 2947 / 283 / 2979 | 49.7% | 1342 → 997 (1457) |
| daily | 14 | 4 / 0 / 10 | 28.6% | 1006 → 1002 (1178) |
| blitz | 1 | 1 / 0 / 0 | 100.0% | 1031 → 1031 (1031) |

## 1. Chaos: do scrambles pay you or them?

A position is *sharp* when the best move beats the second-best by ≥15 win-chance points (miss it and you're in trouble). Chaos index = share of positions after move 8 that are sharp.

- Median chaos index of your games: **0.074**
- Score in your most chaotic third of games: **45.1%** (n=387) vs calmest third: **51.8%** (n=387). Overall: 48.7%.
- Error rate (mistake or blunder) on sharp moves: **you 22.5%** (n=3040) vs **opponents 21.8%** (n=2812)
- Error rate on non-sharp moves: you 3.5%, opponents 3.7%
- **Chaos dividend**: -0.06 per game (opponent sharp-move errors minus yours; positive = chaos favors you)
- Score in opposite-side castling games: 44.6%; n=193
- Score in imbalanced-material games: 50.2%; n=217
- Reached a lost position (≤20% win chance) in 785 games; saved (drew or won) 28.8%
- Opponent blunders: 1109. Times you answered one with a mistake of your own (missed punish): **363**

## 2. Precision: finishing like Fischer

- Reached a winning position (≥80% win chance) in 751 games. Converted to a win: **68.7%**. Went on to lose: 26.5%.
- Per game: 0.95 blunders, 0.86 mistakes, 2.62 inaccuracies (opponents: 0.94 blunders)
- Average move accuracy (lichess formula, not chess.com CAPS): you 84.9, opponents 85.3

| Phase | Your moves | Your error rate | Opp error rate |
|---|---|---|---|
| opening | 13976 | 2.7% | 3.2% |
| middlegame | 24940 | 6.2% | 6.1% |
| endgame | 5086 | 3.9% | 3.6% |

## 3. Clock

- Error rate under time pressure (<10% of starting clock): **5.7%** (n=280) vs otherwise 4.8%
- Average seconds per move on sharp moves: **5.25** (n=3040) vs other moves: **6.33** (n=40962)
- Losses on time: 50 of 2989 losses (all games). Wins on time: 304.

## 4. Openings (all games; families with ≥10 games ranked)

| Color | Opening family | Games | Score | Opening-phase errors / game (analyzed) |
|---|---|---|---|---|
| white | Kings Pawn Opening | 1821 | 54.4% | 0.24 (n=291) |
| black | Kings Pawn Opening | 1364 | 49.9% | 0.31 (n=250) |
| black | Queens Pawn Opening | 484 | 42.0% | 0.44 (n=86) |
| white | Scandinavian Defense | 272 | 46.0% | 0.44 (n=45) |
| black | Bishops Opening | 263 | 47.0% | 0.42 (n=57) |
| white | Sicilian Defense | 221 | 47.3% | 0.5 (n=40) |
| white | Caro Kann Defense | 217 | 48.4% | 0.26 (n=46) |
| white | French Defense | 207 | 50.5% | 0.25 (n=48) |
| black | Vienna Game | 148 | 51.0% | 0.34 (n=35) |
| black | French Defense | 142 | 47.9% | 0.54 (n=24) |
| black | Center Game | 102 | 50.5% | 0.25 (n=4) |
| white | Pirc Defense | 96 | 42.2% | 0.4 (n=20) |
| black | English Opening | 76 | 47.4% | 0.5 (n=16) |
| black | Van t Kruijs Opening | 69 | 42.0% | 0.38 (n=8) |
| white | Nimzowitsch Defense | 62 | 53.2% | 0.56 (n=9) |

39 other families have fewer than 10 games each (in summary.json, not ranked).

## 5. Tilt (next game started within 15 min)

- After a loss: 50.2% (n=1211)
- After a win: 50.7% (n=1422)
- After a draw: 50.8% (n=121)

## 6. Your drill deck

`puzzles.csv` holds **2131** of your own mistakes/blunders with the engine's move (685 in sharp positions; by phase {'opening': 382, 'middlegame': 1550, 'endgame': 199}). Paste a FEN into chess.com → Analysis board to drill it.

