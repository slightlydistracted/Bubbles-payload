import sys
import subprocess
import os
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/../../"))
#!/usr/bin/env python3

repo_root = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, repo_root)
os.environ["PYTHONPATH"] = repo_root + (":" + os.environ.get("PYTHONPATH", ""))

DAEMONS = [
    ("funpumper", "fun_accuracy_reporter.py"),
    ("funpumper", "fun_reflection_loop.py"),
    ("funpumper", "fun_predictor_loop.py"),
    ("funpumper", "fun_brain_loop.py"),
    ("funpumper", "fun_predict_eval_loop.py"),
    ("funpumper", "fun_purger_loop.py"),
    ("funpumper", "metrics_enricher_loop.py"),
    ("funpumper", "fun_trainer_loop.py"),
    ("shadow_srv", "shadow_service_1.py"),
    ("shadow_srv", "shadow_service_2.py"),
    ("common/oracle", "oracle_daemon.py"),
    ("common/council", "run_council.py"),
    ("common", "telegram_telemetry_reporter.py"),
    ("common/black_swan_agent", "simulation_planner.py"),
]

LOG_DIR = os.path.join(repo_root, "common", "logs")
os.makedirs(LOG_DIR, exist_ok=True)


def launch_daemon(mod_path, script):
    script_path = os.path.join(repo_root, mod_path, script)
    log_file = os.path.join(LOG_DIR, f"{script.replace('.py','')}.log")
    err_file = os.path.join(LOG_DIR, f"{script.replace('.py','')}.err")
    print(f"Launching {script_path} ...")
    with open(log_file, "a") as logf, open(err_file, "a") as errf:
        subprocess.Popen(
            ["python3", script_path],
            stdout=logf,
            stderr=errf,
            env=os.environ.copy(),
        )


if __name__ == "__main__":
    for mod_path, script in DAEMONS:
        launch_daemon(mod_path, script)
    print("All daemons launched.")
