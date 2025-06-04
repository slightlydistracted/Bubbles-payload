
import json
import os

THRESHOLDS_PATH = os.path.expanduser("~/feralsys/tools/black_swan_agent/adaptive_thresholds.json")

DEFAULTS = {
    "buy_threshold": 0.02,
    "sell_threshold": 0.15,
    "loss_threshold": -0.10
}

def load_thresholds():
    if not os.path.exists(THRESHOLDS_PATH):
        return DEFAULTS.copy()
    with open(THRESHOLDS_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return DEFAULTS.copy()

def save_thresholds(thresholds):
    with open(THRESHOLDS_PATH, "w") as f:
        json.dump(thresholds, f, indent=2)

def adjust_thresholds(win_rate):
    thresholds = load_thresholds()
    if win_rate > 0.6:
        thresholds["buy_threshold"] = round(thresholds["buy_threshold"] * 1.01, 4)
        thresholds["sell_threshold"] = round(thresholds["sell_threshold"] * 1.02, 4)
    elif win_rate < 0.4:
        thresholds["buy_threshold"] = round(thresholds["buy_threshold"] * 0.99, 4)
        thresholds["sell_threshold"] = round(thresholds["sell_threshold"] * 0.98, 4)
    save_thresholds(thresholds)
    print(f"[THRESHOLDS ADJUSTED] New thresholds: {thresholds}")
    return thresholds
