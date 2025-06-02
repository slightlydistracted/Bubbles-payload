
import os
import json
from datetime import datetime

OUTPUT_PATH = os.path.expanduser("~/blind_reboot_process.json")
LOG_PATH = os.path.expanduser("~/execution_log.json")
ROOT_PATH = os.path.expanduser("~/")

def describe(path):
    if os.path.isdir(path):
        return "directory"
    elif os.path.isfile(path):
        return "file"
    else:
        return "unknown"

def generate_map(root):
    fs_map = {}
    for dirpath, dirnames, filenames in os.walk(root):
        for name in dirnames + filenames:
            full_path = os.path.join(dirpath, name)
            rel_path = os.path.relpath(full_path, root)
            fs_map[rel_path] = describe(full_path)
    return fs_map

def write_output(data):
    with open(OUTPUT_PATH, "w") as f:
        json.dump(data, f, indent=2)

def log_execution():
    timestamp = datetime.utcnow().isoformat()
    entry = {"script": "termux_map_daemon.py", "status": "success", "timestamp": timestamp}
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            logs = json.load(f)
    else:
        logs = []
    logs.append(entry)
    with open(LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)

if __name__ == "__main__":
    try:
        fs_map = generate_map(ROOT_PATH)
        write_output(fs_map)
        log_execution()
        print(f"[âœ“] Termux map generated: {OUTPUT_PATH}")
    except Exception as e:
        print(f"[!] Error: {str(e)}")
