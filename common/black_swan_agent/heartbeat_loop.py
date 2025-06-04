
import asyncio
import json
from datetime import datetime

from trade_executor import buy_token_if_black_swan
from mutation_memory import load_memory, save_memory
from mutation_engine import apply_mutations
from mutation_evaluator import evaluate_mutations
from live_price_fetcher import fetch_live_price
from learned_patterns import load_patterns
from journal_engine import write_daily_journal

SIMULATED_PORTFOLIO_PATH = "/root/feralsys/tools/black_swan_agent/simulated_portfolio.json"

async def heartbeat():
    print(f"[HEARTBEAT] {datetime.utcnow().isoformat()}")
    memory = load_memory()
    new_mutations = apply_mutations(memory)
    save_memory(memory)

    try:
        with open(SIMULATED_PORTFOLIO_PATH, "r") as f:
            portfolio_data = json.load(f)
        tokens = portfolio_data.get("tokens", [])
    except Exception as e:
        print("[ERROR loading portfolio]", e)
        tokens = []

    current_prices = {}
    for token in tokens:
        addr = token.get("token_address")
        if not addr:
            continue
        price = await fetch_live_price(addr)
        if price:
            token["current_price"] = price
            current_prices[addr] = price

    with open(SIMULATED_PORTFOLIO_PATH, "w") as f:
        json.dump(portfolio_data, f, indent=2)

    evaluation_log, updated_memory = evaluate_mutations(memory.get("mutations", []), tokens, current_prices, memory)
    save_memory(updated_memory)

    print("[Portfolio Value]")
    total_value = sum(token.get("current_price", 0) * token.get("amount_purchased", 0) for token in tokens)
    print(f"Total: ${total_value:.4f}")
    for token in tokens:
        print(f"{token['token_address'][-6:]}: ${token.get('current_price', 0):.4f}")

    # Log journal
    patterns = load_patterns()
    journal_path = write_daily_journal(tokens, updated_memory, patterns)
    print(f"[Journal Saved] {journal_path}")

if __name__ == "__main__":
    asyncio.run(heartbeat())
