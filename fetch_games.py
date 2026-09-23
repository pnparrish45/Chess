"""Pull every game for CHESS_USERNAME from the chess.com public API.

Stores one raw JSON file per month in data/games/YYYY-MM.json.
Months already on disk are skipped, except the two most recent
(the current month keeps changing; the previous one may have been
fetched mid-month). No login or API key is needed.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

USER = os.environ.get("CHESS_USERNAME", "").strip().lower()
UA = "chess-sensei-report/1.0 (personal game analysis via GitHub Actions)"
OUT = os.path.join("data", "games")


def get(url, tries=5):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                sys.exit(f"FAILED: chess.com returned 404 for {url}. Check the username '{USER}'.")
            last = f"HTTP {e.code}"
            time.sleep(15 * (i + 1) if e.code == 429 else 5 * (i + 1))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            last = repr(e)
            time.sleep(5 * (i + 1))
    raise RuntimeError(f"FAILED after {tries} tries: {url} ({last})")


def main():
    if not USER:
        sys.exit("FAILED: set the CHESS_USERNAME repository variable (Settings > Secrets and variables > Actions > Variables).")
    os.makedirs(OUT, exist_ok=True)
    archives = get(f"https://api.chess.com/pub/player/{USER}/games/archives").get("archives", [])
    if not archives:
        sys.exit(f"FAILED: chess.com lists no game archives for '{USER}'. Nothing to analyze.")

    refetch = set(archives[-2:])
    fetched = skipped = 0
    for url in archives:
        yyyy, mm = url.rstrip("/").split("/")[-2:]
        path = os.path.join(OUT, f"{yyyy}-{mm}.json")
        if os.path.exists(path) and url not in refetch:
            skipped += 1
            continue
        data = get(url)
        games = data.get("games")
        if games is None:
            raise RuntimeError(f"FAILED: {url} answered without a 'games' field")
        with open(path, "w") as f:
            json.dump(games, f)
        fetched += 1
        time.sleep(1)  # be polite; chess.com rate-limits parallel/fast calls
    total = sum(len(json.load(open(os.path.join(OUT, p)))) for p in os.listdir(OUT) if p.endswith(".json"))
    print(f"months fetched: {fetched}, months already cached: {skipped}, games on disk: {total}")


if __name__ == "__main__":
    main()
