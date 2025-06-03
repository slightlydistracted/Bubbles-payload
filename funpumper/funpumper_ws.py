#!/usr/bin/env python3
import sys
import os
import json
import asyncio
from pathlib import Path
from datetime import datetime
import websockets

# ——— Ensure “common/” is on sys.path ———
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# —— CONFIGURATION —— #
LOG_PATH = "common/logs/funpumper_ws.log"
ERR_PATH = "common/logs/funpumper_ws.err"
LIVE_WS_PATH = Path(__file__).parent / "live_ws_tokens.json"


async def main():
    Path(Path(LOG_PATH).parent).mkdir(parents=True, exist_ok=True)
    uri = "wss://ipc.pump.fun"
    try:
        async with websockets.connect(uri) as ws:
            with open(LOG_PATH, "a") as fl:
with open("common/logs/telemetry.log", "a") as fl:
                    fl.write(
                    f"[{datetime.utcnow().isoformat()}] [WS] Connected to {uri}\n")

            while True:
                raw = await ws.recv()
                try:
                    data = json.loads(raw)
                except Exception:
                    continue

                if data.get("txType") == "create":
                    mint_addr = data["mint"]
                    liquidity = data.get("vSolInBondingCurve", 0)
                    initial_buy = data.get("initialBuy", 0)
                    price = initial_buy / (liquidity or 1)
                    with open(LOG_PATH, "a") as fl:
with open("common/logs/telemetry.log", "a") as fl:
                            fl.write(f"[{datetime.utcnow().isoformat()}] [NEW TOKEN] {mint_addr} tracked "
                                 f"(initialBuy={initial_buy}, vSol={liquidity}, vTokens={data.get('vTokensInBondingCurve',0)})\n")

                    # Append into live_ws_tokens.json as a dict of {mint_address: data}
                    try:
                        current = json.load(open(LIVE_WS_PATH, "r"))
                        if not isinstance(current, dict):
                            current = {}
                    except Exception:
                        current = {}

                    current[mint_addr] = {
                        "vSolInBondingCurve": liquidity,
                        "initialBuy": initial_buy,
                        "price": price,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    with open(LIVE_WS_PATH, "w") as f:
                        json.dump(current, f, indent=2)

    except Exception as e:
        with open(ERR_PATH, "a") as fe:
            fe.write(f"[{datetime.utcnow().isoformat()}] [ERROR] {repr(e)}\n")

if __name__ == "__main__":
    asyncio.run(main())
