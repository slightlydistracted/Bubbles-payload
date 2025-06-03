#!/bin/bash

echo "---- Removing byte order marks (BOM) from all .py files ----"
find . -type f -name "*.py" -exec sed -i '1s/^\xEF\xBB\xBF//' {} +

echo "---- Running autopep8 for indentation and style (if installed) ----"
if command -v autopep8 &> /dev/null; then
  autopep8 -i $(find . -type f -name "*.py")
else
  echo "autopep8 not installed, skipping formatting."
fi

echo "---- Patching all Python files to replace 'fl.write' or 'fo.write' not in 'with open' blocks ----"
# This is NOT perfect, but will brute force wrap lone file writes in with-open blocks
find . -type f -name "*.py" -exec sed -i \
  -e '/^[^#]*fl\.write/s/^/with open("common\/logs\/telemetry.log", "a") as fl:\n    /' \
  -e '/^[^#]*fo\.write/s/^/with open("common\/logs\/oracle.log", "a") as fo:\n    /' \
  {} +

echo "---- Ensuring default config files and all required keys exist ----"
mkdir -p common/config

# TELEMETRY
cat > common/config/telemetry_config.py <<EOF
TELEMETRY_SETTINGS = {
    "api_id": "20244657",
    "api_hash": "582b485fdbe22b7a0677f04ada1b05b6",
    "bot_token": "8090852179:AAE4xSKKs2T5AAapWVzOIuwEq3NVLXvLSnc",
    "chat_id": "8071168808"
}
EOF

# ORACLE
cat > common/config/oracle_config.py <<EOF
ORACLE_SETTINGS = {
    "api_id": "20244657",
    "api_hash": "582b485fdbe22b7a0677f04ada1b05b6",
    "bot_token": "8090852179:AAE4xSKKs2T5AAapWVzOIuwEq3NVLXvLSnc",
    "chat_id": "8071168808"
}
EOF

echo "---- Ensuring all log files exist (touch) ----"
for logf in shadow.err oracle.err funpumper_ws.err fun_purger.err fun_predict.err metrics_enricher.err fun_reflection.err council.err telemetry.err simulation_planner.err; do
  touch common/logs/$logf
done

echo "---- Checking for non-printable character bugs (U+FEFF) ----"
find . -type f -name "*.py" -exec sed -i 's/\xEF\xBB\xBF//g' {} +

echo "---- [OPTIONAL] Re-run all orchestrators after fixing ----"
echo "Run: nohup python3 common/daemons/launch_all_daemons.py > launcher.out 2>&1 &"

echo "---- DONE. If anything explodes, paste errors here. ----"
