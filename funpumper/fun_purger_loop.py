#!/usr/bin/env python3

import os
import json
import time
from datetime import datetime
import requests

# === PATHS ===
WEIGHTS_PATH       = "/srv/daemon-memory/funpumper/funpumper_weights.json"
DEADLIST_PATH      = "/srv/daemon-memory/funpumper/fun_deadlist.json"
GRAD_PATH          = "/srv/daemon-memory/funpumper/fun_graduated.json"
LIVE_WS_PATH       = "/srv/daemon-memory/funpumper/live_ws_tokens.json"
PURGER_LOG         = "/srv/daemon-memory/funpumper/fun_purger.log"

# === PHASE THRESHOLDS (in seconds) ===
P1_THRESHOLD       = 300      # Phase 1 ends at 5 minutes (0–300 s)
P2_THRESHOLD       = 1800     # Phase 2 ends at 30 minutes (300–1800 s)
P3_THRESHOLD       = 3600     # Phase 3 ends at 1 hour (1800–3600 s)

# === PHASE 1 SUB-INTERVALS ===
# (0–15 s), (15–60 s), (60–150 s), (150–300 s)
P1_BINS = [
    (0, 15),
    (15, 60),
    (60, 150),
    (150, 300),
]

def log(msg):
    """
    Append a timestamped line to fun_purger.log.
    """
    ts = datetime.utcnow().isoformat()
    with open(PURGER_LOG, "a") as f:
        f.write(f"[{ts}] {msg}\n")

def load_json(path, default):
    """
    Safely load JSON from `path`; if missing or invalid, return `default`.
    """
    if not os.path.exists(path):
        return default
    try:
        return json.load(open(path))
    except Exception:
        return default

def save_json(path, data):
    """
    Write `data` (a Python object) to `path` as pretty-printed JSON.
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def fetch_price(mint):
    """
    Wrapper around helius_utils.get_token_price(mint).
    Returns a float USD price, or None if unavailable.
    """
    from helius_utils import get_token_price
    return get_token_price(mint)

def get_phase_and_subinterval(info, now):
    """
    Determine which phase (1–3) the token is currently in, plus sub-interval index:
      • Phase 1 (age < 300 s) → subidx ∈ [0..3] corresponding to P1_BINS
      • Phase 2 (300 s ≤ age < 1800 s) → subidx 0..9 for 300–600 s every 30 s, then 10..29 for 600–1800 s every 60 s
      • Phase 3 (1800 s ≤ age < 3600 s) → subidx 0..5 for each 300 s bin
      • Phase 4 (age ≥ 3600 s) → returns (4, None)

    Returns: (phase_number, sub_interval_index)
    """
    age = now - info["mint_time"]

    # Phase 1 (0–300 s)
    if age < P1_THRESHOLD:
        for idx, (start, end) in enumerate(P1_BINS):
            if start <= age < end:
                return (1, idx)
        return (1, None)

    # Phase 2 (300–1800 s)
    if age < P2_THRESHOLD:
        delta = age - P1_THRESHOLD  # 0..1500
        if delta < 300:
            # 300–600 s by 30 s → subidx = 0..9
            return (2, int(delta // 30))
        else:
            # 600–1800 s by 60 s → subidx = 10..29
            delta2 = delta - 300  # 0..1200
            return (2, 10 + int(delta2 // 60))

    # Phase 3 (1800–3600 s)
    if age < P3_THRESHOLD:
        delta = age - P2_THRESHOLD  # 0..1800
        # Every 300 s → subidx = 0..5
        return (3, int(delta // 300))

    # Phase 4 (≥ 3600 s)
    return (4, None)

def evaluate():
    """
    One evaluation cycle: ingest new WS tokens, purge/graduate at phase boundaries,
    update price_log + (optional) sub-interval features for tokens still in Phase 1–3,
    then save state back to disk.
    """
    now = int(time.time())
    data      = load_json(WEIGHTS_PATH, {})      # { mint: info, … }
    deadlist  = load_json(DEADLIST_PATH, [])     # [mint, …]
    graduated = load_json(GRAD_PATH, {})         # { mint: info, … }

    # 1) Ingest new WS tokens into Phase 1
    #    We expect live_ws to contain, for each mint: 
    #        { "mint_time": …, "initialBuy": …, "vSolInBondingCurve": …, "vTokensInBondingCurve": …, … }
    live_ws = load_json(LIVE_WS_PATH, {})
    for mint, msg in live_ws.items():
        if mint not in data and mint not in deadlist and mint not in graduated:
            # Compute initial_price (USD) right away:
            v_sol    = msg.get("vSolInBondingCurve", 0.0)
            v_tokens = msg.get("vTokensInBondingCurve", 0.0)
            if v_tokens and v_tokens != 0:
                price_in_sol = float(v_sol) / float(v_tokens)
            else:
                price_in_sol = 0.0

            # Fetch SOL→USD once (cached internally by helius_utils)
            sol_usd = fetch_price(WRAPPED_SOL_MINT) if False else None
            # Actually, we don’t have a get_price for SOL itself here, so just call helper:
            from helius_utils import _get_sol_usd_price
            sol_usd = _get_sol_usd_price() or 0.0

            initial_price_usd = price_in_sol * sol_usd if (price_in_sol and sol_usd) else 0.0

            data[mint] = {
                "phase": 1,
                "mint_time": now,
                "initial_price": initial_price_usd,
                "price_log": [[now, initial_price_usd]],
                "phase1_data": {
                    # We’ll fill sub‐interval features here, e.g.:
                    # 0: {"volume_sol": 0.0, "buyers": set(), "slippage_samples": []}, …
                },
                "phase2_data": {},
                "phase3_data": {},
                "last_price": initial_price_usd,
            }
            log(f"[UPDATE] New mint from WS added to weights: {mint} (init_price=${initial_price_usd:.8f})")

    # 2) Build active‐phase sets
    active_p1 = set()
    active_p2 = set()
    active_p3 = set()
    for mint, info in data.items():
        age = now - info["mint_time"]
        if age < P1_THRESHOLD:
            active_p1.add(mint)
        elif age < P2_THRESHOLD:
            active_p2.add(mint)
        elif age < P3_THRESHOLD:
            active_p3.add(mint)

    # 3) Phase 1 → Phase 2 transition & purge at T = 300 s
    for mint in list(active_p1):
        info = data[mint]
        age = now - info["mint_time"]
        if age >= P1_THRESHOLD:
            # We’ve hit 300 s for this mint
            price_300s = fetch_price(mint) or 0.0

            # initial_price was already recorded at ingest
            initial_price = info.get("initial_price", 0.0)

            # Purge if price == 0 → truly dead
            if price_300s <= 0:
                deadlist.append(mint)
                del data[mint]
                active_p1.remove(mint)
                log(f"[P1-PURGED] {mint} @ 300s → price=0")
                continue

            # Purge if it fails to hit 2× by 300 s
            if price_300s < 2 * initial_price:
                deadlist.append(mint)
                del data[mint]
                active_p1.remove(mint)
                log(f"[P1-PURGED] {mint} only {price_300s/initial_price:.2f}× @ 300s")
                continue

            # Survived & ≥ 2× → graduate into Phase 2
            active_p1.remove(mint)
            data[mint]["phase"] = 2
            data[mint].setdefault("price_log", []).append([now, price_300s])
            data[mint]["last_price"] = price_300s
            log(f"[P1-GRAD]  {mint} → Phase 2 (price=${price_300s:.8f}, {price_300s/initial_price:.2f}×)")

    # 4) Phase 2 → Phase 3 transition & purge at T = 1800 s
    for mint in list(active_p2):
        info = data[mint]
        age = now - info["mint_time"]
        if age >= P2_THRESHOLD:
            price_1800s = fetch_price(mint) or 0.0
            initial_price = info.get("initial_price", 0.0)
            ratio = price_1800s / initial_price if initial_price > 0 else 0.0

            # Purge if < 1.5× by 30 minutes
            if ratio < 1.5:
                deadlist.append(mint)
                del data[mint]
                active_p2.remove(mint)
                log(f"[P2-PURGED] {mint} only {ratio:.2f}× @ 1800s")
                continue

            # Survived & ≥ 1.5× → graduate to Phase 3
            active_p2.remove(mint)
            data[mint]["phase"] = 3
            data[mint].setdefault("price_log", []).append([now, price_1800s])
            data[mint]["last_price"] = price_1800s
            log(f"[P2-GRAD]  {mint} → Phase 3 (price=${price_1800s:.8f}, {ratio:.2f}×)")

    # 5) Phase 3 → Phase 4 transition & purge at T = 3600 s
    for mint in list(active_p3):
        info = data[mint]
        age = now - info["mint_time"]
        if age >= P3_THRESHOLD:
            price_3600s = fetch_price(mint) or 0.0
            initial_price = info.get("initial_price", 0.0)
            ratio = price_3600s / initial_price if initial_price > 0 else 0.0

            # Purge if < 1.2× by 60 minutes
            if ratio < 1.2:
                deadlist.append(mint)
                del data[mint]
                active_p3.remove(mint)
                log(f"[P3-PURGED] {mint} only {ratio:.2f}× @ 3600s")
                continue

            # Otherwise, graduate to Phase 4 (archive)
            active_p3.remove(mint)
            data[mint]["phase"] = 4
            data[mint]["phase4_start_time"]   = now
            data[mint]["phase4_initial_price"] = price_3600s
            data[mint].setdefault("price_log", []).append([now, price_3600s])
            data[mint]["last_price"] = price_3600s
            graduated[mint] = data[mint]
            del data[mint]
            log(f"[P3-GRAD]  {mint} → Phase 4 (price=${price_3600s:.8f}, {ratio:.2f}×)")

    # 6) Price updates & (optional) feature logging for tokens still in Phase 1–3
    for mint, info in data.items():
        phase, subidx = get_phase_and_subinterval(info, now)
        price = fetch_price(mint) or 0.0

        # Ensure price_log exists and append new tick
        if "price_log" not in info:
            info["price_log"] = []
        info["price_log"].append([now, price])

        # If this is the first time we see price>0, set initial_price if missing
        if "initial_price" not in info or info["initial_price"] == 0.0:
            # (however, we already set initial_price at mint-ingest)
            info["initial_price"] = price if price > 0 else 0.0

        # Update last_price
        info["last_price"] = price

        # ─────────────────────────────────────────────────────────────────────
        # OPTIONAL: Record sub‐interval‐specific features here. For example:
        # if phase == 1:
        #     # Each subidx ∈ [0..3] corresponds to P1_BINS (0–15 s, 15–60 s, …)
        #     bucket = info["phase1_data"].setdefault(subidx, {
        #         "volume_sol": 0.0,
        #         "buyers": set(),
        #         "slippage_samples": [],
        #     })
        #     # You could read from `live_ws_tokens.json` to see exactly which
        #     # vSolInBondingCurve / vTokensInBondingCurve changed in this bucket,
        #     # record that → bucket["volume_sol"] += delta_vsol, etc.
        # elif phase == 2:
        #     # Fill info["phase2_data"][subidx] = { … }
        #     pass
        # elif phase == 3:
        #     # Fill info["phase3_data"][subidx] = { … }
        #     pass
        # ─────────────────────────────────────────────────────────────────────

    # 7) Save everything back to disk
    save_json(WEIGHTS_PATH, data)
    save_json(DEADLIST_PATH, deadlist)
    save_json(GRAD_PATH, graduated)


def loop():
    log("🗜️  FunPurger daemon activated (multi‐phase).")
    while True:
        try:
            evaluate()
        except Exception as e:
            log(f"[ERROR] {e}")
        # Tight loop so we catch exact 300 s / 1800 s / 3600 s boundaries
        time.sleep(1)

if __name__ == "__main__":
    print("### FUN_PURGER_LOOP STARTED ###")
    loop()
