import sys
import os; sys.path.append(
    os.path.abspath(
        os.path.dirname(__file__) +
         "/../../"))
#!/usr/bin/env python3
import os
import subprocess
import time
from datetime import datetime

# Use your existing PAT; fallback to the old hardcoded one if unset
GITHUB_TOKEN = os.getenv(
    "GITHUB_PAT", "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")

# Change CLONE_DIR to point at historical_tokens so downstream parsers
# will find data there
CLONE_DIR = "/srv/daemon-memory/funpumper/historical_tokens"
INTERVAL_HOURS = 6

REPOS = [
    "solsniperxyz/pumpfun-snipe-data",
    "0xHanzo/pumpfun_tools",
    "T4uru/pumpfun-analysis"
]


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def clone_or_pull(repo):
    user_repo = repo.split("/")[-1]
    target_path = os.path.join(CLONE_DIR, user_repo)

    # Ensure the parent directory exists
    if not os.path.exists(CLONE_DIR):
        os.makedirs(CLONE_DIR)

    if os.path.exists(target_path):
        log(f"Updating {repo}...")
        subprocess.run(
            ["git", "-C", target_path, "pull"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    else:
        url = f"https://{GITHUB_TOKEN}:x-oauth-basic@github.com/{repo}.git"
        log(f"Cloning {repo}...")
        subprocess.run(
            ["git", "clone", url, target_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )


def main():
    log("FunPumper GitHub sync loop started")
    while True:
        for repo in REPOS:

            try:
    pass

                clone_or_pull(repo)
            except Exception as e:
                log(f"[✗] Failed to access {repo}: {e}")
        log(f"Sleeping {INTERVAL_HOURS} hours...\n")
        time.sleep(INTERVAL_HOURS * 3600)


if __name__ == "__main__":
    main()
