import json
import os
from datetime import datetime

MEMORY_PATH = os.path.expanduser("~/feralsys/tools/black_swan_agent/mutation_memory.json")

def load_memory():
    if not os.path.exists(MEMORY_PATH):
        return {"mutations": [], "blacklist": []}
    with open(MEMORY_PATH, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {"mutations": [], "blacklist": []}

def evaluate_mutations(memory):
    mutations = memory.get("mutations", [])
    for m in mutations:
        if "timestamp" not in m:
            m["timestamp"] = "1970-01-01T00:00:00"
    sorted_mutations = sorted(mutations, key=lambda m: m["timestamp"])
    return sorted_mutations
