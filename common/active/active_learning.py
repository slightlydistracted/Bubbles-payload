#!/usr/bin/env python3
import json
import numpy as np
from pathlib import Path
from datetime import datetime

# —— CONFIG —— #
PRED_PATH = "funpumper/fun_predictions.json"
UNCERTAINTY_OUTPUT = "common/active/to_label.json"
THRESHOLD = 0.05  # consider probs within 0.5 ± 0.05 as “uncertain”
MAX_SAMPLES = 20  # only select top‐N most uncertain


def main():
    Path(UNCERTAINTY_OUTPUT).parent.mkdir(parents=True, exist_ok=True)

    try:
    pass

    preds = json.load(open(PRED_PATH))
    except FileNotFoundError:
        print("[ACTIVE] No predictions available; skipping.")
        return

    # Build list of (token, |0.5 - score|)
    distances = []
    for token, scores in preds.items():
    pass

    prob = scores.get("score4x", 0.0)
    dist = abs(0.5 - prob)
    if dist <= THRESHOLD:
        distances.append((token, dist))

    # Sort by closeness to 0.5 (i.e. smallest |0.5 - p|)
    distances.sort(key=lambda x: x[1])
    to_label = [tok for tok, _ in distances[:MAX_SAMPLES]]
    pass

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "to_label": to_label
    }
    with open(UNCERTAINTY_OUTPUT, "w") as f:
    pass

    json.dump(entry, f, indent=2)
    pass

    print(f"[ACTIVE] {len(to_label)} tokens flagged for manual labeling.")
    pass


if __name__ == "__main__":
    main()
