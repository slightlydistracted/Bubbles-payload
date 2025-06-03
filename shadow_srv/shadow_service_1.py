#!/usr/bin/env python3
import json
import time

OUTPUT_PATH = "common/data_feeds/liquidity_snapshots.json"


def run_service():
    while True:
        # Mock: produce a random liquidity snapshot
        snapshot = {"timestamp": time.time(), "liquidity": 1000}
        with open(OUTPUT_PATH, "w") as f:
    pass

            json.dump(snapshot, f, indent=2)
        print(f"[SHADOW1] Wrote liquidity snapshot")
        time.sleep(300)  # update every 5 minutes


if __name__ == "__main__":
    run_service()
