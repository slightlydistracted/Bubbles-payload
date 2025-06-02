#!/usr/bin/env python3
import os, json, time
from datetime import datetime

WEIGHTS_PATH     = "/srv/daemon-memory/funpumper/funpumper_weights.json"
PREDICTIONS_PATH = "/srv/daemon-memory/funpumper/fun_predictions.json"
LOG_PATH         = "/srv/daemon-memory/funpumper/fun_predict_eval_loop.log"

# how strong a signal before we “predict a moon”
PREDICT_THRESHOLD = 0.8

def log(msg):
    ts = datetime.utcnow().isoformat()
    with open(LOG_PATH, "a") as f:
        f.write(f"[{ts}] {msg}\n")

def load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return default

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def run_once():
    weights = load_json(WEIGHTS_PATH, {})
    preds   = load_json(PREDICTIONS_PATH, [])
    seen    = {p["mint"] for p in preds}

    new_mints = []
    for mint, info in weights.items():
        score = info.get("score", 0.0)
        if score >= PREDICT_THRESHOLD and mint not in seen:
            preds.append({
                "mint":         mint,
                "predicted_at": datetime.utcnow().isoformat(),
                "score":        score,
                "outcome":      None
            })
            new_mints.append(mint)
            log(f"[PREDICT]   {mint}  (score {score:.2f})")

    if new_mints:
        save_json(preds, PREDICTIONS_PATH)
        log(f"[UPDATE]    {len(new_mints)} new predictions")
    else:
        log("[PASS]      no new predictions")

def main():
    log("🔮 Prediction loop started.")
    while True:
        try:
            run_once()
        except Exception as e:
            log(f"[ERROR] {e}")
        time.sleep(300)  # every 5 minutes

if __name__ == "__main__":
    main()
