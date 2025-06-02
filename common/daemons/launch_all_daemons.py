!/usr/bin/env bash#!/usr/bin/env bash
print("[DEBUG] launch_all_daemons.py starting")
# (script goes here)
#!/usr/bin/env python3
import os
import subprocess
import time
import threading
from pathlib import Path

# Debug print to confirm script is running
print("[DEBUG] launch_all_daemons.py starting")

# 1. Clock sync (NTP)
subprocess.call(["bash", "common/daemons/sync_time.sh"])

# 2. Remote Sync (GitHub)
subprocess.call(["bash", "common/daemons/remote_sync.sh"])

# 3. Define repository root
REPO_ROOT = Path(__file__).resolve().parents[2]

# 4. Start Shadow-srv services
shadow_folder = REPO_ROOT / "shadow_srv"
if shadow_folder.exists():
    for svc in shadow_folder.glob("*.py"):
        print(f"[SHADOW] Starting {svc.name}")
        subprocess.Popen(
            ["python3", str(svc)],
            stdout=open("common/logs/shadow.log", "a"),
            stderr=open("common/logs/shadow.err", "a")
        )
else:
    print("[SHADOW] No shadow_srv folder found")

# 5. Start Oracle
oracle_script = REPO_ROOT / "common/oracle/oracle_daemon.py"
if oracle_script.exists():
    print("[ORACLE] Starting oracle_daemon.py")
    subprocess.Popen(
        ["python3", str(oracle_script), "--config", "common/config/oracle_config.json"],
        stdout=open("common/logs/oracle.log", "a"),
        stderr=open("common/logs/oracle.err", "a")
    )
else:
    print("[ERROR] Missing oracle_daemon.py")

# 6. Start Funpumper WS ingestion
fun_ws = REPO_ROOT / "funpumper/funpumper_ws.py"
if fun_ws.exists():
    print("[FUNPUMPER WS] Starting funpumper_ws.py")
    subprocess.Popen(
        ["python3", str(fun_ws)],
        stdout=open("common/logs/funpumper_ws.log", "a"),
        stderr=open("common/logs/funpumper_ws.err", "a")
    )
else:
    print("[ERROR] Missing funpumper_ws.py")
time.sleep(5)

# 7. Start Funpumper Phase 1
phase1 = REPO_ROOT / "funpumper/fun_purger_loop.py"
if phase1.exists():
    print("[FUNPUMPER PHASE1] Starting fun_purger_loop.py")
    subprocess.Popen(
        ["python3", str(phase1)],
        stdout=open("common/logs/fun_purger.log", "a"),
        stderr=open("common/logs/fun_purger.err", "a")
    )
else:
    print("[ERROR] Missing fun_purger_loop.py")

# 8. Start Funpumper Phase 2/3 predictor
phase2 = REPO_ROOT / "funpumper/fun_predict_eval_loop.py"
if phase2.exists():
    print("[FUNPUMPER PHASE2/3] Starting fun_predict_eval_loop.py")
    echo "[FUNPUMPER REFLECTION] Starting funpumper/fun_reflection_loop.py"

    os.system("python3 funpumper/fun_reflection_loop.py python3 funpumper/fun_reflection_loop.py &")
    subprocess.Popen(
        ["python3", str(phase2)],
        stdout=open("common/logs/fun_predict.log", "a"),
        stderr=open("common/logs/fun_predict.err", "a")
    )
else:
    print("[ERROR] Missing fun_predict_eval_loop.py")

# 9. Start Metrics Enricher
enricher = REPO_ROOT / "funpumper/metrics_enricher_loop.py"
if enricher.exists():
    print("[METRICS ENRICHER] Starting metrics_enricher_loop.py")
    subprocess.Popen(
        ["python3", str(enricher)],
        stdout=open("common/logs/metrics_enricher.log", "a"),
        stderr=open("common/logs/metrics_enricher.err", "a")
    )
else:
    print("[ERROR] Missing metrics_enricher_loop.py")

# 10. Start Funpumper Reflection/Mutation Engine
if reflection.exists():
    subprocess.Popen(
        ["python3", str(reflection)],
        stdout=open("common/logs/fun_reflection.log", "a"),
        stderr=open("common/logs/fun_reflection.err", "a")
    )
else:

# 11. Start Council
council = REPO_ROOT / "common/council/run_council.py"
if council.exists():
    print("[COUNCIL] Starting run_council.py")
    subprocess.Popen(
        ["python3", str(council), "--config", "common/config/council_config.json"],
        stdout=open("common/logs/council.log", "a"),
        stderr=open("common/logs/council.err", "a")
    )
else:
    print("[ERROR] Missing run_council.py")

# 12. Schedule Black Swan Simulation every 6 hours
sim_script = REPO_ROOT / "common/black_swan_agent/simulation_planner.py"
def schedule_simulation():
    while True:
        if sim_script.exists():
            print("[SIM] Running simulation_planner.py")
            subprocess.call(["python3", str(sim_script)])
        else:
            print("[ERROR] Missing simulation_planner.py")
        time.sleep(6 * 3600)

threading.Thread(target=schedule_simulation, daemon=True).start()

# 13. Start Telemetry Reporter (Telegram updates)
telemetry = REPO_ROOT / "common/telegram_telemetry_reporter.py"
if telemetry.exists():
    print("[TELEMETRY] Starting telegram_telemetry_reporter.py")
    subprocess.Popen(
        ["python3", str(telemetry), "--config", "common/config/telemetry_config.json"],
        stdout=open("common/logs/telemetry.log", "a"),
        stderr=open("common/logs/telemetry.err", "a")
    )
else:
    print("[ERROR] Missing telegram_telemetry_reporter.py")

# 14. Keep this script alive
while True:
    time.sleep(3600)

# ————— New additions to launch_all_daemons.py ————— #
#  1. Social Velocity (runs every 5 minutes)
social = REPO_ROOT / "common/agents/social_velocity.py"
if social.exists():
    print("[SOCIAL] Starting social_velocity.py")
    subprocess.Popen(
        ["python3", str(social)],
        stdout=open("common/logs/social_velocity.log", "a"),
        stderr=open("common/logs/social_velocity.err", "a")
    )
else:
    print("[ERROR] Missing social_velocity.py")

# 2. Feature Engineering (every 5 minutes)
feat_eng = REPO_ROOT / "common/features/feature_engineer.py"
if feat_eng.exists():
    print("[FE] Generating engineered features")
    subprocess.Popen(
        ["python3", str(feat_eng)],
        stdout=open("common/logs/feature_engineer.log", "a"),
        stderr=open("common/logs/feature_engineer.err", "a")
    )
else:
    print("[ERROR] Missing feature_engineer.py")

# 3. Real Model Training (once per hour)
train = REPO_ROOT / "common/models/train_models.py"
def schedule_training():
    while True:
        if train.exists():
            print("[TRAIN] Running model training")
            subprocess.call(["python3", str(train)])
        else:
            print("[ERROR] Missing train_models.py")
        time.sleep(3600)  # hourly

threading.Thread(target=schedule_training, daemon=True).start()

# 4. Active Learning (every 30 minutes)
active = REPO_ROOT / "common/active/active_learning.py"
def schedule_active():
    while True:
        if active.exists():
            print("[ACTIVE] Running uncertainty sampling")
            subprocess.call(["python3", str(active)])
        else:
            print("[ERROR] Missing active_learning.py")
        time.sleep(1800)  # every 30 min

threading.Thread(target=schedule_active, daemon=True).start()
