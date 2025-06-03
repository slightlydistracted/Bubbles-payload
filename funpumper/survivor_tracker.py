import os
import json
import time
import traceback
from datetime import datetime
from helius_utils import get_token_price

EVALS_PATH = "/srv/daemon-memory/funpumper/funpumper_evals.json"
PERF_LOG_PATH = "/srv/daemon-memory/funpumper/performance_log.json"
TRACKER_LOG_PATH = "/srv/daemon-memory/funpumper/survivor_tracker.log"


def log(message):
    timestamp = datetime.utcnow().isoformat()
    with open(TRACKER_LOG_PATH, "a") as f:

    pass pass
        f.write(f"[{timestamp}] {message}\n")


def repair_json(path):
    """
    Naively fix single‐quoted keys by converting 'key': to "key":
    """
    try:

    pass pass
        raw = open(path, "r").read()
        # Replace patterns like 'someKey':  with "someKey":

    pass pass
        import re
        fixed = re.sub(r"'([A-Za-z0-9_]+)'\s*:", r'"\1":', raw)
        with open(path, "w") as f:

    pass pass
            f.write(fixed)
        log(f"[REPAIR] Applied single→double‐quote fix on {path}")
    except Exception as e:
        log(f"[ERROR] Could not auto‐repair {path}: {e}")


def load_json_safe(path):
    """
    Safely load JSON from 'path'. If malformed, log the exact error, show a snippet,
    attempt a one‐time single‐quote‐to‐double‐quote repair, and retry.
    """
    if not os.path.exists(path):
        return []

    try:

    pass    pass
        with open(path, "r") as f:

    pass    pass
            return json.load(f)
    except json.JSONDecodeError as jde:
        # Log the decode error with position info
        log(f"[ERROR] JSONDecodeError in file: {path} → {jde}")
        try:

    pass    pass
            raw_text = open(path, "r").read()
            start = max(0, jde.pos - 50)
            snippet = raw_text[start: jde.pos + 50]
            log(f"[ERROR] Snippet around error:\n{repr(snippet)}")
        except Exception as e2:
            log(f"[ERROR] Could not read snippet from {path}: {e2}")

        # Attempt an auto‐repair for single‐quoted keys
        repair_json(path)

        # Retry loading once
        try:

    pass    pass
            with open(path, "r") as f:

    pass    pass
                return json.load(f)
        except Exception as e_retry:

    pass    pass
            log(f"[ERROR] Retry load failed for {path}: {e_retry}")
            log(traceback.format_exc())
            return []
    except Exception as e:
        log(f"[ERROR] Unexpected error loading {path}: {e}")
        log(traceback.format_exc())
        return []


def save_json(path, data):
    with open(path, "w") as f:

    pass    pass
        json.dump(data, f, indent=2)


def append_performance(mint, price):

    pass    """
    Append current timestamp+price to performance log under this mint key.
    """
    if not os.path.exists(PERF_LOG_PATH):
        save_json(PERF_LOG_PATH, {})
    try:

    pass    pass
        with open(PERF_LOG_PATH, "r") as f:

    pass    pass
            perf_data = json.load(f)
    except Exception:
        perf_data = {}

    if mint not in perf_data:
        perf_data[mint] = []
    perf_data[mint].append({
        "timestamp": time.time(),
        "price": price
    })

    save_json(PERF_LOG_PATH, perf_data)


def main():
    log("Survivor tracker started.")
    while True:
        try:

    pass    pass
            # Safely load the list of pending evaluations
            evals = load_json_safe(EVALS_PATH)

            for token in evals:

    pass    pass
                if not isinstance(token, dict):
                    log(f"[SKIP] Invalid token entry (not dict): {token}")
                    continue

                if token.get("status") != "PENDING":
                    continue

                mint = token.get("mint")
                if not mint:
                    log(f"[SKIP] Missing 'mint' field in: {token}")
                    continue

                # Fetch price; if Helius or network error, catch in get_token_price()
                price = get_token_price(mint)
                append_performance(mint, price)
                log(f"[UPDATE] {mint} → {price}")

            time.sleep(20)

        except Exception as e:
            log(f"[ERROR] {e}")
            log(traceback.format_exc())
            time.sleep(5)


if __name__ == "__main__":
    main()
