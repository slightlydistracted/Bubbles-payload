import sys
import os; sys.path.append(
    os.path.abspath(
        os.path.dirname(__file__) +
         "/../../"))
#!/usr/bin/env python3
import os
import json
import time
import random
import requests
from datetime import datetime

MEMORY_FILE = "/data/data/com.termux/files/home/feralsys/srv_link/agent_logs/winny_memory.json"
LOG_FILE = "/data/data/com.termux/files/home/feralsys/srv_link/logs/winny_loop.log"
STATUS_FILE = "/data/data/com.termux/files/home/feralsys/srv_link/logs/winny_status.json"
SUMMON_PATH = "/data/data/com.termux/files/home/feralsys/srv_link/summon/winny.txt"
THROCK_PATH = "/data/data/com.termux/files/home/feralsys/srv_link/throckmorton/throckmorton_adapter.json"
CLOCK_ORACLE = "/data/data/com.termux/files/home/feralsys/srv_link/clock_oracle.json"
DEX_FILE = "/data/data/com.termux/files/home/feralsys/srv_link/oracle_stream/dex_data.json"
HELIUS_FILE = "/data/data/com.termux/files/home/feralsys/srv_link/oracle_stream/helius_token_analysis.json"

TOKEN_LIMIT = 10
DEV_WALLET_CAP = 2
LIQUIDITY_MIN = 10000


def log(msg):
    t = datetime.utcnow().isoformat()
    line = f"[{t}] {msg}"
    with open(LOG_FILE, "a") as f:
    pass

        f.write(line + "\n")
    print(line)


def load_json(path, default):
    if not os.path.exists(path):
        return default
    try:

        with open(path) as f:
    pass

            return json.load(f)
    except BaseException:
        return default


def save_json(path, data):
    with open(path, "w") as f:

        json.dump(data, f, indent=2)


def load_tokens():
    data = load_json(DEX_FILE, [])
    return [t for t in data if isinstance(
        t, dict) and "mint" in t][:TOKEN_LIMIT]
    return []


def get_helius_info(mint):
    holders = load_json(HELIUS_FILE, {}).get(mint, {}).get("holders", [])
    return len(holders)


def is_safe(token, helius_count):
    reasons = []
    if token.get("lp_locked") is False:
        reasons.append("LP not locked")
    if token.get("honeypot") is True:
        reasons.append("Honeypot detected")
    if token.get("dev_wallets", 0) > DEV_WALLET_CAP:
        reasons.append("Too many dev wallets")
    if helius_count == 0:
        reasons.append("No holder data")
    return reasons


def main_loop():
    memory = load_json(MEMORY_FILE, {"scans": [], "mutations": 0})
    log("Winny online. Full sentinel mode engaged.")

    while True:
        try:

            tokens = load_tokens()
            if not tokens:
                log("[WARN] No tokens available from oracle.")
                time.sleep(60)
                continue

            safe_count = 0
            for t in tokens:
    pass

                mint = t.get("mint", "unknown")
                helius_count = get_helius_info(mint)
                reasons = is_safe(t, helius_count)
                report = f"{t.get('symbol', '???')} | ${t.get('price')} | LP ${t.get('lp')} | Dex: {t.get('dex')} | Mint: {mint} | TS: {datetime.utcnow().isoformat()}"
    pass

                if reasons and not all(r == "No holder data" for r in reasons):
    pass

                    log(f"FLAGGED: {report} | REASON: {' + '.join(reasons)}")
                else:
                    log(f"SAFE: {report}")

                memory["scans"].append(t)
                safe_count += 1

            memory["mutations"] += 1
            save_json(MEMORY_FILE, memory)
            log(f"[SCAN COMPLETE] {len(tokens)} checked | {safe_count} marked safe.")
            time.sleep(120)
        except Exception as e:
            log(f"[ERROR] {e}")
            time.sleep(60)


if __name__ == "__main__":
    main_loop()
