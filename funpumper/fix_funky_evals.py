#!/usr/bin/env python3
import json
from pathlib import Path

# Overwrite the canonical evals file in place
EVALS_PATH = Path("/srv/daemon-memory/funpumper/funpumper_evals.json")

def fix():
    try:
        raw = json.loads(EVALS_PATH.read_text())
        fixed = []

        if isinstance(raw, dict):
            # { mint: { … } } form
            for mint, val in raw.items():
                if isinstance(val, dict):
                    entry = dict(val)
                    entry.setdefault("mint", mint)
                    entry.setdefault("status", "PENDING")
                    fixed.append(entry)
                elif isinstance(val, str):
                    fixed.append({"mint": val, "status": "PENDING"})

        elif isinstance(raw, list):
            # [ { … }, { … } ] or [ "mint1", "mint2" ]
            for val in raw:
                if isinstance(val, dict):
                    val.setdefault("status", "PENDING")
                    fixed.append(val)
                elif isinstance(val, str):
                    fixed.append({"mint": val, "status": "PENDING"})

        else:
            print(f"[ERROR] Unrecognized JSON structure: {type(raw)}")
            return

        # Write back the cleaned-up list
        EVALS_PATH.write_text(json.dumps(fixed, indent=2))
        print(f"[OK] Normalized evals written to {EVALS_PATH}")

    except Exception as e:
        print(f"[ERROR] Fixer failed: {e}")

if __name__ == "__main__":
    fix()
