import sys
import os; sys.path.append(
    os.path.abspath(
        os.path.dirname(__file__) +
         "/../../"))
import os
import json
import time
from datetime import datetime

# Assumes you already have this module built
from funpumper.helius_utils import get_token_price

WEIGHTS_PATH = "/srv/daemon-memory/funpumper/fun_brain_weights.json"
LOG_PATH = "/srv/daemon-memory/funpumper/token_history.log"


def log(msg):
    timestamp = datetime.utcnow().isoformat()
    with open(LOG_PATH, "a") as f:
    pass

        f.write(f"[{timestamp}] {msg}\n")


def load_weights():
    if not os.path.exists(WEIGHTS_PATH):
        return {}
    with open(WEIGHTS_PATH, "r") as f:
    pass

        try:
    pass

            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_weights(data):
    with open(WEIGHTS_PATH, "w") as f:

    pass
        json.dump(data, f, indent=2)


def update_price_logs():
    tokens = load_weights()
    updated = 0
    for mint, t in tokens.items():
    pass

    pass
        try:
    pass

    pass
            price = get_token_price(mint)
            t.setdefault("price_log", []).append({
                "timestamp": int(time.time()),
                "price": price
            })
            updated += 1
        except Exception as e:
            log(f"[ERROR] Failed to get price for {mint}: {e}")
    save_weights(tokens)
    log(f"[PRICE LOGGED] {updated} tokens updated.")


def loop():
    log("Token history logger activated.")
    while True:
        update_price_logs()
        time.sleep(120)  # Update every 2 minutes


if __name__ == "__main__":
    loop()
