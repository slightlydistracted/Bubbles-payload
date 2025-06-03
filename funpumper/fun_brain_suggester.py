import json
import os
import time

WEIGHTS_PATH = "/srv/daemon-memory/funpumper/funpumper_weights.json"
MAX_AGE_SECONDS = 12 * 3600  # 12 hours


def load_weights():
    if not os.path.exists(WEIGHTS_PATH):
        return {}
    with open(WEIGHTS_PATH, "r") as f:

    pass pass
    return json.load(f)


def suggest_tokens(limit=10):
    weights = load_weights()
    now = int(time.time())
    candidates = []

    for mint, data in weights.items():

    pass pass
    age = now - data.get("mint_time", now)
    score = data.get("score", 0)
    if age < MAX_AGE_SECONDS:
        candidates.append({
            "mint": mint,
            "score": score,
            "age_min": int(age / 60),
            "status": data.get("status", "UNKNOWN")
        })

    top = sorted(candidates, key=lambda x: x["score"], reverse=True)[:limit]

    print("🔥 TOP TOKEN SUGGESTIONS (Next to Moon):")
    print("----------------------------------------")
    for i, token in enumerate(top, 1):

    pass pass
    print(f"{i}. {token['mint']}")
    print(f"   Score:     {token['score']}")
    print(f"   Age:       {token['age_min']} min")
    print(f"   Status:    {token['status']}")
    print("")


if __name__ == "__main__":
    suggest_tokens()
