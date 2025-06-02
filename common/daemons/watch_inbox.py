#!/usr/bin/env python3
import os
import time
import json

# Configuration: which folder to watch
CONFIG_PATH = "common/config/inbox_config.json"
DEFAULT_INBOX = os.path.expanduser("~/feralsys/inbox")

def load_config():
    try:
        cfg = json.load(open(CONFIG_PATH))
        return cfg.get("inbox_folder", DEFAULT_INBOX)
    except FileNotFoundError:
        return DEFAULT_INBOX

def fetch_next_message():
    inbox = load_config()
    processed_folder = os.path.join(inbox, "processed")
    os.makedirs(processed_folder, exist_ok=True)

    # Poll every 10 seconds
    while True:
        for fname in os.listdir(inbox):
            fpath = os.path.join(inbox, fname)
            if os.path.isfile(fpath) and fname.endswith(".json"):
                try:
                    msg = json.load(open(fpath))
                    # Move to processed
                    os.rename(fpath, os.path.join(processed_folder, fname))
                    return msg
                except json.JSONDecodeError:
                    os.remove(fpath)
        time.sleep(10)

if __name__ == "__main__":
    # Example usage: continuously print messages
    while True:
        msg = fetch_next_message()
        print(f"[INBOX] Received: {msg}")
