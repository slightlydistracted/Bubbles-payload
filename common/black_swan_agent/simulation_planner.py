#!/usr/bin/env python3
import json
import time
from datetime import datetime
from common.black_swan_agent.mutation_memory import load_memory, save_memory

SIM_LOG = "common/black_swan_agent/simulation_log.json"
PORTFOLIO_SNAPSHOT = "common/black_swan_agent/portfolio_snapshot.json"

def load_simulation_log():
    try:
        return json.load(open(SIM_LOG))
    except:
        return []

def save_simulation_log(log):
    with open(SIM_LOG, "w") as f:
        json.dump(log, f, indent=2)

def get_portfolio_value():
    try:
        return json.load(open(PORTFOLIO_SNAPSHOT))["value"]
    except:
        return 100.0  # default simulated value

def simulate_run(memory, portfolio_value):
    score = 0.0
    # Simple simulation: each “mutation” grants +0.1 ROI
    for m in memory.get("mutations", []):
        if m["phase"] == 3 and m["outcome"] == "6x":
            score += 0.1
    new_value = portfolio_value * (1 + score)
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "initial_value": portfolio_value,
        "final_value": new_value,
        "score": score
    }
    log = load_simulation_log()
    log.append(entry)
    save_simulation_log(log)
    # Update portfolio snapshot
    with open(PORTFOLIO_SNAPSHOT, "w") as f:
        json.dump({"value": new_value}, f)
    print(f"[SIM] Ran simulation: {entry}")
    return entry

if __name__ == "__main__":
    memory = load_memory()
    current_val = get_portfolio_value()
    simulate_run(memory, current_val)
