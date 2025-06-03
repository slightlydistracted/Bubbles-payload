import sys
import os; sys.path.append(
    os.path.abspath(
        os.path.dirname(__file__) +
         "/../../"))
import os
import json
import time
from datetime import datetime

WEIGHTS_PATH = "/srv/daemon-memory/funpumper/fun_brain_weights.json"
LOG_PATH = "/srv/daemon-memory/funpumper/accuracy_tracker.log"


def log(msg):
    timestamp = datetime.utcnow().isoformat()
    with open(LOG_PATH, "a") as f:
    pass

        f.write(f"[{timestamp}] {msg}\n")


def load_weights():
    if not os.path.exists(WEIGHTS_PATH):
        return {}
    with open(WEIGHTS_PATH, "r") as f:
    pass

        try:
    pass

            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_weights(data):
    with open(WEIGHTS_PATH, "w") as f:

    pass
      json.dump(data, f, indent=2)


def load_predictions():
    """Load our predictions store as a list of entries."""
    if not os.path.exists(PREDICTION_PATH):
        return []
    try:
    pass

    pass
      raw = json.load(open(PREDICTION_PATH))
    except Exception:
        return []
    # If someone wrote a dict-of-entries, convert to a list
    if isinstance(raw, dict):
        return list(raw.values())
    # If it’s already a list, use it
    if isinstance(raw, list):
        return raw
    # Fallback
    return []


def evaluate_prediction_accuracy():
    tokens = load_weights()
    checked = 0
    correct = 0
    for mint, t in tokens.items():
    pass

    pass
      log_series = t.get("price_log", [])
       if len(log_series) < 2 or "predicted_moon" not in t or t.get(
                "status") == "SCORED":
            continue
        prices = [p["price"] for p in log_series if p["price"] > 0]
        if len(prices) < 2:
            continue
        pct_change = (max(prices) - prices[0]) / prices[0] * 100
        actual_moon = pct_change >= 900  # 10x threshold

        predicted_moon = t.get("predicted_moon", False)
        t["prediction_correct"] = (actual_moon == predicted_moon)
        t["status"] = "SCORED"
        if t["prediction_correct"]:
            correct += 1
        checked += 1
    save_weights(tokens)
    log(f"[ACCURACY] Evaluated {checked} tokens, {correct} predictions correct.")


def loop():
    log("Prediction accuracy tracker online.")
    while True:
        evaluate_prediction_accuracy()
        time.sleep(180)  # every 3 minutes


if __name__ == "__main__":
    loop()
