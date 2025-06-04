
import json
import os

MEMORY_PATH = os.path.expanduser("~/feralsys/tools/black_swan_agent/mutation_memory.json")
ALPHA_PATH = os.path.expanduser("~/feralsys/tools/black_swan_agent/alpha_signals.json")

def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return fallback

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def reinforce_alpha_signals():
    memory = load_json(MEMORY_PATH, {"mutations": [], "history": [], "blacklist": []})
    alpha_data = load_json(ALPHA_PATH, {"alpha_signals": []})

    signal_counts = {}
    for signal in alpha_data.get("alpha_signals", []):
        addr = signal.get("token_address")
        if addr:
            signal_counts[addr] = signal_counts.get(addr, 0) + 1

    if not signal_counts:
        print("[Reinforcement] No alpha signals to reinforce.")
        return

    # Adjust weights or priority in memory
    updated = False
    for mutation in memory.get("mutations", []):
        addr = mutation.get("token_address")
        if addr in signal_counts:
            old_score = mutation.get("confidence_score", 1.0)
            multiplier = 1 + 0.05 * signal_counts[addr]  # 5% boost per occurrence
            mutation["confidence_score"] = round(old_score * multiplier, 4)
            updated = True

    if updated:
        print("[Reinforcement] Alpha signal reinforcement complete.")
        save_json(MEMORY_PATH, memory)
    else:
        print("[Reinforcement] No matching entries found in memory to reinforce.")

if __name__ == "__main__":
    reinforce_alpha_signals()
