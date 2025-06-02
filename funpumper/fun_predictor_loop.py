#!/usr/bin/env python3
import os
import json
import time
import pickle
from datetime import datetime

from helius_utils import get_token_price
from fun_purger_loop import get_phase_and_subinterval

# ————————— PATHS —————————
WEIGHTS_PATH      = "/srv/daemon-memory/funpumper/funpumper_weights.json"
PREDICTIONS_PATH  = "/srv/daemon-memory/funpumper/fun_predictions.json"
MODEL_PATH        = "/srv/daemon-memory/funpumper/phase1_model.pkl"
PREDICTOR_LOG     = "/srv/daemon-memory/funpumper/fun_predictor.log"

# Phase 1 bins (# of checks = 4)
P1_CHECK_TIMES = [15, 60, 150, 300]

LOOP_INTERVAL_S = 5  # run every 5 seconds


def log(msg: str):
    ts = datetime.utcnow().isoformat()
    with open(PREDICTOR_LOG, "a") as f:
        f.write(f"[{ts}] {msg}\n")


def load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        return json.load(open(path))
    except:
        return default


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_phase1_model():
    """
    Attempt to load the latest Phase 1 model. If not found or invalid, return None.
    """
    if not os.path.exists(MODEL_PATH):
        return None
    try:
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    except:
        return None


def build_phase1_features(info: dict, now: int):
    """
    Given one token’s `info` (from funpumper_weights.json) and the current time,
    return a 4‐element ratio vector [p15/t0, p60/t0, p150/t0, p300/t0], BUT only
    if each check time has passed. Otherwise return None.

    We look for the first price_log entry at or after each P1_CHECK_TIMES[k].
    """
    if "initial_price" not in info or info["initial_price"] <= 0:
        return None

    price_log = info.get("price_log", [])
    if not price_log:
        return None

    m = info["mint_time"]
    t0 = info["initial_price"]

    # Build a mapping check_time → price_usd
    bucket_prices = {}
    for ts, p in price_log:
        age = ts - m
        for check in P1_CHECK_TIMES:
            if age >= check and check not in bucket_prices:
                bucket_prices[check] = p

    # If we have all 4 check times, build ratios
    if all(check in bucket_prices for check in P1_CHECK_TIMES):
        return [ bucket_prices[check] / t0 for check in P1_CHECK_TIMES ]
    return None


def run_predictions():
    now = int(time.time())
    data = load_json(WEIGHTS_PATH, {})
    preds = load_json(PREDICTIONS_PATH, {})

    model = load_phase1_model()

    for mint, info in data.items():
        phase, subidx = get_phase_and_subinterval(info, now)

        # Only make a Phase 1 prediction once per subinterval
        if phase == 1 and subidx is not None:
            key = f"{mint}@1-{subidx}"
            if key in preds:
                continue  # already predicted for this bin

            features = build_phase1_features(info, now)
            if features is None:
                # Not enough data to predict yet
                continue

            if model is not None:
                try:
                    prob = float(model.predict_proba([features])[0, 1])
                except Exception as e:
                    prob = None
                    log(f"[PREDICT-ERR] {mint} subidx={subidx} → {e}")
                else:
                    log(f"[PREDICT] {mint} subidx={subidx} → p={prob:.3f}")
            else:
                prob = None
                log(f"[PREDICT-SKIP] {mint} subidx={subidx} → no model")

            preds[key] = {
                "timestamp": now,
                "phase": 1,
                "subinterval": subidx,
                "features": features,
                "prediction": prob
            }

    save_json(PREDICTIONS_PATH, preds)


def loop():
    log("🔮 FunPredictor loop started.")
    while True:
        try:
            run_predictions()
        except Exception as e:
            log(f"[ERROR] {e}")
        time.sleep(LOOP_INTERVAL_S)


if __name__ == "__main__":
    print("### FUN_PREDICTOR_LOOP STARTED ###")
    loop()
