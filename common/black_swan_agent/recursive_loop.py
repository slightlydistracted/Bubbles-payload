
import asyncio
from mutation_memory import load_memory, save_memory
from learned_patterns import load_patterns
from journal_engine import write_daily_journal
from alpha_extractor import extract_alpha_signals
from reinforcement_engine import reinforce_alpha_signals
from simulation_planner import simulate_run
from simulation_evaluator import evaluate_simulation
from adaptive_thresholds import adjust_thresholds, load_thresholds
from wallet_tracker import track_whale_wallets
from strategy_weaver import weave_strategy
import json
import os

SIMULATED_PORTFOLIO_PATH = os.path.expanduser("~/feralsys/tools/black_swan_agent/simulated_portfolio.json")
MUTATION_LOG_PATH = os.path.expanduser("~/feralsys/tools/black_swan_agent/reports/mutation_log.json")
ALPHA_PATH = os.path.expanduser("~/feralsys/tools/black_swan_agent/alpha_signals.json")

async def recursive_loop():
    memory = load_memory()
    patterns = load_patterns()

    # Load portfolio snapshot
    try:
        with open(SIMULATED_PORTFOLIO_PATH, "r") as f:
            portfolio = json.load(f).get("tokens", [])
    except Exception:
        portfolio = []

    portfolio_value = sum(t.get("current_price", 0) * t.get("amount_purchased", 0) for t in portfolio)

    # Simulate
    simulation_result = simulate_run(memory, portfolio_value)
    evaluation = evaluate_simulation([{"net_gain": simulation_result["score"], "trades": simulation_result["mutation_count"]}])
    thresholds = adjust_thresholds(evaluation["win_rate"])

    # Alpha & Reinforcement
    try:
        with open(MUTATION_LOG_PATH, "r") as f:
            mutation_log = json.load(f)
    except Exception:
        mutation_log = []

    alpha_signals = extract_alpha_signals(mutation_log, portfolio)
    with open(ALPHA_PATH, "w") as f:
        json.dump({"alpha_signals": alpha_signals}, f, indent=2)

    reinforce_alpha_signals()
    whale_data = await track_whale_wallets()
    strategy = weave_strategy(memory.get("mutations", []), alpha_signals, whale_data, thresholds)

    print(f"[Strategy Drafted] Risk Mode: {strategy['risk']} | Buys: {strategy['buy'][:3]}")
    write_daily_journal(portfolio, memory, patterns)

if __name__ == "__main__":
    asyncio.run(recursive_loop())
