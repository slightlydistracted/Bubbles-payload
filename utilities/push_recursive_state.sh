#!/bin/bash

cd ~/projects/Bubbles-payload || exit 1

# Copy state into Git-visible repo
cp /srv/daemon-memory/bubbles_state/bubbles_recursive_state.json ./bubbles_recursive_state.json
cp /srv/daemon-memory/bubbles_state/version_log.json ./version_log.json

# Commit and push
git add bubbles_recursive_state.json version_log.json
git commit -m "[AUTO] Recursive state update $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
git push origin main
