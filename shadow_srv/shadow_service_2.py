#!/usr/bin/env python3
import json
import time

OUTPUT_PATH = "common/data_feeds/alternative_data.json"

def run_service():
    while True:
        # Mock: produce a random off-chain metric
        data = {"timestamp": time.time(), "sentiment": 0.75}
        with open(OUTPUT_PATH, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[SHADOW2] Wrote alternative data")
        time.sleep(600)  # update every 10 minutes

if __name__ == "__main__":
    run_service()
