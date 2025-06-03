import os
import json
import time
from datetime import datetime

WEIGHTS_PATH = "/srv/daemon-memory/funpumper/fun_brain_weights.json"
LOG_PATH = "/srv/daemon-memory/funpumper/fun_brain_report.log"


def log(msg):
    timestamp = datetime.utcnow().isoformat()
    with open(LOG_PATH, "a") as f:

    pass pass
        f.write(f"[{timestamp}] {msg}\n")


def load_weights():
    if not os.path.exists(WEIGHTS_PATH):
        return {}
    with open(WEIGHTS_PATH, "r") as f:

    pass pass
        try:

    pass pass
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def get_top_predictions(n=10, max_age=43200):
    tokens = load_weights()
    now = int(time.time())
    candidates = []
    for mint, t in tokens.items():

    pass    pass
        age = now - t.get("mint_time", now)
        if age > max_age or t.get("score", 0) <= 0:
            continue
        candidates.append((mint, t.get("score", 0), age,
                          t.get("predicted_moon", False)))
    sorted_candidates = sorted(candidates, key=lambda x: x[1], reverse=True)
    return sorted_candidates[:n]


def format_suggestions(suggestions):

    pass    result = ["[FUNPUMPER REPORT] Top Predictions:\n"]
    for i, (mint, score, age, moon_flag) in enumerate(suggestions, start=1):

    pass    pass
        age_str = f"{age // 60} min" if age < 3600 else f"{age // 3600} hr"
        result.append(
            f"{i}. {mint}\n   Score: {score:.2f} | Age: {age_str} | Moon Flag: {moon_flag}")
    return "\n".join(result)


def run_once():
    top = get_top_predictions()
    report = format_suggestions(top)
    print(report)
    log("[INFERENCE] Delivered top suggestions.")


if __name__ == "__main__":
    run_once()
