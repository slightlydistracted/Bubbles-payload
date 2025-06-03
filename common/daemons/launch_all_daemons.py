import subprocess
import sys
import os

# Make sure we're in the root project directory!
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

DAEMONS = [
    # Format: (module_path, log_base)
    # Example: ("common.oracle.oracle_daemon", "oracle")
    ("common.oracle.oracle_daemon", "oracle"),
    ("common.telegram_telemetry_reporter", "telemetry"),
    ("common.council.run_council", "council"),
    ("funpumper.metrics_enricher_loop", "metrics_enricher"),
    ("funpumper.fun_purger_loop", "fun_purger"),
    ("funpumper.fun_predict_eval_loop", "fun_predict"),
    ("funpumper.fun_reflection_loop", "fun_reflection"),
    ("funpumper.fun_predictor_loop", "fun_predictor"),
    ("funpumper.fun_mutation_engine", "fun_mutation"),
    ("funpumper.fun_trainer_loop", "fun_trainer"),
    ("funpumper.fun_brain_loop", "fun_brain"),
    ("funpumper.fun_accuracy_reporter", "fun_accuracy_reporter"),
    ("funpumper.fun_accuracy_reporter", "fun_accuracy_reporter"),
    ("funpumper.fun_reflection_loop", "fun_reflection"),
    ("funpumper.fun_predictor_loop", "fun_predictor"),
    ("funpumper.fun_brain_loop", "fun_brain"),
    # Add others as needed
    # ("common.oracle.another_daemon", "another_log_name"),
]

def launch_daemon(module_path, log_base):
    log_dir = "common/logs"
    os.makedirs(log_dir, exist_ok=True)
    log_out = os.path.join(log_dir, f"{log_base}.log")
    log_err = os.path.join(log_dir, f"{log_base}.err")
    with open(log_out, "ab") as stdout, open(log_err, "ab") as stderr:
        # Use -m for proper Python package imports!
        print(f"Launching {module_path} ...")
        subprocess.Popen(
            [sys.executable, "-m", module_path],
            stdout=stdout,
            stderr=stderr,
            close_fds=True,
        )

if __name__ == "__main__":
    for module_path, log_base in DAEMONS:
        try:
            launch_daemon(module_path, log_base)
        except Exception as e:
            print(f"[ERROR] Could not launch {module_path}: {e}")
