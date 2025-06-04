import asyncio
import json
from alpha_extractor import extract_alpha_signals
from budget_manager import initialize_budget, update_budget, is_budget_exhausted, reset_budget, get_budget_log
from mutation_engine import apply_mutation_strategies
from journal_engine import write_daily_journal
from mutation_memory import load_memory, save_memory
from reinforcement_engine import reinforce_alpha_signals
from simulation_planner import simulate_run
from adaptive_thresholds import load_thresholds
from wallet_tracker import track_whale_wallets
from strategy_weaver import weave_strategy
from trade_executor import buy_token_if_black_swan

budget = initialize_budget(100.0)
memory = load_memory()
thresholds = load_thresholds()
portfolio = {"tokens": []}
mutation_log = []

async def ignition_cycle():
    global budget, memory, portfolio, mutation_log
    alpha_signals = extract_alpha_signals(mutation_log, portfolio.get("tokens", []))
    reinforce_alpha_signals()
    simulate_run(memory, portfolio.get("tokens", []))
    strategy = weave_strategy(alpha_signals)
    portfolio["tokens"], spent = apply_mutation_strategies(strategy, portfolio["tokens"])
    budget = update_budget(budget, -spent)
    if is_budget_exhausted(budget):
        write_daily_journal(portfolio, memory, mutation_log, budget)
        budget = reset_budget(100.0)
        memory = load_memory()
        portfolio = {"tokens": []}
        mutation_log.clear()

async def main_loop():
    while True:
        await ignition_cycle()
        await asyncio.sleep(3)

if __name__ == "__main__":
    print("[IGNITION] Starting autonomous loop...")
    print(f"[IGNITION] Portfolio value: ${budget['amount']:.2f}")
    asyncio.run(main_loop())
