#!/usr/bin/env python3
import os
import json
import time
import pickle
from datetime import datetime

import numpy as np
from sklearn.linear_model import LogisticRegression

# ————————— PATHS —————————
WEIGHTS_PATH    = "/srv/daemon-memory/funpumper/funpumper_weights.json"
MODEL_PATH      = "/srv/daemon-memory/funpumper/phase1_model.pkl"
TRAINER_LOG     = "/srv/daemon-memory/funpumper/fun_trainer.log"

# Phase 1 bins (end‐timestamps in seconds) relative to mint:
P1_CHECK_TIMES = [15, 60, 150, 300]

# Retrain every 3600 seconds (1 hour)
RETRAIN_INTERVAL_S = 3600


def log(msg: str):
    ts = datetime.utcnow().isoformat()
    with open(TRAINER_LOG, "a") as f:
        f.write(f"[{ts}] {msg}\n")


def load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        return json.load(open(path))
    except:
        return default


def save_model(model, path):
    with open(path, "wb") as f:
        pickle.dump(model, f)


def gather_phase1_examples():
    """
    Returns two lists:
      X_list = [ [r15, r60, r150, r300], … ]  (ratios: price@t / price@0)
      y_list = [ 0 or 1, … ]
    Only include tokens that have at least one price entry at each of 15s, 60s, 150s, 300s.
    """
    data = load_json(WEIGHTS_PATH, {})
    X_list = []
    y_list = []

    now = int(time.time())
    for mint, info in data.items():
        # We need price_log with at least one entry >= 300s old
        # price_log is a list of [timestamp, price_usd] entries
        price_log = info.get("price_log", [])
        if not price_log or "initial_price" not in info:
            continue

        t0 = info["initial_price"]  # price at “0s” (first positive price encountered)
        if t0 <= 0:
            continue

        # Build a small mapping: { age_in_seconds: price }
        # (take the *first* price we saw in each P1_CHECK_TIMES bin)
        # e.g. “price at ~ 15s” := the earliest price_log entry where (timestamp – mint_time) ≥ 15
        m = info["mint_time"]
        bucket_prices = {}  # key = check_time, val = price_usd
        for ts, p in price_log:
            age = ts - m
            for check in P1_CHECK_TIMES:
                if age >= check and check not in bucket_prices:
                    bucket_prices[check] = p

        # Only keep if we got all 4 bins
        if all(check in bucket_prices for check in P1_CHECK_TIMES):
            # Feature vector: [p15/t0, p60/t0, p150/t0, p300/t0]
            ratios = [ bucket_prices[check] / t0 for check in P1_CHECK_TIMES ]
            X_list.append(ratios)

            # Label = 1 if p300 >= 2× t0, else 0
            y_list.append(1 if bucket_prices[300] >= 2.0 * t0 else 0)

    return X_list, y_list


def train_phase1_model():
    X_list, y_list = gather_phase1_examples()
    n = len(X_list)
    if n < 50:
        log(f"[SKIP] Only {n} examples found (<50). Waiting for more data.")
        return

    X = np.array(X_list)
    y = np.array(y_list)

    # Simple logistic‐regression classifier
    model = LogisticRegression(C=1.0, max_iter=200)
    model.fit(X, y)

    save_model(model, MODEL_PATH)
    log(f"[TRAINED] Phase 1 model retrained on {n} examples. Positive labels: {int(y.sum())}.")


def loop():
    log("🚀 FunTrainer loop started.")
    last_train = 0

    while True:
        now = time.time()
        if now - last_train >= RETRAIN_INTERVAL_S:
            try:
                train_phase1_model()
            except Exception as e:
                log(f"[ERROR] {e}")
            last_train = now
        time.sleep(10)


if __name__ == "__main__":
    print("### FUN_TRAINER_LOOP STARTED ###")
    loop()
