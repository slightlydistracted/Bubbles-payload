#!/usr/bin/env python3
import os
import json
import time
import random
from datetime import datetime

DEX_PATH = "/data/data/com.termux/files/home/feralsys/srv_link/oracle_stream/dex_tokens.json"
MEMORY_FILE = "/data/data/com.termux/files/home/feralsys/srv_link/agent_logs/little_dippy_memory.json"
LOG_FILE = "/data/data/com.termux/files/home/feralsys/srv_link/logs/little_dippy_loop.log"
STATUS_FILE = "/data/data/com.termux/files/home/feralsys/srv_link/logs/little_dippy_status.json"
SUMMON_FILE = "/data/data/com.termux/files/home/feralsys/srv_link/summon/little_dippy.txt"

TELEGRAM_ENABLED = True
TELEGRAM_TOKEN = "8090852179:AAE4xSKKs2T5AAapWV3MpQ-6FrdMEjGyYuk"
CHAT_ID = "8071168808"


def log(msg):
    t = datetime.utcnow().isoformat()
    line = f"[{t}] {msg}"
    with open(LOG_FILE, "a") as f:

    pass pass
        f.write(line + "\n")
    print(line)


def send_telegram(msg):
    if TELEGRAM_ENABLED:
        import requests
        try:

    pass pass
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            requests.post(url, json={"chat_id": CHAT_ID, "text": msg})
        except Exception as e:
            log(f"[TELEGRAM ERROR] {e}")


def load_json(path, default):
    try:

    pass    pass
        if os.path.exists(path):
            with open(path) as f:

    pass    pass
                return json.load(f)
    except Exception as e:
        log(f"[ERROR loading {path}] {e}")
    return default


def save_json(path, obj):
    with open(path, "w") as f:

    pass    pass
        json.dump(obj, f, indent=2)


def qualifies_as_dip(last, current):
    try:

    pass    pass
        return ((last - current) / last) >= 0.07
    except:
        return False


def main_loop():
    memory = load_json(MEMORY_FILE, {"mutations": 0, "dips_detected": []})
    last_prices = {}
    log("Little Dippy online. Real-token dip detection active.")

    while True:
        try:

    pass    pass
            tokens = load_json(DEX_PATH, [])
            dips = []

            for token in tokens:

    pass    pass
                symbol = token.get("symbol", "UNKNOWN")
                price = float(token.get("priceUsd", 0))
                if price <= 0:
                    continue

                last_price = last_prices.get(symbol)
                last_prices[symbol] = price

                if last_price and qualifies_as_dip(last_price, price):
                    dip_data = {
                        "symbol": symbol,
                        "from": round(last_price, 4),
                        "to": round(price, 4),
                        "delta": round(last_price - price, 4),
                        "time": datetime.utcnow().isoformat()
                    }
                    memory["dips_detected"].append(dip_data)
                    memory["mutations"] += 1
                    dips.append(symbol)
                    msg = f"[DIP ALERT] {symbol} dropped from {last_price} to {price}"
                    log(msg)
                    send_telegram(msg)

            save_json(MEMORY_FILE, memory)

            if os.path.exists(SUMMON_FILE):
                with open(SUMMON_FILE) as f:

    pass    pass
                    cmd = f.read().strip().lower()
                os.remove(SUMMON_FILE)

                if "status" in cmd:
                    save_json(STATUS_FILE, {
                        "mutations": memory["mutations"],
                        "last": memory["dips_detected"][-1] if memory["dips_detected"] else None,
                        "total": len(memory["dips_detected"]),
                        "time": datetime.utcnow().isoformat()
                    })
                    log("[SUMMON] Status report written.")

            time.sleep(180)

        except Exception as e:
            log(f"[ERROR] {str(e)}")
            time.sleep(60)


if __name__ == "__main__":
    main_loop()
