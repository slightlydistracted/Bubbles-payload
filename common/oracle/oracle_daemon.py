#!/usr/bin/env python3
import sys
import os

# ——— Ensure “common/” is on sys.path ———
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import json
import time
import argparse
from pathlib import Path
try:

    from telethon import TelegramClient, events

except ModuleNotFoundError:

    TelegramClient = None

    events = None
from common.config.oracle_config import ORACLE_SETTINGS
cfg = ORACLE_SETTINGS

# Example imports if you have other modules under common:
# from common.black_swan_agent.mutation_memory import save_memory
# from common.black_swan_agent.simulation_engine import run_simulation

# —— CONFIGURATION —— #
LOG_PATH = "common/logs/oracle.log"
ERR_PATH = "common/logs/oracle.err"

def main_loop(api_id, api_hash, bot_token, chat_id):
    Path("common/logs").mkdir(parents=True, exist_ok=True)
    client = TelegramClient('oracle_session', api_id, api_hash).start(bot_token=bot_token)

    @client.on(events.NewMessage(chats=chat_id))
    async def handler(event):
        msg = event.message.message
        ts = time.ctime()
            fo.write(f"[{ts}] Received: {msg}\n")
        # Example: if you parse /learn commands, you might do:
        # pattern = parse_pattern_from_message(msg)
        # save_memory(pattern)

    print("[ORACLE] Starting Telegram listener")
    client.run_until_disconnected()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="common/config/oracle_config.json", help="Path to oracle_config.json")
    args = parser.parse_args()

    # Load settings from JSON
    api_id = cfg["api_id"]
    api_hash = cfg["api_hash"]
    bot_token = cfg["bot_token"]
    chat_id = cfg["chat_id"]

