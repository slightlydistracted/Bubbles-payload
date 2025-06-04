
import json
import os
from collections import defaultdict

LEXICON_PATH = os.path.expanduser("~/feralsys/tools/black_swan_agent/lexicon_output.json")

def load_lexicon():
    with open(LEXICON_PATH, "r") as f:
        return json.load(f)

def analyze_drift(lexicon):
    term_usage = defaultdict(lambda: defaultdict(set))

    for file, contents in lexicon.items():
        for category, items in contents.items():
            for item in items:
                term_usage[category][item].add(file)

    drift_suspects = {}
    for category, terms in term_usage.items():
        normalized = defaultdict(list)
        for term in terms:
            base = term.replace("_", "").lower()
            normalized[base].append(term)

        for base_form, variants in normalized.items():
            if len(variants) > 1:
                drift_suspects[base_form] = variants

    return drift_suspects

if __name__ == "__main__":
    try:
        lexicon = load_lexicon()
        drift = analyze_drift(lexicon)
        if drift:
            print("[LEXICON VALIDATOR] Drift Detected:")
            for base, variants in drift.items():
                print(f"  - {base}: {', '.join(variants)}")
        else:
            print("[LEXICON VALIDATOR] No drift found. Terminology is consistent.")
    except Exception as e:
        print(f"[ERROR] Failed to validate lexicon: {e}")
