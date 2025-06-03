#!/usr/bin/env python3
import json
import time
from datetime import datetime, timedelta
from pathlib import Path

# —— INPUT PATHS —— #
FUN_PUMPER_LIVE = "funpumper/live_ws_tokens.json"
FUN_FILTERED = "funpumper/fun_filtered.json"
FUN_PREDICTIONS = "funpumper/fun_predictions.json"  # Phase1/2 preds
WHale_FEED = "common/data_feeds/whale_activity.json"
SENTIMENT_FEED = "common/data_feeds/sentiment_feed.json"
DELTA_FEED = "common/data_feeds/delta_6x_signals.json"
SOCIAL_VEL_FEED = "common/data_feeds/social_velocity.json"

# —— OUTPUT —— #
FEATURES_OUTPUT = "common/features/engineered_features.json"

# Helper: read newline-delimited JSON from a file, return list of dicts


def read_ndjson(path):
    out = []
    if not Path(path).exists():
        return out
    for line in open(path, "r"):
        try:
            out.append(json.loads(line))
        except:
            continue
    return out


def build_feature_vector(token):
    addr = token["address"]
    base = {
        "address": addr,
        "mint_time": token.get("timestamp", None),
        "initial_liquidity": token.get("liquidity", 0),
        "initial_price": token.get("price", 0),
    }

    # —— Whale count in first 5 minutes —— #
    whales = read_ndjson(WHale_FEED)
    cutoff = datetime.fromisoformat(
        base["mint_time"]) + timedelta(minutes=5) if base["mint_time"] else None
    whale_buys = [w for w in whales if w.get("token") == addr
                  and cutoff and datetime.fromisoformat(w["timestamp"]) <= cutoff]
    base["whale_buys_5m"] = len(whale_buys)

    # —— Sentiment in first 10 minutes —— #
    sents = read_ndjson(SENTIMENT_FEED)
    cutoff2 = datetime.fromisoformat(
        base["mint_time"]) + timedelta(minutes=10) if base["mint_time"] else None
    sent_scores = [s["sentiment"] for s in sents
                   if s.get("token") == addr
                   and cutoff2 and datetime.fromisoformat(s["timestamp"]) <= cutoff2]
    base["avg_sentiment_10m"] = sum(
        sent_scores)/len(sent_scores) if sent_scores else 0

    # —— Delta 6× score —— #
    deltas = read_ndjson(DELTA_FEED)
    delta_scores = [d["score"] for d in deltas if d.get("token") == addr]
    base["delta_6x_score"] = max(delta_scores) if delta_scores else 0

    # —— Social velocity at mint time —— #
    socials = read_ndjson(SOCIAL_VEL_FEED)
    # Find the entry whose timestamp is closest before mint_time
    if base["mint_time"]:
        mint_dt = datetime.fromisoformat(base["mint_time"])
        past = [s for s in socials if datetime.fromisoformat(
            s["timestamp"]) <= mint_dt]
        if past:
            nearest = max(
                past, key=lambda s: datetime.fromisoformat(s["timestamp"]))
            base["twitter_cnt_5m"] = nearest.get("twitter_mentions_5m", 0)
            base["reddit_cnt_15m"] = nearest.get("reddit_mentions_15m", 0)
        else:
            base["twitter_cnt_5m"] = 0
            base["reddit_cnt_15m"] = 0
    else:
        base["twitter_cnt_5m"] = 0
        base["reddit_cnt_15m"] = 0

    # —— Phase 1/2 predicted probabilities —— #
    preds = {}
    for _ in [FUN_PREDICTIONS]:
        if Path(FUN_PREDICTIONS).exists():
            all_preds = json.load(open(FUN_PREDICTIONS))
            if addr in all_preds:
                preds = all_preds[addr]
    base["pred_score4x"] = preds.get("score4x", 0)
    base["pred_score6x"] = preds.get("score6x", 0)

    return base


def main():
    Path(FEATURES_OUTPUT).parent.mkdir(parents=True, exist_ok=True)

    try:
        tokens = json.load(open(FUN_FILTERED))
    except:
        tokens = []

    all_features = []
    for token in tokens:
        fv = build_feature_vector(token)
        all_features.append(fv)

    with open(FEATURES_OUTPUT, "w") as f:
        json.dump(all_features, f, indent=2)

    print(f"[FE] Generated features for {len(all_features)} tokens.")


if __name__ == "__main__":
    main()
