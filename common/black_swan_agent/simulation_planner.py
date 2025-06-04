import json
import os
from datetime import datetime
from mutation_memory import load_memory

SIMULATION_LOG = os.path.expanduser("~/feralsys/tools/black_swan_agent/reports/simulation_log.json")


def load_simulation_log():
    if os.path.exists(SIMULATION_LOG):
        with open(SIMULATION_LOG, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def save_simulation_log(log):
    with open(SIMULATION_LOG, 'w') as f:
        json.dump(log, f, indent=2)


def simulate_run(memory, portfolio_value_snapshot):
    """Perform a dry-run forward simulation using past mutation data."""
    timestamp = datetime.utcnow().isoformat()
    mutations = memory.get("mutations", [])
    simulation_result = {
        "timestamp": timestamp,
        "initial_value": portfolio_value_snapshot,
        "mutation_count": len(mutations),
        "score": 0.0,
        "notes": []
    }

    for mutation in mutations:
        score = mutation.get("performance_score", 0)
        simulation_result["score"] += score
        if score < 0:
            simulation_result["notes"].append(f"Weak mutation: {mutation.get('description', '')}")

    simulation_result["score"] = round(simulation_result["score"], 4)

    log = load_simulation_log()
    log.append(simulation_result)
    save_simulation_log(log)

    print(f"[SIMULATION PLANNER] Simulated score: {simulation_result['score']} (mutations: {len(mutations)})")
    return simulation_result
