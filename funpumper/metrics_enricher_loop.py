#!/usr/bin/env python3

import os
import json
import time
import threading
import requests
from datetime import datetime

# ── Configuration ──────────────────────────────────────────────────────────────

API_KEY = "1dc0efc3-6f32-4590-8b06-e2fd8bb46f03"
EVALS_PATH = "/srv/daemon-memory/funpumper/fixed_evals.json"
LOG_PATH = "/srv/daemon-memory/funpumper/metrics_enricher.log"

# HOW MANY HELIUS REQUESTS TOTAL per second (shared across get_price + get_activity)
HELIUS_RATE_LIMIT = 2    # 2 requests per second
HELIUS_RATE_PERIOD_SEC = 1.0  # period over which that applies

# How long to wait after fully processing each token, to further spread out calls
TOKEN_PAUSE_SEC = 0.3

# ── Rate Limiter Definition ────────────────────────────────────────────────────


class RateLimiter:
    """
    Simple token‐bucket rate limiter: allows `rate` calls per `per` seconds total.
    """

    def __init__(self, rate, per):
        self.rate = float(rate)
        self.per = float(per)
        self.allowance = float(rate)
        self.last_check = time.time()
        self.lock = threading.Lock()

    def acquire(self):
        with self.lock:
            current = time.time()
            elapsed = current - self.last_check
            self.last_check = current
            # refill allowance
            self.allowance += elapsed * (self.rate / self.per)
            if self.allowance > self.rate:
                self.allowance = self.rate

            if self.allowance < 1.0:
                needed = 1.0 - self.allowance
                sleep_time = needed * (self.per / self.rate)
                time.sleep(sleep_time)
                self.allowance = 0.0
            else:
                self.allowance -= 1.0


# Single global limiter for all Helius calls
limiter = RateLimiter(rate=HELIUS_RATE_LIMIT, per=HELIUS_RATE_PERIOD_SEC)

# ── Logging Utility ─────────────────────────────────────────────────────────────


def log(message):
    """
    Append a timestamped message to metrics_enricher.log.
    """
    ts = datetime.utcnow().isoformat()
    with open(LOG_PATH, "a") as f:
        f.write(f"[{ts}] {message}\n")

# ── Load Eval List Safely ────────────────────────────────────────────────────────


def load_evals():
    """
    Read fixed_evals.json, return list of token dicts. If JSON is malformed or missing,
    return empty list and log an error.
    """
    if not os.path.exists(EVALS_PATH):
        return []
    try:
        with open(EVALS_PATH, "r") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        log(f"[ERROR] Failed to load evals: {e}")
        return []
    except Exception as e:
        log(f"[ERROR] Unexpected error loading evals: {e}")
        return []

# ── Helius Wrappers (Rate‐Limited) ────────────────────────────────────────────────


def get_price(mint):
    """
    Fetch on-chain price from Helius for `mint`. Returns price or None.
    """
    try:
        limiter.acquire()
        url = f"https://api.helius.xyz/v0/tokens/{mint}/price"
        params = {"api-key": API_KEY}
        r = requests.get(url, params=params, timeout=5)

        if r.status_code == 404:
            log(f"[WARN] price not available for {mint} (404)")
            return None

        r.raise_for_status()
        j = r.json()
        return j.get("price")

    except requests.exceptions.HTTPError as e:
        code = e.response.status_code if e.response else None
        if code == 429:
            log(
                f"[WARN] rate-limited fetching price for {mint} (429), backing off 5s")
            time.sleep(5)
            return None
        log(f"[ERROR] price lookup failed for {mint}: {e}")
        return None

    except Exception as e:
        log(f"[ERROR] get_price {mint}: {e}")
        return None


def get_activity(mint):
    """
    Fetch up to 10 'TRANSFER' transactions for `mint` from Helius. Returns count or 0.
    """
    try:
        limiter.acquire()
        url = f"https://api.helius.xyz/v0/addresses/{mint}/transactions"
        params = {"type": "TRANSFER", "limit": 10, "api-key": API_KEY}
        r = requests.get(url, params=params, timeout=5)

        if r.status_code == 404:
            log(f"[WARN] activity not available for {mint} (404)")
            return 0

        r.raise_for_status()
        j = r.json()
        return len(j.get("result", []))

    except requests.exceptions.HTTPError as e:
        code = e.response.status_code if e.response else None
        if code == 429:
            log(
                f"[WARN] rate-limited fetching activity for {mint} (429), backing off 5s")
            time.sleep(5)
            return 0
        log(f"[ERROR] get_activity {mint}: {e}")
        return 0

    except Exception as e:
        log(f"[ERROR] get_activity {mint}: {e}")
        return 0

# ── Main Loop: Oldest‐First with Pauses ───────────────────────────────────────────


def main_loop():
    log("Live metrics enricher loop started.")

    while True:
        evals = load_evals()

        # Sort by “created_at” if it exists, oldest (smallest) first
        try:
            evals_sorted = sorted(
                evals,
                key=lambda t: t.get("created_at", float("inf"))
            )
        except Exception:
            evals_sorted = evals

        for token in evals_sorted:
            mint = token.get("mint")
            if not mint:
                continue

            price = get_price(mint)
            activity = get_activity(mint)
            log(f"[UPDATE] {mint} → price={price} act={activity}")

            # Pause briefly before next token to spread calls further
            time.sleep(TOKEN_PAUSE_SEC)

        # After the entire list, wait 60 seconds before re‐running
        time.sleep(60)


if __name__ == "__main__":
    main_loop()
