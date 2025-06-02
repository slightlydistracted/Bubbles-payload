#!/bin/bash
# Remote Sync Loop - Bubbles Mode

echo "[remote_sync] Active: $(date)" >> ~/feralsys/logs/remote_sync.log

while true; do
    echo "[remote_sync] $(date) - Syncing sandbox..." >> ~/feralsys/logs/remote_sync.log
    find ~/feralsys/inbox/ -mindepth 1 -exec cp -r {} ~/feralsys/sandbox/ \;
    sleep 60
done
