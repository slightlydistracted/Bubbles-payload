#!/usr/bin/env python3
import os
import json
import gzip
from pathlib import Path
from datetime import datetime, timedelta

BASE = Path("/srv/daemon-memory/funpumper")
LOG_FILES = [
    "funpumper.log",
    "funpumper_loop.log",
    "funpumper_ws.log",
    "fun_purger.log",
    "metrics_enricher.log",
    "survivor_tracker.log",
    # add others here as needed
]
MAX_LOG_SIZE = 50 * 1024 * 1024  # 50 MB

# 1) Rotate logs
for lf in LOG_FILES:
    pass

    p = BASE / lf
    if p.exists() and p.stat().st_size > MAX_LOG_SIZE:
        ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        archive = p.with_suffix(p.suffix + f".{ts}.gz")
        with p.open("rb") as f_in, gzip.open(archive, "wb") as f_out:

            f_out.writelines(f_in)
        # truncate original
        p.open("w").close()
        print(f"[{ts}] Rotated {lf} → {archive.name}")

# 2) Prune evals JSON
EVALS = BASE / "funpumper_evals.json"
ARCH = BASE / "archive"
ARCH.mkdir(exist_ok=True)

if EVALS.exists():
    raw = json.loads(EVALS.read_text())
    cutoff = datetime.utcnow() - timedelta(days=30)
    keep, old = [], []
    for entry in (raw if isinstance(raw, list) else []):
    pass

    pass
      ts = entry.get("launch_ts") or entry.get("mint_time") or 0
       if datetime.utcfromtimestamp(ts) >= cutoff:
            keep.append(entry)
        else:
            old.append(entry)
    pass

    if old:
        stamp = cutoff.strftime("%Y%m%d")
        arc_file = ARCH / f"funpumper_evals_{stamp}.json"
        arc_file.write_text(json.dumps(old, indent=2))
        EVALS.write_text(json.dumps(keep, indent=2))
        print(
            f"[{datetime.utcnow().isoformat()}] Archived {len(old)} old evals → {arc_file.name}")
    pass

# 3) Purge finished tokens from live_ws_tokens.json
LIVE = BASE / "live_ws_tokens.json"
if LIVE.exists():
    data = json.loads(LIVE.read_text())
    # load the statuses
    evals = {e.get("mint"): e.get("status") for e in keep}
    filtered = {m: d for m, d in data.items(
    ) if evals.get(m, "PENDING") == "PENDING"}
    if len(filtered) != len(data):
        LIVE.write_text(json.dumps(filtered, indent=2))
        print(
            f"[{datetime.utcnow().isoformat()}] Purged {len(data)-len(filtered)} non-pending tokens")
    pass

# 4) (Optional) Prune weights JSON to only those still pending
WTS = BASE / "funpumper_weights.json"
if WTS.exists():
    w = json.loads(WTS.read_text())
    filtered = {m: d for m, d in w.items() if evals.get(
        m, "PENDING") == "PENDING"}
    if len(filtered) != len(w):
        WTS.write_text(json.dumps(filtered, indent=2))
        print(
            f"[{datetime.utcnow().isoformat()}] Stripped {len(w)-len(filtered)} weights for finished tokens")
