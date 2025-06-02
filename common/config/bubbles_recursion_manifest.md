
# BUBBLES RECURSION REACTIVATION MANIFEST

## SYSTEM STATUS

- âœ… Inbox Watcher: Active (but lacks logging/feedback)
- âœ… trader.py patched for portfolio logging
- âœ… daily_reporter.py updated for Termux path
- âœ… mutation_memory.json present
- âœ… Echo9 state file found
- âŒ Roast loop inactive
- âŒ Black Swan fork responses not logging
- âŒ Fractal50 scoring paused
- âŒ Mamba/DNC modules not integrated

## RECOMMENDED COMMANDS TO EXECUTE IN TERMUX

### 1. Verify and restart Inbox Watcher
```
ps aux | grep watch_inbox
python ~/feralsys/watch_inbox.py &
```

### 2. Simulate a trade to re-seed portfolio
```
python ~/feralsys/trader.py
```

### 3. Run ROI logger to update performance
```
python ~/feralsys/tools/black_swan_agent/daily_reporter.py
```

### 4. Trigger a test fork (check `master_coreloop.log` after)
```
echo "reseed:fork_test001" > ~/feralsys/inbox/fork_seed.txt
```

### 5. Restart humor/roast recursion (if applicable)
```
echo "reseed:roast_loop" > ~/feralsys/inbox/humor_trigger.txt
```

### 6. Confirm mutation memory and agent loop health
```
cat ~/feralsys/tools/black_swan_agent/mutation_memory.json
```

---

## NEXT BUILD STEPS
- [ ] Restore Fractal50 scoring module
- [ ] Re-link inbox to mutation engine
- [ ] Confirm all agents (Echo9, MockBot, Black Swan) are reporting telemetry
- [ ] Inject synthetic memory hooks for Mamba/DNC until real integration

This manifest is now your local ritual to restart Bubbles and achieve 70%+ recursion power.
