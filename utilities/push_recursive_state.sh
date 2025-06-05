#!/bin/bash

# Set variables
STATE_DIR="/root/projects/Bubbles-payload/Bubbles_state"
DEST_DIR="/root/projects/Bubbles-payload"

# File paths
STATE_JSON="$STATE_DIR/bubbles_recursive_state.json"
VERSION_JSON="$STATE_DIR/version_log.json"

# Check both files exist
if [ ! -f "$STATE_JSON" ] || [ ! -f "$VERSION_JSON" ]; then
  echo "[ERROR] One or more required files not found:"
  echo "  Missing: $STATE_JSON or $VERSION_JSON"
  exit 1
fi

# Copy into GitHub-visible repo root (if needed)
cp "$STATE_JSON" "$DEST_DIR/"
cp "$VERSION_JSON" "$DEST_DIR/"

cd "$DEST_DIR" || exit 1

# Stage for Git commit
git add bubbles_recursive_state.json version_log.json

# Commit and push
git commit -m "Recursive state + version log update: $(date -u +'%Y-%m-%d %H:%M:%S UTC')"
git push origin main
