#!/usr/bin/env python3
import argparse
import json
import time
from datetime import datetime
from telethon import TelegramClient, events

# Path to the JSON file of learned patterns
LEARNED_PATTERNS = "common/oracle/learned_patterns.json"
WALLET_SIGS = "common/oracle/wallet_last_sigs.json"
ORACLE_OUTPUT = "common/oracle/oracle_output.json"

def load_config(path):
    try:
        return json.load(open(path))
    except:
        return {
            "api_id": 123456,
            "api_hash": "your_api_hash",
            "bot_token": "your_bot_token",
            "chat_id": "your_chat_id"
        }

def run_oracle(config_path):
    cfg = load_config(config_path)
    client = TelegramClient('oracle_session', cfg["api_id"], cfg["api_hash"])

    @client.on(events.NewMessage(chats=cfg["chat_id"]))
    async def handler(event):
        text = event.raw_text
        print(f"[ORACLE] Received: {text}")
        # Dummy: write a new pattern when a message contains “learn”
        if text.lower().startswith("/learn"):
            parts = text.split()
            pattern = parts[1] if len(parts) > 1 else "default"
            entry = {
                "pattern": pattern,
                "timestamp": datetime.utcnow().isoformat()
            }
            try:
                patterns = json.load(open(LEARNED_PATTERNS))
            except:
                patterns = []
            patterns.append(entry)
            with open(LEARNED_PATTERNS, "w") as f:
                json.dump(patterns, f, indent=2)
            print(f"[ORACLE] Learned new pattern: {pattern}")
            with open(ORACLE_OUTPUT, "w") as f:
                json.dump({"new_pattern": pattern}, f, indent=2)

    client.start(bot_token=cfg["bot_token"])
    print("[ORACLE] Telegram client started, listening for messages...")
    client.run_until_disconnected()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="common/config/oracle_config.json")
    args = parser.parse_args()
    run_oracle(args.config)
