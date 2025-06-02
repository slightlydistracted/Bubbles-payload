import requests
from email.utils import parsedate_to_datetime
from datetime import timezone
import json
from pathlib import Path

def get_network_time():
    try:
        r = requests.head("http://google.com", timeout=5)
        date_str = r.headers["Date"]
        dt = parsedate_to_datetime(date_str)
        print(f"[LILITH CLOCK] UTC: {dt.isoformat()}")
        return dt
    except Exception as e:
        print(f"[LILITH CLOCK] Failed to fetch UTC: {e}")
        return None

def write_sync_timestamp():
    dt = get_network_time()
    if dt:
        Path("~/feralsys/system").expanduser().mkdir(parents=True, exist_ok=True)
        timestamp_path = Path("~/feralsys/system/utc_timestamp.json").expanduser()
        with open(timestamp_path, "w") as f:
            json.dump({"utc": dt.isoformat()}, f, indent=2)
        print(f"[LILITH CLOCK] Wrote timestamp to {timestamp_path}")

if __name__ == "__main__":
    write_sync_timestamp()
