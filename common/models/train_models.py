#!/usr/bin/env python3
import json
import pickle
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from pathlib import Path

# —— CONFIG —— #
MEMORY_PATH = "common/black_swan_agent/mutation_memory.json"
FEATURES_PATH = "common/features/engineered_features.json"
MODEL_DIR = "common/models"

PHASE1_PKL = f"{MODEL_DIR}/phase1_2x.pkl"
PHASE1_SURVIVE_PKL = f"{MODEL_DIR}/phase1_survive.pkl"
PHASE2_PKL = f"{MODEL_DIR}/phase2_4x.pkl"
PHASE3_PKL = f"{MODEL_DIR}/phase3_6x.pkl"

def load_memory():
    try:
        return json.load(open(MEMORY_PATH))
    except:
        return {"mutations": []}

def load_features():
    try:
        df = pd.read_json(FEATURES_PATH)
        return df
    except:
        return pd.DataFrame()

def train_phase(phase, label_col, output_path):
    mem = load_memory().get("mutations", [])
    feats = load_features()
    if feats.empty or not mem:
        print(f"[TRAIN] No data for Phase {phase}")
        return

    # Build DataFrame of memory entries
    records = []
    for m in mem:
        if m["phase"] == phase:
            rec = {"address": m["token"], label_col: (1 if m["outcome"] == label_col else 0)}
            rec.update(m.get("features", {}))
            records.append(rec)
    if not records:
        print(f"[TRAIN] No records labeled for Phase {phase}")
        return

    df_mem = pd.DataFrame(records)
    # Merge with engineered features on “address”
    df = pd.merge(df_mem, feats, on="address", how="left").dropna()
    y = df[label_col]
    X = df.drop(columns=["address", "mint_time", label_col])

    # Train/test split
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # LightGBM dataset
    lgb_train = lgb.Dataset(X_train, label=y_train)
    lgb_val = lgb.Dataset(X_val, label=y_val, reference=lgb_train)

    params = {
        "objective": "binary",
        "metric": "auc",
        "learning_rate": 0.05,
        "verbose": -1
    }
    print(f"[TRAIN] Training Phase {phase} model ({label_col}) on {len(X_train)} examples...")
    gbm = lgb.train(
        params,
        lgb_train,
        num_boost_round=500,
        valid_sets=[lgb_train, lgb_val],
        early_stopping_rounds=50,
        verbose_eval=50
    )
    # Evaluate
    preds = gbm.predict(X_val)
    auc = roc_auc_score(y_val, preds)
    print(f"[TRAIN] Phase {phase} {label_col} AUC: {auc:.4f}")

    # Save model
    Path(MODEL_DIR).mkdir(parents=True, exist_ok=True)
    pickle.dump(gbm, open(output_path, "wb"))
    print(f"[TRAIN] Saved Phase {phase} model to {output_path}")

def main():
    # Phase 1: two separate labels (2× vs. survive vs. fail)
    train_phase(1, "2x", PHASE1_PKL)
    # Optionally train a “survive” model (if you have distinct labels)
    # train_phase(1, "survive", PHASE1_SURVIVE_PKL)

    # Phase 2: only tokens that graduated Phase 1 have “4x” or “dead”
    train_phase(2, "4x", PHASE2_PKL)

    # Phase 3: only tokens that graduated Phase 2 have “6x” or “dead”
    train_phase(3, "6x", PHASE3_PKL)

if __name__ == "__main__":
    main()
