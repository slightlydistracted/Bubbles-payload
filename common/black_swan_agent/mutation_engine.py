import random
import json
from datetime import datetime

MUTATION_MEMORY_PATH = "mutation_memory.json"

def load_mutation_memory():
    try:
        with open(MUTATION_MEMORY_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"history": [], "current": None}

def save_mutation_memory(data):
    with open(MUTATION_MEMORY_PATH, "w") as f:
        json.dump(data, f, indent=2)

# Define your base mutation rules
AVAILABLE_MUTATIONS = [
    "increase_buy_aggression",
    "decrease_sell_threshold",
    "randomize_entry_points",
    "follow_whale_wallets",
    "react_to_social_volume",
    "early_exit_on_dip",
    "volatility_based_position_sizing",
    "ignore_low_liquidity",
    "prefer_new_tokens",
    "simulate_trend_following",
    "simulate_mean_reversion",
    "track_hype_decay",
    "inverse_rugpull_sensitivity",
    "echo_successful_wallets",
]

def select_two_mutations(previously_used):
    choices = [m for m in AVAILABLE_MUTATIONS if m not in previously_used[-6:]]
    selected = random.sample(choices, 2) if len(choices) >= 2 else random.sample(AVAILABLE_MUTATIONS, 2)
    return selected

def apply_mutations():
    memory = load_mutation_memory()

    today = datetime.utcnow().date().isoformat()
    previous = memory.get("history", [])

    # Only mutate if we haven't today
    if previous and previous[-1]["date"] == today:
        return previous[-1]["mutations"]

    selected = select_two_mutations([x["mutations"][0] for x in previous[-6:]] + [x["mutations"][1] for x in previous[-6:]])

    memory["history"].append({
        "date": today,
        "mutations": selected
    })
    memory["current"] = selected
    save_mutation_memory(memory)

    return selected
