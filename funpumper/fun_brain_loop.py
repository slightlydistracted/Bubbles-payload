import os
import json
import time
from datetime import datetime
from random import uniform

WEIGHTS_PATH = "/srv/daemon-memory/funpumper/funpumper_weights.json"
LOG_PATH = "/srv/daemon-memory/funpumper/fun_brain_loop.log"
PREDICTION_LOG = "/srv/daemon-memory/funpumper/fun_predictions.json"

TRAIT_WEIGHTS = {
    "age": 0.2,
    "status": 0.3,
    "price_log": 0.3,
    "randomness": 0.2,
}

PREDICTION_THRESHOLD = 0.85

def log(message):
    timestamp = datetime.utcnow().isoformat()
    with open(LOG_PATH, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

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

def score_token(t):
    score = 0.0

    # Age score
    age = t.get("age", 0)
    age_score = min(age / 10000, 1.0) if age > 0 else 0.0
    score += age_score * TRAIT_WEIGHTS["age"]

    # Status influence
    status = t.get("status", "PENDING")
    status_score = {"PENDING": 0.2, "ACTIVE": 0.7, "FINAL": 0.5}.get(status, 0.1)
    score += status_score * TRAIT_WEIGHTS["status"]

    # Price volatility
    price_log = t.get("price_log", [])
    vol = 0.0
    if isinstance(price_log, list) and len(price_log) >= 2:
        diffs = [abs(price_log[i] - price_log[i - 1]) for i in range(1, len(price_log))]
        vol = sum(diffs) / len(diffs)
        vol_score = min(vol / 0.1, 1.0)
    else:
        vol_score = 0.0
    score += vol_score * TRAIT_WEIGHTS["price_log"]

    # Randomness
    rand_score = uniform(0.0, 1.0)
    score += rand_score * TRAIT_WEIGHTS["randomness"]

    return round(min(score, 1.0), 4)

def brain_loop():
    log("FunBrain (Phase 2) engaged.")
    tokens = load_json(WEIGHTS_PATH)
    predictions = load_json(PREDICTION_LOG)
    updated = 0

    for mint, t in tokens.items():
        brain_score = score_token(t)
        t["brain_score"] = brain_score
        updated += 1

        # Make prediction
        if brain_score >= PREDICTION_THRESHOLD and mint not in predictions:
            predictions[mint] = {
                "predicted_at": datetime.utcnow().isoformat(),
                "score": brain_score,
                "confirmed_moon": False,
                "accuracy_checked": False
            }
            log(f"[PREDICTION] {mint} (Score: {brain_score})")

        if updated % 500 == 0:
            log(f"[UPDATE] {updated} tokens scored...")

    save_json(WEIGHTS_PATH, tokens)
    save_json(PREDICTION_LOG, predictions)
    log(f"[COMPLETE] Brain scored {updated} tokens.")

if __name__ == "__main__":
    while True:
        brain_loop()
        time.sleep(600)  # 10-minute loop
