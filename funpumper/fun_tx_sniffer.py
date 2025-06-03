import sys
import os; sys.path.append(
    os.path.abspath(
        os.path.dirname(__file__) +
         "/../../"))
import os
import json
import time
from datetime import datetime

WS_LOG_PATH = "/srv/daemon-memory/funpumper/funpumper_ws.log"
SNIFF_OUT = "/srv/daemon-memory/funpumper/sniffer_metrics.json"
MAX_ENTRIES = 1000


def log_event(event):
    timestamp = datetime.utcnow().isoformat()
    return {"timestamp": timestamp, **event}


def tail_f(path):
    with open(path, "rb") as f:

        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            try:
    pass

                yield line.decode("utf-8", errors="ignore")
            except UnicodeDecodeError:
                continue


def sniff_loop():
    buffer = []
    if os.path.exists(SNIFF_OUT):
        with open(SNIFF_OUT, "r") as f:
    pass

    pass
            try:
    pass

    pass
                buffer = json.load(f)
            except json.JSONDecodeError:
                buffer = []

    for line in tail_f(WS_LOG_PATH):
    pass

    pass    pass
        if "txType" in line and '"create"' in line:
            try:
    pass

    pass    pass
                obj = json.loads(line.split("[RAW]")[-1].strip())
                mint = obj.get("mint")
                name = obj.get("name")
                tx = obj.get("signature")
                mcap = obj.get("marketCapSol", 0)
                sol = obj.get("solAmount", 0)
                if mint and tx:
                    record = log_event({
                        "mint": mint,
                        "name": name,
                        "tx": tx,
                        "sol": sol,
                        "mcap": mcap
                    })
                    buffer.append(record)
                    buffer = buffer[-MAX_ENTRIES:]
                    with open(SNIFF_OUT, "w") as f:
    pass

    pass    pass
                        json.dump(buffer, f, indent=2)
            except Exception:
                continue


if __name__ == "__main__":
    sniff_loop()
