#!/usr/bin/env python3
import os
import json
import asyncio
import websockets
import time
from datetime import datetime

#
# funpumper_ws.py
#
# Listens to PumpPortal’s WebSocket feed and writes out one JSON entry per mint:
#    {
#      "mint_time": 1700000000,
#      "initialBuy": 50000000,
#      "vSolInBondingCurve": 32.0,
#      "vTokensInBondingCurve": 1000000000,
#      "traderPublicKey": "...",
#      "raw": { ...full original WS payload... }
#    }
#
# into live_ws_tokens.json.  Phase 1’s purifier/predictor will pick up these fields
# (especially vSolInBondingCurve / vTokensInBondingCurve) to compute price_in_sol, etc.
#

PUMP_WS_URL = "wss://pumpportal.fun/api/data"
LOG_PATH    = "/srv/daemon-memory/funpumper/funpumper_ws.log"
DATA_OUT    = "/srv/daemon-memory/funpumper/live_ws_tokens.json"
TMP_OUT     = DATA_OUT + ".tmp"

# In‐memory cache for “live” tokens; on every new mint we write to disk atomically.
live_tokens = {}

def log(msg: str):
    ts = datetime.utcnow().isoformat()
    line = f"[{ts}] {msg}"
    # append to logfile
    with open(LOG_PATH, "a") as f:
        f.write(line + "\n")
    # also print to stdout (so `tail -f` shows it)
    print(line)


def atomic_write(data: dict, path: str, tmp_path: str):
    """
    Write JSON to tmp_path then rename → path.  This prevents partial writes.
    """
    with open(tmp_path, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp_path, path)


async def subscribe(ws, method: str):
    """
    Send subscription message over WebSocket.
    """
    msg = {"method": method}
    await ws.send(json.dumps(msg))
    log(f"[SUBSCRIBED] {method}")


async def handle_messages():
    """
    Connect to the PumpPortal WS, subscribe to new‐token events, and record each mint.
    """
    # (Re)connect loop
    async with websockets.connect(PUMP_WS_URL) as ws:
        await subscribe(ws, "subscribeNewToken")
        while True:
            try:
                raw = await ws.recv()
                msg = json.loads(raw)
                log(f"[RAW] {msg}")

                # If the WS payload has a "mint" key, it’s a new‐token event.
                if "mint" in msg:
                    mint = msg["mint"]

                    # If we’ve already recorded this mint, skip.
                    if mint in live_tokens:
                        continue

                    # Extract timestamp and bonding‐curve data:
                    now = int(time.time())

                    initial_buy = msg.get("initialBuy", None)
                    v_sol       = msg.get("vSolInBondingCurve", None)
                    v_tokens    = msg.get("vTokensInBondingCurve", None)
                    trader_key  = msg.get("traderPublicKey", None)

                    # Build our stored record for this mint:
                    record = {
                        "mint_time": now,
                        "initialBuy": initial_buy,
                        "vSolInBondingCurve": v_sol,
                        "vTokensInBondingCurve": v_tokens,
                        "traderPublicKey": trader_key,
                        # Keep the entire raw WS payload in case we need other fields later:
                        "raw": msg
                    }

                    live_tokens[mint] = record

                    # Atomically write the entire live_tokens dict out to disk:
                    atomic_write(live_tokens, DATA_OUT, TMP_OUT)
                    log(f"[NEW TOKEN] {mint} tracked (initialBuy={initial_buy}, vSol={v_sol}, vTokens={v_tokens})")

            except Exception as e:
                log(f"[WS ERROR] {e}")
                # Wait a moment before trying again
                await asyncio.sleep(5)


def run_ws_client():
    log("FunPumper WebSocket Listener Active.")
    asyncio.run(handle_messages())


if __name__ == "__main__":
    run_ws_client()
