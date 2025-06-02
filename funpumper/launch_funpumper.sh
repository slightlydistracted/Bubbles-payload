#!/usr/bin/env bash
set -e

# 0️⃣ Go to the right folder
cd /srv/daemon-memory/funpumper || exit 1

# 1️⃣ Sanity‐check helius_utils.py can import
echo "[*] Validating helius_utils.py..."
if python3 - << 'PYCODE' 2>/dev/null
import helius_utils
PYCODE
then
  echo "[✓] helius_utils OK."
else
  echo "[✗] Failed to import helius_utils.py!"
  exit 1
fi

# 2️⃣ Kill any old FunPumper processes
echo "[*] Killing old FunPumper processes…"
pkill -f funpumper_ws.py               || true
pkill -f funpumper_loop.py             || true
pkill -f metrics_enricher_loop.py      || true
pkill -f weights_saver_loop.py         || true
pkill -f fun_purger_loop.py            || true
pkill -f survivor_tracker.py           || true
pkill -f token_history_logger.py       || true
pkill -f mint_filter.py                || true
pkill -f fun_reflection_loop.py        || true
pkill -f fun_predictor_loop.py         || true
pkill -f fun_predict_eval_loop.py      || true
pkill -f prediction_accuracy_tracker.py|| true
pkill -f fun_brain_loop.py             || true
pkill -f fun_brain_metrics.py          || true
pkill -f fun_brain_suggester.py        || true
pkill -f fun_brain_reporter.py         || true
pkill -f fun_accuracy_reporter.py      || true
pkill -f fun_mutation_engine.py        || true

#   ➕ Kill any leftover Phase-1 trainer
pkill -f fun_trainer_loop.py           || true

sleep 1

# 3️⃣ Launch everything in the background  
echo "[*] Launching FunPumper stack…"    
nohup python3 funpumper_ws.py               > funpumper_ws.log              2>&1 &  
nohup python3 funpumper_loop.py             > funpumper_loop.log            2>&1 &  
nohup python3 metrics_enricher_loop.py      > metrics_enricher.log          2>&1 &  
nohup python3 weights_saver_loop.py         > weights_saver_loop.log        2>&1 &  
nohup python3 fun_purger_loop.py            > fun_purger.log                2>&1 &  
nohup python3 survivor_tracker.py           > survivor_tracker.log          2>&1 &  
nohup python3 token_history_logger.py       > token_history_logger.log      2>&1 &  
nohup python3 mint_filter.py                > mint_filter.log               2>&1 &  
nohup python3 fun_reflection_loop.py        > fun_reflection_loop.log       2>&1 &  
nohup python3 fun_predictor_loop.py         > fun_predictor_loop.log        2>&1 &  
nohup python3 fun_predict_eval_loop.py      > fun_predict_eval_loop.log     2>&1 &  
nohup python3 prediction_accuracy_tracker.py> prediction_accuracy_tracker.log 2>&1 &  
nohup python3 fun_brain_loop.py             > fun_brain_loop.log            2>&1 &  
nohup python3 fun_brain_metrics.py          > fun_brain_metrics.log         2>&1 &  
nohup python3 fun_brain_suggester.py        > fun_brain_suggester.log       2>&1 &  
nohup python3 fun_brain_reporter.py         > fun_brain_reporter.log        2>&1 &  
nohup python3 fun_accuracy_reporter.py      > fun_accuracy_reporter.log     2>&1 &  
nohup python3 fun_mutation_engine.py        > fun_mutation.log              2>&1 &

#   ➕ Now launch the Phase-1 trainer and real-time predictor
nohup python3 fun_trainer_loop.py           > fun_trainer.log               2>&1 &
nohup python3 fun_predictor_loop.py         > fun_predictor.log             2>&1 &

echo "[✓] All FunPumper modules launched."
