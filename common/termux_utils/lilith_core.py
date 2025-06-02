import os
import time
import subprocess
import requests

INBOX_DIR = os.path.expanduser("~/feralsys/inbox/")
PROCESSED_DIR = os.path.join(INBOX_DIR, "processed")
LOG_PATH = os.path.expanduser("~/feralsys/logs/lilith_push.log")
LOCK_PATH = os.path.expanduser("~/feralsys/lilith_core.lock")
HEARTBEAT_PATH = os.path.expanduser("~/feralsys/lilith_heartbeat.txt")

REMOTE_HOST = "188.245.87.243"
REMOTE_USER = "root"
REMOTE_PATH = "/data/data/com.termux/files/home/feralsys/shadow_srv/daemon-memory/"
KEY_PATH = os.path.expanduser("~/.ssh/id_rsa")

# Telegram credentials
BOT_TOKEN = "8090852179:AAE4xSKKs2T5AAapWVzOIuwEq3NVLXvLSnc"
CHAT_ID = "8071168808"

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_PATH, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(f"[{timestamp}] {msg}")

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": msg}
        requests.post(url, data=payload, timeout=5)
    except Exception as e:
        log(f"[TELEGRAM FAIL] {e}")

def push_file_to_abraxas(file_path):
    filename = os.path.basename(file_path)
    scp_cmd = f"scp -i {KEY_PATH} {file_path} {REMOTE_USER}@{REMOTE_HOST}:{REMOTE_PATH}"
    try:
        subprocess.run(scp_cmd, shell=True, check=True)
        log(f"[PUSHED] {filename}")
        send_telegram(f"[Lilith Push] {filename} → Abraxas [OK]")
        return True
    except subprocess.CalledProcessError as e:
        log(f"[ERROR] SCP failed for {filename}: {e}")
        send_telegram(f"[Lilith Push] {filename} → FAILED")
        return False

def write_lock():
    with open(LOCK_PATH, "w") as f:
        f.write(str(os.getpid()))

def update_heartbeat():
    with open(HEARTBEAT_PATH, "w") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S"))

def monitor_inbox():
    write_lock()
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    while True:
        update_heartbeat()
        for file in os.listdir(INBOX_DIR):
            if file.endswith(".py") or file.endswith(".json"):
                full_path = os.path.join(INBOX_DIR, file)
                success = push_file_to_abraxas(full_path)
                if success:
                    os.rename(full_path, os.path.join(PROCESSED_DIR, file))
        time.sleep(10)

if __name__ == "__main__":
    monitor_inbox()
