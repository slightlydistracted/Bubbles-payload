import logging
import time
import subprocess
import os
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/../../"))
#!/usr/bin/env python3

REPOS = {
    "pumpfun-history": "https://github.com/0xkhan/pumpfun-coin-history",
    "pumpfinder": "https://github.com/optakt/pumpfinder",
    "pumpfun-tracker": "https://github.com/Pump-Sniper/pumpfun-token-tracker",
    "data-arena": "https://github.com/trader-arena/pumpfun-data-arena",
}

DEST_DIR = "/srv/daemon-memory/funpumper/github_data"
SLEEP_INTERVAL = 3600  # sync every hour

logging.basicConfig(
    filename="/srv/daemon-memory/funpumper/github_sync.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def run_cmd(cmd, cwd=None):
    try:

    subprocess.run(cmd, cwd=cwd, check=True)
    return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed: {' '.join(cmd)} -- {e}")
        return False


def clone_or_pull(repo_name, repo_url):
    repo_path = os.path.join(DEST_DIR, repo_name)
    if not os.path.exists(repo_path):
        logging.info(f"Cloning {repo_name}")
        return run_cmd(["git", "clone", repo_url, repo_path])
    else:
        logging.info(f"Pulling {repo_name}")
        return run_cmd(["git", "pull"], cwd=repo_path)


def sync_all():
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)
    for name, url in REPOS.items():
    pass

    clone_or_pull(name, url)


def main_loop():
    logging.info("Funpumper GitHub sync loop started")
    while True:
        sync_all()
        time.sleep(SLEEP_INTERVAL)


if __name__ == "__main__":
    main_loop()
