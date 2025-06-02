#!/data/data/com.termux/files/usr/bin/bash

INBOX_DIR="$HOME/feralsys/inbox"
LOG_DIR="$HOME/feralsys/logs"
MASTER_LOG="$LOG_DIR/master_coreloop.log"

mkdir -p "$LOG_DIR"

echo "[Auto Corelogic] Scanning inbox at $(date)" >> "$MASTER_LOG"

for file in "$INBOX_DIR"/*; do
    [ -f "$file" ] || continue  # Skip if not a regular file
    echo "[Processing] $file" >> "$MASTER_LOG"

    grep -v -e '^\s*$' -e '^\s*#' -e 'echo' "$file" >> "$MASTER_LOG"

    echo "[Finished] $file at $(date)" >> "$MASTER_LOG"
    echo "----------------------------------------" >> "$MASTER_LOG"
done
