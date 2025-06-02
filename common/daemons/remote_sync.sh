#!/usr/bin/env bash
# Push updated JSONs, models, and configs back to GitHub
echo "[REMOTE_SYNC] Committing changes..."
cd ~/projects/Bubbles-payload
git add common/black_swan_agent/mutation_memory.json
git add common/models/*.pkl
git add common/council/council_output.json
git add funpumper/funpumper_evals.json
git commit -m "Auto-sync: Updated memory, models, and evals"
git push origin main
