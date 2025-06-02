#!/usr/bin/env bash
# Synchronize system time via NTP
echo "[SYNC_TIME] Syncing clock..."
ntpdate -u pool.ntp.org
