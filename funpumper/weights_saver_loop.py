import os
import time
import json
from datetime import datetime

BRAIN_WEIGHTS = "/srv/daemon-memory/funpumper/fun_brain_weights.json"
WEIGHT_SNAPSHOTS = "/srv/daemon-memory/funpumper/weights_archive.json"
WEIGHTS_LOG = "/srv/daemon-memory/funpumper/weights_saver.log"

def log(msg):
    timestamp = datetime.utcnow().isoformat()
    with open(WEIGHTS_LOG, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def snapshot_loop():
    log("Weights snapshot loop started.")
    while True:
        weights = load_json(BRAIN_WEIGHTS)
        if weights:
            save_json(WEIGHT_SNAPSHOTS, weights)
            log(f"[SNAPSHOT] {len(weights)} tokens saved.")
        else:
            log("[SKIP] No weights found.")
        time.sleep(300)  # Every 5 minutes

if __name__ == "__main__":
    snapshot_loop()
