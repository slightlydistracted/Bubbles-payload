import json
from datetime import datetime
import os

MEMORY_PATH = "mutation_memory.json"

def load_memory():
    if not os.path.exists(MEMORY_PATH):
        save_memory({
            "mutations": [],
            "blacklist": [],
            "history": [],
            "meta": {
                "last_updated": datetime.utcnow().isoformat(),
                "error_log": [],
                "performance_log": [],
                "learning_notes": []
            }
        })
    with open(MEMORY_PATH, "r") as f:
        return json.load(f)

def save_memory(data):
    with open(MEMORY_PATH, "w") as f:
        json.dump(data, f, indent=4)

def log_mutation(mutation_name, metadata=None):
    memory = load_memory()
    mutation_entry = {
        "name": mutation_name,
        "timestamp": datetime.utcnow().isoformat(),
        "metadata": metadata or {},
        "score": None,
        "status": "active"
    }
    memory["mutations"].append(mutation_entry)
    save_memory(memory)

def retire_mutation(mutation_name):
    memory = load_memory()
    retained = []
    for m in memory["mutations"]:
        if m["name"] == mutation_name:
            m["status"] = "retired"
            memory["blacklist"].append(m)
        else:
            retained.append(m)
    memory["mutations"] = retained
    save_memory(memory)

def get_active_mutations():
    memory = load_memory()
    return [m for m in memory["mutations"] if m.get("status") != "retired"]

def record_performance(note):
    memory = load_memory()
    memory["meta"].setdefault("performance_log", []).append({
        "timestamp": datetime.utcnow().isoformat(),
        "note": note
    })
    save_memory(memory)

def record_learning_note(note):
    memory = load_memory()
    memory["meta"].setdefault("learning_notes", []).append({
        "timestamp": datetime.utcnow().isoformat(),
        "note": note
    })
    save_memory(memory)

def update_last_modified():
    memory = load_memory()
    memory["meta"]["last_updated"] = datetime.utcnow().isoformat()
    save_memory(memory)
