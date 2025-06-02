#!/usr/bin/env python3
import json
import os

MEMORY_PATH = "common/black_swan_agent/mutation_memory.json"

def load_memory():
    os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)
    try:
        return json.load(open(MEMORY_PATH))
    except:
        return {"mutations": []}

def save_memory(memory):
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)
