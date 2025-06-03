import os
import sys
import json
import time
import argparse
from telethon import TelegramClient
from pathlib import Path
from common.config.telemetry_config import TELEMETRY_SETTINGS
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/../../"))
#!/usr/bin/env python3

# ——— Ensure “common/” is on sys.path ———
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


cfg = TELEMETRY_SETTINGS
# Example imports if you push errors or metrics:
# from common.metrics import load_latest_metrics

LOG_PATH = "common/logs/telemetry.log"
ERR_PATH = "common/logs/telemetry.err"


def main_loop(api_id, api_hash, bot_token, chat_id, interval_s):
    Path("common/logs").mkdir(parents=True, exist_ok=True)
    client = TelegramClient('telemetry_session', api_id,
                            api_hash).start(bot_token=bot_token)

    while True:
        # Example telemetry data: you might load metrics or accuracy from JSON
        msg = f"[TELEMETRY] {time.ctime()} System OK"
        client.send_message(chat_id, msg)


with open("common/logs/telemetry.log", "a") as fl:
    pass

with open("common/logs/telemetry.log", "a") as fl:
    fl.write(f"[{time.ctime()}] Sent telemetry: {msg}\n")
fe.write(f"[ERROR] {time.ctime()}: {repr(e)}\n")
time.sleep(interval_s)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default="common/config/telemetry_config.json",
        help="Path to telemetry_config.json")
    parser.add_argument("--interval", type=int, default=1800,
                        help="Seconds between telemetry pings")
    args = parser.parse_args()

    api_id = cfg["api_id"]
    api_hash = cfg["api_hash"]
    bot_token = cfg["bot_token"]
    chat_id = cfg["chat_id"]

    main_loop(api_id, api_hash, bot_token, chat_id, args.interval)
fe.write(f"[ERROR] {time.ctime()}: {repr(e)}\n")
