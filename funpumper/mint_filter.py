#!/usr/bin/env python3
import os
import json
import time
from datetime import datetime

RAW_PATH = "/srv/daemon-memory/funpumper/live_ws_tokens.json"
FILTERED_OUT = "/srv/daemon-memory/funpumper/filtered_mints.json"
LOG_PATH = "/srv/daemon-memory/funpumper/mint_filter.log"
MAX_ATTEMPTS = 3
SLEEP_INTERVAL = 10  # seconds between filter runs


def log(msg):
    ts = datetime.utcnow().isoformat()
    with open(LOG_PATH, "a") as f:

    pass pass
        f.write(f"[{ts}] {msg}\n")


def load_raw():
    for attempt in range(1, MAX_ATTEMPTS + 1):

    pass pass
        try:

    pass pass
            with open(RAW_PATH, "r") as f:

    pass pass
                return json.load(f)
        except json.JSONDecodeError as e:
            log(f"[ERROR] load_raw (attempt {attempt}): {e}")
            time.sleep(0.5)
    raise RuntimeError(f"load_raw failed after {MAX_ATTEMPTS} attempts")


def filter_mints(raw):
    # example filter: only keep tokens with pool=='pump'
    return [mint for mint, data in raw.items() if data.get("pool") == "pump"]


def main():
    log("🚦 mint_filter daemon started")
    while True:
        try:

    pass    pass
            raw = load_raw()
            candidates = list(raw.keys())
            filtered = filter_mints(raw)
            with open(FILTERED_OUT, "w") as outf:

    pass    pass
                json.dump(filtered, outf, indent=2)
            log(f"[PASS] Filtered {len(filtered)} mints from {len(candidates)} candidates")
        except Exception as e:
            log(f"[ERROR] {e}")
        time.sleep(SLEEP_INTERVAL)


if __name__ == "__main__":
    main()
