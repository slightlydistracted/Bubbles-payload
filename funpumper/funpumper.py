import os, json, time
from datetime import datetime

# === PATHS ===
BASE = "/srv/daemon-memory/funpumper"
LOG_PATH = f"{BASE}/funpumper.log"
DATA_PATH = f"{BASE}/live_ws_tokens.json"
RESULT_PATH = f"{BASE}/funpumper_evals.json"
os.makedirs(BASE, exist_ok=True)

# === CONFIG ===
PREDICTION_WINDOW = 12 * 60 * 60  # 12 hours
SLEEP_INTERVAL = 600  # 10 minutes

# === LOGGING ===
def log(msg):
    ts = datetime.utcnow().isoformat()
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_PATH, "a") as f:
        f.write(line + "\n")

# === JSON UTIL ===
def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def load_json(path, default=[]):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return default

# === EVALUATION ===
def evaluate(tokens):
    now = int(time.time())
    results = load_json(RESULT_PATH, [])
    known = {r["mint"] for r in results}

    for mint, t in tokens.items():
        if mint in known:
            continue
        try:
            symbol = t.get("symbol", "???")
            price = float(t.get("initialBuy", 0))
            cap = float(t.get("marketCapSol", 0))
            launch_ts = now

            result = {
                "mint": mint,
                "symbol": symbol,
                "init_price": price,
                "init_mcap": cap,
                "launch_ts": launch_ts,
                "predicted_moon": cap < 5,
                "eval_due": now + PREDICTION_WINDOW,
                "status": "PENDING"
            }
            results.append(result)
            log(f"[NEW TOKEN] {mint} {symbol} added for eval")
        except Exception as e:
            log(f"[Eval FAIL: {mint}] {str(e)}")

    save_json(RESULT_PATH, results)
    save_json(DATA_PATH, tokens)

# === REEVALUATION ===
def reevaluate():
    now = int(time.time())
    results = load_json(RESULT_PATH, [])
    tokens = load_json(DATA_PATH, {})

    updated = []

    for r in results:
        if r["status"] != "PENDING" or now < r["eval_due"]:
            updated.append(r)
            continue

        mint = r["mint"]
        if mint not in tokens:
            r["status"] = "FAILED"
            r["reason"] = "GONE_OR_DELISTED"
        else:
            t = tokens[mint]
            try:
                price_now = float(t.get("initialBuy", 0))
                cap_now = float(t.get("marketCapSol", 0))
                price_ratio = price_now / max(r["init_price"], 1e-6)

                if price_ratio >= 10:
                    r["status"] = "MOON"
                    r["final_price"] = price_now
                    r["final_cap"] = cap_now
                elif price_ratio <= 0.2:
                    r["status"] = "CRASHED"
                    r["reason"] = "PRICE_DROP"
                elif cap_now < r["init_mcap"] and cap_now < 1:
                    r["status"] = "CRASHED"
                    r["reason"] = "VOLUME_DIED"
                else:
                    r["status"] = "STABLE"
                    r["final_price"] = price_now
                    r["final_cap"] = cap_now
            except Exception as e:
                r["status"] = "FAILED"
                r["reason"] = str(e)
        updated.append(r)

    save_json(RESULT_PATH, updated)

# === MAIN LOOP ===
def loop():
    log("FunPumper evaluator active.")
    while True:
        reevaluate()
        tokens = load_json(DATA_PATH, {})
        evaluate(tokens)
        time.sleep(SLEEP_INTERVAL)

if __name__ == "__main__":
    loop()
