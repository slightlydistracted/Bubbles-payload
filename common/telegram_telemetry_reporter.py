#!/usr/bin/env python3
import argparse
import json
import time
from telethon import TelegramClient

LOG_PATH = "common/logs/telemetry_sent.log"
CONFIG_PATH = "common/config/telemetry_config.json"

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

def send_telemetry(cfg):
    client = TelegramClient('telemetry_session', cfg["api_id"], cfg["api_hash"])
    client.start(bot_token=cfg["bot_token"])
    message = f"Heartbeat: {time.strftime('%Y-%m-%d %H:%M:%S')}"
    client.send_message(cfg["chat_id"], message)
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps({"timestamp": time.time(), "message": message}) + "\n")
    print(f"[TELEMETRY] Sent: {message}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=CONFIG_PATH)
    args = parser.parse_args()
    cfg = load_config(args.config)
    while True:
        send_telemetry(cfg)
        time.sleep(3600)  # every hour
