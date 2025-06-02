import os
import json
import time
from datetime import datetime

WEIGHTS_PATH = "/srv/daemon-memory/funpumper/funpumper_weights.json"
EVOLUTION_LOG = "/srv/daemon-memory/funpumper/fun_brain_evolution.log"
PROFILE_PATH = "/srv/daemon-memory/funpumper/fun_scoring_profile.json"

def log(message):
    timestamp = datetime.utcnow().isoformat()
    with open(EVOLUTION_LOG, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def load_weights():
    if not os.path.exists(WEIGHTS_PATH):
        return {}
    with open(WEIGHTS_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_profile(profile):
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f, indent=2)

def reflect_and_mutate():
    tokens = load_weights()
    score_buckets = {
        "0-0.2": {"pred": 0, "hit": 0},
        "0.2-0.4": {"pred": 0, "hit": 0},
        "0.4-0.6": {"pred": 0, "hit": 0},
        "0.6-0.8": {"pred": 0, "hit": 0},
        "0.8-1.0": {"pred": 0, "hit": 0}
    }

    for mint, t in tokens.items():
        if not t.get("predicted_moon") or "actual_moon" not in t:
            continue
        score = float(t.get("score", 0))
        if score < 0.2:
            b = "0-0.2"
        elif score < 0.4:
            b = "0.2-0.4"
        elif score < 0.6:
            b = "0.4-0.6"
        elif score < 0.8:
            b = "0.6-0.8"
        else:
            b = "0.8-1.0"
        score_buckets[b]["pred"] += 1
        if t["actual_moon"]:
            score_buckets[b]["hit"] += 1

    best_bucket = max(score_buckets.items(), key=lambda x: x[1]["hit"] / x[1]["pred"] if x[1]["pred"] else 0)
    best_range, best_stats = best_bucket
    accuracy = best_stats["hit"] / best_stats["pred"] if best_stats["pred"] else 0

    log(f"Reflection complete. Best score range: {best_range} with accuracy: {accuracy:.2%}")

    new_profile = {
        "last_best_score_range": best_range,
        "last_accuracy": accuracy,
        "last_reflection": datetime.utcnow().isoformat()
    }

    save_profile(new_profile)

def loop():
    while True:
        reflect_and_mutate()
        time.sleep(3600)  # Reflect once per hour

if __name__ == "__main__":
    loop()
