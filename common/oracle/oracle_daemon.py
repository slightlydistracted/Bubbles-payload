#!/usr/bin/env python3

import requests, json, time, os, shutil
from datetime import datetime

OUTFILE = "/data/data/com.termux/files/home/feralsys/shadow_srv/daemon-memory/oracle_stream/dex_data.json"
BACKUPFILE = "/data/data/com.termux/files/home/feralsys/shadow_srv/daemon-memory/oracle_stream/dex_data_backup.json"
LOGFILE = "/data/data/com.termux/files/home/feralsys/shadow_srv/daemon-memory/oracle_stream/oracle.log"
HEARTBEAT = "/data/data/com.termux/files/home/feralsys/shadow_srv/daemon-memory/oracle_heartbeat.txt"
DEXSCREENER_URL = "https://api.dexscreener.com/latest/dex/search/?q=sol"

os.makedirs("/data/data/com.termux/files/home/feralsys/shadow_srv/daemon-memory/oracle_stream", exist_ok=True)

def log(msg):
    timestamp = datetime.utcnow().isoformat()
    with open(LOGFILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(f"[{timestamp}] {msg}")

def write_heartbeat():
    with open(HEARTBEAT, "w") as f:
        f.write(str(int(time.time())))

def fetch_dex_tokens():
    try:
        res = requests.get(DEXSCREENER_URL, timeout=10)
        res.raise_for_status()
        data = res.json()
        pairs = data.get("pairs", [])
        tokens = []

        for p in pairs[:25]:
            token = {
                "symbol": p.get("baseToken", {}).get("symbol", "???"),
                "lp": float(p.get("liquidity", {}).get("usd", 0)),
                "price": float(p.get("priceUsd", 0)),
                "mint": p.get("baseToken", {}).get("address", "???"),
                "dex": p.get("dexId", "???"),
                "fetched_at": datetime.utcnow().isoformat()
            }
            tokens.append(token)

        if os.path.exists(OUTFILE):
            shutil.copyfile(OUTFILE, BACKUPFILE)

        with open(OUTFILE, "w") as f:
            json.dump(tokens, f, indent=2)

        log(f"[DEX] Wrote {len(tokens)} tokens to dex_data.json")
    except requests.exceptions.Timeout:
        log("[DEX ERROR] Timeout occurred while fetching DEX data")
    except requests.exceptions.RequestException as e:
        log(f"[DEX ERROR] Request exception: {e}")
    except Exception as e:
        log(f"[DEX ERROR] General exception: {e}")

def loop():
    log("Dex oracle daemon online.")
    while True:
        fetch_dex_tokens()
        write_heartbeat()
        time.sleep(300)

if __name__ == "__main__":
    loop()
