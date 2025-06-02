import time
import shutil
from pathlib import Path

INBOXES = [
    Path.home() / "feralsys/inbox",
    Path("/sdcard/Download/")
]

PROCESSED = Path.home() / "feralsys/inbox/processed"
LOGFILE = Path.home() / "feralsys/lilith_inbox.log"
MAX_LOG_SIZE = 1024 * 1024  # 1MB max log file size

def log(message):
    try:
        if LOGFILE.exists() and LOGFILE.stat().st_size > MAX_LOG_SIZE:
            LOGFILE.write_text("")  # clear log if too big
        with open(LOGFILE, "a") as f:
            f.write(f"[Lilith Inbox] {message}\n")
    except Exception as e:
        print(f"[Lilith Logging ERROR] {e}")

def process_file(file_path):
    try:
        target_path = PROCESSED / file_path.name
        shutil.move(str(file_path), str(target_path))
        log(f"Processed {file_path}")
    except Exception as e:
        log(f"Error processing {file_path}: {e}")

def main():
    PROCESSED.mkdir(parents=True, exist_ok=True)
    while True:
        for inbox in INBOXES:
            if inbox.exists():
                for item in inbox.iterdir():
                    if item.is_file() and not item.name.startswith("."):
                        process_file(item)
        time.sleep(0.5)  # sniper-speed polling

if __name__ == "__main__":
    main()
