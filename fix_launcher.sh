#!/bin/bash

set -e

LAUNCHER="common/daemons/launch_all_daemons.py"

echo "---- [BUBBLES] Fixing $LAUNCHER for proper Python module launching ----"

# Make a backup
cp "$LAUNCHER" "$LAUNCHER.bak"

# Replace python3 <relpath>.py with python3 -m <dot.path> everywhere in launcher
sed -i -E '
s#(["'\''])python3(["'\'']?), *["'\'']common/oracle/oracle_daemon\.py["'\'']#\1python3\2, "-m", "common.oracle.oracle_daemon"#g;
s#(["'\''])python3(["'\'']?), *["'\'']funpumper/funpumper_ws\.py["'\'']#\1python3\2, "-m", "funpumper.funpumper_ws"#g;
s#(["'\''])python3(["'\'']?), *["'\'']funpumper/metrics_enricher_loop\.py["'\'']#\1python3\2, "-m", "funpumper.metrics_enricher_loop"#g;
s#(["'\''])python3(["'\'']?), *["'\'']funpumper/fun_predict_eval_loop\.py["'\'']#\1python3\2, "-m", "funpumper.fun_predict_eval_loop"#g;
s#(["'\''])python3(["'\'']?), *["'\'']funpumper/fun_purger_loop\.py["'\'']#\1python3\2, "-m", "funpumper.fun_purger_loop"#g;
s#(["'\''])python3(["'\'']?), *["'\'']funpumper/fun_reflection_loop\.py["'\'']#\1python3\2, "-m", "funpumper.fun_reflection_loop"#g;
s#(["'\''])python3(["'\'']?), *["'\'']common/council/run_council\.py["'\'']#\1python3\2, "-m", "common.council.run_council"#g;
s#(["'\''])python3(["'\'']?), *["'\'']common/telegram_telemetry_reporter\.py["'\'']#\1python3\2, "-m", "common.telegram_telemetry_reporter"#g;
s#(["'\''])python3(["'\'']?), *["'\'']common/simulation_planner\.py["'\'']#\1python3\2, "-m", "common.simulation_planner"#g;
' "$LAUNCHER"

echo "---- [BUBBLES] Launcher patched. Backup at $LAUNCHER.bak ----"

# Optional: Warn if not in repo root
echo 'import os, sys; assert os.path.isfile("common/daemons/launch_all_daemons.py"), "Run this from repo root!"' \
  | cat - "$LAUNCHER" > temp && mv temp "$LAUNCHER"

echo "---- [BUBBLES] All done! Relaunch your daemons from repo root: ----"
echo "cd ~/projects/Bubbles-payload"
echo "nohup python3 common/daemons/launch_all_daemons.py > launcher.out 2>&1 &"
echo "tail -f common/logs/*.err"
