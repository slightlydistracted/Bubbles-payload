# /srv/daemon-memory/funpumper/fun_brain.py

import os
import json
import time
from datetime import datetime

WEIGHTS_PATH = "/srv/daemon-memory/funpumper/funpumper_weights.json"
BRAIN_LOG = "/srv/daemon-memory/funpumper/fun_brain.log"


def log(message):
    timestamp = datetime.utcnow().isoformat()
    with open(BRAIN_LOG, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


def load_weights():
    if not os.path.exists(WEIGHTS_PATH):
        return {}
    with open(WEIGHTS_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_weights(data):
    with open(WEIGHTS_PATH, "w") as f:
        json.dump(data, f, indent=2)


def simple_score(token):
    # Placeholder scoring logic
    age = token.get("age", 0)
    if age <= 0:
        return 0.0
    moon = token.get("predicted_moon", False)
    score = (1.0 if moon else 0.5) * min(age / 10000, 1.0)
    return round(score, 3)


def score_tokens():
    tokens = load_weights()
    count = 0
    for mint, token in tokens.items():
        if token.get("score", 0) > 0:
            continue
        token["score"] = simple_score(token)
        count += 1
        if count % 500 == 0:
            log(f"[UPDATE] {count} tokens scored so far...")
    log(f"[COMPLETE] Brain scored {count} tokens.")
    save_weights(tokens)


def get_top_suggestions(limit=10, max_age=43200):
    now = int(time.time())
    tokens = load_weights()
    filtered = [
        (mint, t) for mint, t in tokens.items()
        if t.get("score", 0) > 0 and now - t.get("mint_time", 0) <= max_age
    ]
    sorted_tokens = sorted(filtered, key=lambda x: x[1]["score"], reverse=True)
    return sorted_tokens[:limit]
