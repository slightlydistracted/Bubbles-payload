#!/usr/bin/env python3
from common.black_swan_agent.mutation_memory import load_memory, save_memory
import sys
import os
from pathlib import Path
import json
import time
import requests
from datetime import datetime

# ——— Ensure “common/” is on sys.path ———
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


# —— CONFIGURATION —— #
LOG_PATH = "funpumper/fun_purger_loop.log"
ERR_PATH = "common/logs/fun_purger.err"

# Change LIVE_WS_PATH to point to funpumper/live_ws_tokens.json
LIVE_WS_PATH = Path(__file__).parent / "live_ws_tokens.json"
FILTERED_PATH = Path(__file__).parent / "fun_filtered.json"
DEADLIST_PATH = Path(__file__).parent / "fun_deadlist.json"

# Phase 1 filter thresholds
MIN_LIQUIDITY = 10  # example value
MIN_INITIAL_BUY = 1  # example value


def load_json(path: Path, default):
    try:
        return json.load(open(path, "r"))
    except FileNotFoundError:
        return default
    except json.JSONDecodeError:
        return default


def save_json(path: Path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def fetch_price_for_token(token_address):
    # Placeholder for actual price lookup. Replace with real API if needed.
    # Example: Helius or Serum API call
    try:
        resp = requests.get(f"https://api.example.com/price/{token_address}")
        return float(resp.json().get("price", 0))
    except Exception:
        return 0


def loop():
    Path("funpumper").mkdir(parents=True, exist_ok=True)
    Path("common/logs").mkdir(parents=True, exist_ok=True)

    while True:
        try:
            # 1) Load the WS‐populated dictionary (address → data dict)
            live_ws: dict = load_json(LIVE_WS_PATH, {})

            # 2) Load and index which addresses have already been processed
            if FILTERED_PATH.exists():
                filtered_list = load_json(FILTERED_PATH, [])
                filtered_addresses = {item["address"]
                                      for item in filtered_list}
            else:
                filtered_list = []
                filtered_addresses = set()

            if DEADLIST_PATH.exists():
                deadlist = load_json(DEADLIST_PATH, [])
                dead_addresses = set(deadlist)
            else:
                deadlist = []
                dead_addresses = set()

            # 3) Iterate over all mint entries in live_ws
            for mint_addr, msg in live_ws.items():
                if mint_addr in filtered_addresses or mint_addr in dead_addresses:
                    continue

                # Extract relevant data from msg (msg is a dict from funpumper_ws.py)
                liquidity = msg.get("vSolInBondingCurve", 0)
                initial_buy = msg.get("initialBuy", 0)
                if liquidity < MIN_LIQUIDITY or initial_buy < MIN_INITIAL_BUY:
                    deadlist.append(mint_addr)
                    print(
                        f"[PURGER] Rejecting {mint_addr} (liquidity={liquidity}, initial_buy={initial_buy})")
                else:
                    price = initial_buy / (liquidity or 1)
                    record = {
                        "address": mint_addr,
                        "liquidity": liquidity,
                        "price": price,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    filtered_list.append(record)
                    filtered_addresses.add(mint_addr)
                    print(
                        f"[PURGER] Accepting {mint_addr} (liquidity={liquidity}, price={price:.6f})")

                # Write updates immediately
                save_json(FILTERED_PATH, filtered_list)
                save_json(DEADLIST_PATH, deadlist)

            # 4) Sleep briefly before re‐checking
        except Exception as e:
            with open(ERR_PATH, "a") as fe:
                fe.write(
                    f"[{datetime.utcnow().isoformat()}] [ERROR] {repr(e)}\n")
        time.sleep(1)


if __name__ == "__main__":
    loop()
