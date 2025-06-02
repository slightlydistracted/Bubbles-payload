# telemetry_clock_sync.py

import time
import json
import requests
from datetime import datetime, timezone

def get_network_utc():
    try:
        response = requests.get("http://worldtimeapi.org/api/timezone/Etc/UTC", timeout=4)
        if response.status_code == 200:
            net_time = response.json()["utc_datetime"]
            return datetime.fromisoformat(net_time.replace("Z", "+00:00"))
    except Exception as e:
        return None

def get_local_utc():
    return datetime.utcnow().replace(tzinfo=timezone.utc)

def measure_time_drift():
    local = get_local_utc()
    network = get_network_utc()
    if local and network:
        drift = (local - network).total_seconds()
        return {
            "local_time": local.isoformat(),
            "network_time": network.isoformat(),
            "drift_seconds": round(drift, 4),
            "status": (
                "OK" if abs(drift) < 1.0 else
                "WARNING" if abs(drift) < 5.0 else
                "CRITICAL"
            )
        }
    else:
        return {
            "local_time": str(local) if local else "ERROR",
            "network_time": str(network) if network else "ERROR",
            "drift_seconds": None,
            "status": "ERROR"
        }

if __name__ == "__main__":
    drift_info = measure_time_drift()
    print(json.dumps(drift_info, indent=2))
