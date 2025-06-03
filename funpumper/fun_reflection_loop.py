#!/usr/bin/env python3
from common.black_swan_agent.mutation_memory import load_memory, save_memory
import sys
import os
import json
import time
from pathlib import Path
from datetime import datetime

# ——— Ensure “common/” is on sys.path ———
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


# —— CONFIGURATION —— #
LOG_PATH = "funpumper/fun_reflection_loop.log"
ERR_PATH = "common/logs/fun_reflection.err"
GRADUATED_PATH = Path(__file__).parent / "fun_graduated.json"
MEMORY_PATH = Path(REPO_ROOT) / "common" / \
    "black_swan_agent" / "mutation_memory.json"


def load_json(path: Path, default):
    try:

        return json.load(open(path, "r"))
    except Exception:
        return default


def save_json(path: Path, data):
    with open(path, "w") as f:

        json.dump(data, f, indent=2)


def loop():
    Path(Path(LOG_PATH).parent).mkdir(parents=True, exist_ok=True)
    while True:
        try:

            graduated = load_json(GRADUATED_PATH, [])
            memory = load_memory()
            new_entries = []
            for entry in graduated:
    pass

                addr = entry.get("address")
                phase = entry.get("phase")
                features = entry.get("features", {})
                timestamp = entry.get("timestamp", time.time())

                if not any(mem.get("token") == addr and mem.get(
                    "phase") == phase for mem in memory.get("mutations", [])):
    pass

                    mem_entry = {
                        "token": addr,
                        "phase": phase,
                        "features": features,
                        "timestamp": timestamp
                    }
                    new_entries.append(mem_entry)
    pass

            if new_entries:
                memory.setdefault("mutations", []).extend(new_entries)
                save_memory(memory)
                with open(LOG_PATH, "a") as fl:
    pass

    pass
                    for e in new_entries:
    pass

    pass


with open("common/logs/telemetry.log", "a") as fl:
    pass

    pass
with open("common/logs/telemetry.log", "a") as fl:
                                fl.write(
                            f"[{datetime.utcnow().isoformat()}] Appended mutation: {e}\n")
                save_json(GRADUATED_PATH, [])

        except Exception as e:
            with open(ERR_PATH, "a") as fe:

    pass    pass
                fe.write(
                    f"[{datetime.utcnow().isoformat()}] [ERROR] {repr(e)}\n")
    pass

        time.sleep(60)


if __name__ == "__main__":
    loop()
