import json
import os
from datetime import datetime

EVAL_PATH = "/srv/daemon-memory/funpumper/funpumper_evals.json"
WEIGHT_OUT = "/srv/daemon-memory/funpumper/funpumper_weights.json"

def load_json(path, default=[]):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def compute_weights(evals):
    weights = {}
    now = int(datetime.utcnow().timestamp())
    for item in evals:
        mint = item.get("mint")
        age = now - item.get("launch_ts", now)
        init_mcap = item.get("init_mcap", 0)
        volume = item.get("volume24h", 0)

        # Weight components
        score = 0
        score += 2 if init_mcap < 10000 else 1 if init_mcap < 50000 else -1
        score += 2 if volume > 25000 else 1 if volume > 10000 else -1
        score += 1 if age < 3600 else 0

        weights[mint] = {
            "score": score,
            "age": age,
            "symbol": item.get("symbol", "???"),
            "status": item.get("status", "UNKNOWN"),
            "predicted_moon": item.get("predicted_moon", False)
        }

    return weights

def main():
    evals = load_json(EVAL_PATH, [])
    weights = compute_weights(evals)
    save_json(WEIGHT_OUT, weights)
    print(f"[{datetime.utcnow().isoformat()}] Weights saved to {WEIGHT_OUT} ({len(weights)} tokens)")

if __name__ == "__main__":
    main()

