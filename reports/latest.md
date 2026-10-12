# Chess report: swed45

Generated 2026-10-12T20:18+00:00 UTC · Stockfish depth 12 · time classes: all

Games on disk: **6067** (2022-01-18 → 2026-10-12). Engine-analyzed: **785** (2026-03-30 → 2026-10-12). Failed to parse: 0. Under 10 plies (skipped): 15.

> Thresholds below are conventions, not measurements (see `summary.json → assumptions`). Any rate on fewer than 10 observations prints as **short**.

## Record by time control

| Time class | Games | W / D / L | Score | Rating first → last (peak) |
|---|---|---|---|---|
| rapid | 6052 | 2869 / 278 / 2905 | 49.7% | 1342 → 961 (1457) |
| daily | 14 | 4 / 0 / 10 | 28.6% | 1006 → 1002 (1178) |
| blitz | 1 | 1 / 0 / 0 | 100.0% | 1031 → 1031 (1031) |

## 1. Chaos: do scrambles pay you or them?

A position is *sharp* when the best move beats the second-best by ≥15 win-chance points (miss it and you're in trouble). Chaos index = share of positions after move 8 that are sharp.

- Median chaos index of your games: **0.075**
- Score in your most chaotic third of games: **44.4%** (n=257) vs calmest third: **54.1%** (n=257). Overall: 49.2%.
- Error rate (mistake or blunder) on sharp moves: **you 22.7%** (n=2022) vs **opponents 21.8%** (n=1923)
- Error rate on non-sharp moves: you 3.5%, opponents 3.7%
- **Chaos dividend**: -0.05 per game (opponent sharp-move errors minus yours; positive = chaos favors you)
- Score in opposite-side castling games: 44.6%; n=130
- Score in imbalanced-material games: 49.3%; n=150
- Reached a lost position (≤20% win chance) in 513 games; saved (drew or won) 29.0%
- Opponent blunders: 753. Times you answered one with a mistake of your own (missed punish): **258**

## 2. Precision: finishing like Fischer

- Reached a winning position (≥80% win chance) in 497 games. Converted to a win: **68.4%**. Went on to lose: 26.6%.
- Per game: 0.95 blunders, 0.85 mistakes, 2.64 inaccuracies (opponents: 0.96 blunders)
- Average move accuracy (lichess formula, not chess.com CAPS): you 84.9, opponents 85.3

| Phase | Your moves | Your error rate | Opp error rate |
|---|---|---|---|
| opening | 9305 | 2.7% | 3.2% |
| middlegame | 16824 | 6.1% | 6.0% |
| endgame | 3515 | 4.0% | 3.6% |

## 3. Clock

- Error rate under time pressure (<10% of starting clock): **5.7%** (n=209) vs otherwise 4.8%
- Average seconds per move on sharp moves: **5.2** (n=2022) vs other moves: **6.31** (n=27622)
- Losses on time: 47 of 2915 losses (all games). Wins on time: 299.

## 4. Openings (all games; families with ≥10 games ranked)

| Color | Opening family | Games | Score | Opening-phase errors / game (analyzed) |
|---|---|---|---|---|
| white | Kings Pawn Opening | 1807 | 54.4% | 0.27 (n=213) |
| black | Kings Pawn Opening | 1357 | 50.0% | 0.33 (n=180) |
| black | Queens Pawn Opening | 469 | 42.6% | 0.4 (n=57) |
| white | Scandinavian Defense | 267 | 46.4% | 0.24 (n=34) |
| black | Bishops Opening | 255 | 46.9% | 0.32 (n=38) |
| white | Sicilian Defense | 219 | 46.8% | 0.56 (n=32) |
| white | Caro Kann Defense | 213 | 48.4% | 0.29 (n=28) |
| white | French Defense | 203 | 49.5% | 0.25 (n=32) |
| black | Vienna Game | 143 | 51.4% | 0.43 (n=21) |
| black | French Defense | 138 | 47.8% | 0.4 (n=15) |
| black | Center Game | 101 | 50.0% | 0.0 (n=2) |
| white | Pirc Defense | 93 | 42.5% | 0.55 (n=11) |
| black | English Opening | 74 | 45.9% | 0.36 (n=11) |
| black | Van t Kruijs Opening | 68 | 42.6% | 0.5 (n=6) |
| white | Nimzowitsch Defense | 61 | 52.5% | 0.71 (n=7) |

40 other families have fewer than 10 games each (in summary.json, not ranked).

## 5. Tilt (next game started within 15 min)

- After a loss: 50.3% (n=1169)
- After a win: 50.3% (n=1372)
- After a draw: 52.1% (n=118)

## 6. Your drill deck

`puzzles.csv` holds **1418** of your own mistakes/blunders with the engine's move (458 in sharp positions; by phase {'opening': 254, 'middlegame': 1025, 'endgame': 139}). Paste a FEN into chess.com → Analysis board to drill it.

