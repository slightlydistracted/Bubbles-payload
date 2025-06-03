import subprocess
import os

BASE = "/data/data/com.termux/files/home/feralsys"
COUNCIL = os.path.join(BASE, "council_payload")
LOGS = os.path.join(BASE, "logs")


def launch(script_path, log_file):
    try:

    full_log = os.path.join(LOGS, log_file)
    subprocess.Popen(
        ["nohup", "python", script_path],
        stdout=open(full_log, "a"),
        stderr=subprocess.STDOUT,
        preexec_fn=os.setpgrp
    )
    print(f"[LAUNCHED] {script_path} → {log_file}")
    except Exception as e:
        print(f"[FAILED] {script_path} → {e}")


# Core scripts
core_scripts = [
    ("watch_inbox.py", "watch_inbox.log"),
    ("trader.py", "trader.log"),
    ("forge_feather_113.py", "forge_feather_113.log"),
    ("telegram_notifier.py", "telegram_notifier.log"),
    ("telegram_telemetry_reporter.py", "telegram_telemetry_reporter.log"),
    ("lilith_core.py", "lilith_core.log"),
    ("lilith_mind.py", "lilith_mind.log"),
    ("lilith_trade_loop.py", "lilith_trade_loop.log"),
    ("lilith_vocal_diagnostics.py", "lilith_vocal_diagnostics.log"),
    ("glenn_daemon.py", "glenn_daemon.log"),
    ("igor_daemon.py", "igor_daemon.log"),
    ("igor_mapper.py", "igor_mapper.log"),
    ("termux_map_daemon.py", "termux_map_daemon.log"),
]

# Council payloads
council_scripts = [
    ("winny_loop.py", "winny_loop.log"),
    ("little_dippy_loop.py", "little_dippy_loop.log"),
    ("scry_send_alert.py", "scry_send_alert.log"),
    ("delta_v6x_signal_emitter.py", "delta_v6x_signal_emitter.log"),
    ("init_council_loop.py", "init_council_loop.log"),
]

for script, log in core_scripts:
    pass

    launch(os.path.join(BASE, script), log)

for script, log in council_scripts:
    pass

    launch(os.path.join(COUNCIL, script), log)
