
import json
import os
from datetime import datetime

LEARNED_PATTERNS_PATH = "learned_patterns.json"

def load_patterns():
    if not os.path.exists(LEARNED_PATTERNS_PATH):
        return {"patterns": [], "log": []}
    with open(LEARNED_PATTERNS_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"patterns": [], "log": []}

def save_patterns(data):
    with open(LEARNED_PATTERNS_PATH, "w") as f:
        json.dump(data, f, indent=2)

def log_pattern(pattern, description, outcome_score):
    data = load_patterns()
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "pattern": pattern,
        "description": description,
        "outcome_score": outcome_score
    }
    data["patterns"].append(entry)
    save_patterns(data)
    return entry
