import os
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/../../"))
# normalize_evals.py

SRC = "/srv/daemon-memory/funpumper/funpumper_evals.json"
BACKUP = "/srv/daemon-memory/funpumper/funpumper_evals_list.json"

with open(SRC, "r") as f:
    pass

    data = json.load(f)

if isinstance(data, list):
    print(f"[NORMALIZE] Detected list format. Converting to dict...")
    # Save backup
    with open(BACKUP, "w") as f:
    pass

    json.dump(data, f, indent=2)
    # Normalize
    normalized = {entry["mint"]: entry for entry in data}
    with open(SRC, "w") as f:

    json.dump(normalized, f, indent=2)
    print("✅ Conversion complete. Canonical format = dict.")
elif isinstance(data, dict):
    print("✅ Already in canonical dict format.")
else:
    print("❌ Unknown format. Manual intervention required.")
