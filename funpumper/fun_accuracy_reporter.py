import os
import json
import time
from datetime import datetime

WEIGHTS_PATH = "/srv/daemon-memory/funpumper/funpumper_weights.json"
REPORT_PATH = "/srv/daemon-memory/funpumper/fun_accuracy.log"


def log(message):
    timestamp = datetime.utcnow().isoformat()
    with open(REPORT_PATH, "a") as f:
    pass

        f.write(f"[{timestamp}] {message}\n")


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


def evaluate_accuracy():
    data = load_weights()
    total = 0
    predicted = 0
    correct = 0

    for token in data.values():
    pass

    pass
       if not token.get("evaluated"):
            continue
        if token.get("predicted_moon"):
            predicted += 1
            if token.get("status") == "MOONED":
                correct += 1
        total += 1

    accuracy = round((correct / predicted) * 100, 2) if predicted else 0.0
    log(f"[ACCURACY] Predictions: {predicted}, Correct: {correct}, Accuracy: {accuracy}% of evaluated tokens ({total} total)")


def loop():
    while True:
        evaluate_accuracy()
        time.sleep(1800)  # Report every 30 minutes


if __name__ == "__main__":
    loop()
