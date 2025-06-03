#!/usr/bin/env python3
import ntplib
import time
import json
from datetime import datetime

LOG_PATH = "common/logs/clock_offset.log"


def sync_and_log():
    client = ntplib.NTPClient()
    try:
        response = client.request('time.google.com')
        offset = response.offset
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "offset_seconds": offset
        }
        with open(LOG_PATH, "a") as f:
            f.write(json.dumps(entry) + "\n")
        print(f"[CLOCK_SYNC] Offset: {offset:.4f} s")
    except Exception as e:
        with open(LOG_PATH, "a") as f:
            f.write(json.dumps({
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e)
            }) + "\n")
        print(f"[CLOCK_SYNC] Error: {e}")


if __name__ == "__main__":
    while True:
        sync_and_log()
        time.sleep(3600)  # run once every hour
