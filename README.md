# chess-sensei

Weekly Stockfish audit of your chess.com games, tuned for one question:
**do you profit from chaos, and do you finish clean?**

Every Monday (and whenever you press the button) GitHub Actions:

1. pulls your full game history from chess.com's public API (no login needed),
2. runs Stockfish over every new game (2 lines per position, so it can tell a *sharp* position from a calm one),
3. writes `reports/latest.md`, `reports/summary.json` and `reports/puzzles.csv`, and commits them.

## Setup (10 minutes, all in the GitHub website)

1. **Create the repo.** github.com → **+** → *New repository* → name it `chess-sensei`.
   Public is simplest (your chess.com games are already public; there are no secrets in this repo).
   Tick *Add a README* so the repo isn't empty. Create.
2. **Add the files.** On the repo page: *Add file* → *Upload files* → drag in
   `fetch_games.py`, `analyze.py`, `requirements.txt`, `README.md`. Commit.
3. **Add the workflow** (the `.github` folder is hidden on Mac/Windows, so create it by hand):
   *Add file* → *Create new file* → in the name box type exactly
   `.github/workflows/sensei.yml` (GitHub turns the slashes into folders) → paste the contents of
   `sensei.yml` → Commit.
4. **Tell it who you are.** *Settings* → *Secrets and variables* → *Actions* → **Variables** tab →
   *New repository variable* → Name `CHESS_USERNAME`, Value = your chess.com username. Add.
   Optional variables: `TIME_CLASSES` (e.g. `blitz,rapid` to ignore bullet/daily), `ENGINE_DEPTH` (default 12).
5. **Let the bot commit.** *Settings* → *Actions* → *General* → scroll to *Workflow permissions* →
   choose **Read and write permissions** → Save.
6. **First run.** *Actions* tab → *Sensei weekly report* → *Run workflow* → set *max_games* to `400`
   for the first backfill → *Run workflow*. Expect 20–60 minutes. Later runs only analyze new games.
7. **Read it.** Open `reports/latest.md` in the repo (or the run's *Summary* page shows the same text).
   Give the raw link of `reports/summary.json` to your Claude project:
   `https://raw.githubusercontent.com/<you>/chess-sensei/main/reports/summary.json`

If a run fails, the log says why in a line that starts with `FAILED:` (wrong username, chess.com down, etc.).
The scripts never print a zero when a source didn't answer.

## What the report measures

| Section | Question | Key figures |
|---|---|---|
| Chaos | Do sharp positions hurt them more than you? | chaos index, error rate on sharp moves (you vs opp), *chaos dividend*, opposite-side castling, material imbalance, comebacks, missed punishes |
| Precision | Do you finish? | conversion rate from ≥80% positions, blunders/game, errors by phase |
| Clock | Do you slow down when it matters? | seconds on sharp vs calm moves, error rate under time pressure, losses on time |
| Openings | Which families pay? | score by family and color (ranked only with ≥10 games) |
| Tilt | Do you play worse right after a loss? | score of games started within 15 min of a loss/win |
| Drill deck | What to fix? | `puzzles.csv`: FEN, your move, engine move, for every mistake/blunder you made |

All thresholds (what counts as "sharp", "blunder", "time pressure"...) are conventions, listed in
`summary.json → assumptions` and at the top of each report. Rates on fewer than 10 observations print as **short**.

## Running locally

```
pip install -r requirements.txt   # plus Stockfish: apt-get install stockfish / brew install stockfish
CHESS_USERNAME=yourname python fetch_games.py
CHESS_USERNAME=yourname MAX_GAMES=100 python analyze.py
```
