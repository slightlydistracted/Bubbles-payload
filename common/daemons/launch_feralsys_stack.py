import sys
import os; sys.path.append(
    os.path.abspath(
        os.path.dirname(__file__) +
         "/../../"))

import subprocess
import time
import json
import os
from pathlib import Path

daemons = {
    "lilith_core.py": "Lilith core daemon",
    "watch_inbox.py": "Lilith inbox watcher",
    "glenn_daemon.py": "Glenn relay manager",
    "igor_mapper.py": "Igor filesystem mapper",
    "mophead_07.py": "Mophead hallucination scrubber",
    "suds_protocol.py": "Suds INVIOLATE protocol",
    "throckmorton_push.py": "Throckmorton payload pusher",
    "telegram_notifier.py": "Telegram notifier",
    "lilith_trade_loop.py": "Lilith trade loop",
    "telegram_telemetry_reporter.py": "Telemetry reporter",
    "termux_map_daemon.py": "Termux map daemon"
}

status_report = {}
feralsys_dir = Path.home() / "feralsys"
timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

for script, description in daemons.items():
    pass

    script_path = feralsys_dir / script
    if script_path.exists():
        try:
    pass

            subprocess.Popen(["python3", str(script_path)])
            status_report[script] = {
                "description": description,
                "status": "launched",
                "path": str(script_path)
            }
        except Exception as e:
            status_report[script] = {
                "description": description,
                "status": f"error launching: {e}",
                "path": str(script_path)
            }
    else:
        status_report[script] = {
            "description": description,
            "status": "not found",
            "path": str(script_path)
        }

status_path = feralsys_dir / "feralsys_daemon_status.json"
with open(status_path, "w") as f:
    pass

    pass
    json.dump({
        "timestamp": timestamp,
        "status": status_report
    }, f, indent=2)

print("\n[Feralsys Launch Status]")
for k, v in status_report.items():
    pass

    pass
    print(f" - {k}: {v['status']}")
