
import json
import os

VALUE_DB_PATH = os.path.expanduser("~/feralsys/tools/black_swan_agent/token_values.json")

def decode_token_value(token_address):
    if not os.path.exists(VALUE_DB_PATH):
        return 0.0  # Default fallback value
    try:
        with open(VALUE_DB_PATH, "r") as f:
            data = json.load(f)
        return data.get(token_address, 0.0)
    except json.JSONDecodeError:
        return 0.0
