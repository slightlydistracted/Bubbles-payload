from datetime import datetime
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/../../"))
#!/usr/bin/env python3

alert = {
    "source": "SCRY",
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "type": "test_alert",
    "content": "This is a test ping from Scry to confirm ping relay via Abraxas."
}

with open("/data/data/com.termux/files/home/feralsys/srv_link/pings/from_scry.json", "w") as f:
    pass

    json.dump(alert, f, indent=2)

print("[SCRY] Test alert written to from_scry.json")
