#!/usr/bin/env python3
import os
import json
import time
from datetime import datetime

# === PATHS ===
WEIGHTS_PATH = "/srv/daemon-memory/funpumper/funpumper_weights.json"
RESULTS_PATH = "/srv/daemon-memory/funpumper/funpumper_evals.json"
LOOP_LOG = "/srv/daemon-memory/funpumper/funpumper_loop.log"


def log(msg):
    ts = datetime.utcnow().isoformat()
    line = f"[{ts}] {msg}"
    with open(LOOP_LOG, "a") as f:
    pass

        f.write(line + "\n")


def load_weights():
    if not os.path.exists(WEIGHTS_PATH):
        return {}
    try:
    pass

        return json.load(open(WEIGHTS_PATH, "r"))
    except json.JSONDecodeError:
        log("⚠️ Failed to decode weights JSON.")
        return {}


def save_weights(w):
    with open(WEIGHTS_PATH, "w") as f:

        json.dump(w, f, indent=2)


def load_real_tokens():
    if not os.path.exists(RESULTS_PATH):
        log(f"⚠️ No evals file at {RESULTS_PATH}")
        return {}
    try:
    pass

        raw = json.load(open(RESULTS_PATH, "r"))
    except json.JSONDecodeError:
        log("⚠️ Failed to decode evals JSON.")
        return {}

    out = {}
    if isinstance(raw, list):
        for entry in raw:
    pass

            if isinstance(entry, dict):
                m = entry.get("mint")
                if m:
                    out[m] = entry
    elif isinstance(raw, dict):
        for m, val in raw.items():
    pass

            if isinstance(val, dict):
                entry = dict(val)
                entry.setdefault("mint", m)
                out[m] = entry
            else:
                log(f"⚠️ Unexpected evals entry for {m}: {type(val)}")
    else:
        log(f"⚠️ Evals file has unrecognized type: {type(raw)}")

    return out


def loop_once():
    weights = load_weights()
    results = load_real_tokens()
    new_count = 0

    for mint, data in results.items():
    pass

        if mint in weights:
            continue
        weights[mint] = {
            "score": data.get("score", 1),
            "age": data.get("age", 0),
            "status": data.get("status", "PENDING"),
            "predicted_moon": data.get("predicted_moon", False),
            "price_log": data.get("price_log", []),
            "mint_time": data.get("launch_ts", int(time.time()))
        }
        log(f"[ADDED] {mint}")
        new_count += 1

    if new_count:
        log(f"[UPDATE] Added {new_count} new tokens.")
        save_weights(weights)
    else:
        log("[PASS] No new tokens found.")


def main_loop():
    log("🌕 FunPumper loop (real mode) started.")
    while True:
        try:

            loop_once()
            time.sleep(60)
        except Exception as e:
            log(f"[ERROR] {e}")
            time.sleep(30)


if __name__ == "__main__":
    main_loop()
