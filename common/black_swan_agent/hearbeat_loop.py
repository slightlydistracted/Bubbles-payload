import asyncio
import json
from datetime import datetime
from mutation_memory import load_memory
from mutation_engine import evaluate_mutations

SIMULATED_PORTFOLIO_PATH = "/root/feralsys/tools/black_swan_agent/simulated_portfolio.json"

async def heartbeat():
    print(f"[HEARTBEAT] {datetime.utcnow().isoformat()}")

    try:
        memory = load_memory()
    except Exception as e:
        print("[ERROR loading memory]", e)
        memory = {"mutations": [], "history": []}

    try:
        with open(SIMULATED_PORTFOLIO_PATH, "r") as f:
            portfolio_data = json.load(f)
        tokens = portfolio_data.get("tokens", [])
    except Exception as e:
        print("[ERROR loading portfolio]", e)
        tokens = []

    try:
        mutation_log = evaluate_mutations(tokens, memory)
        print(f"[MUTATION LOG] {mutation_log}")
    except Exception as e:
        print("[ERROR during mutation evaluation]", e)

if __name__ == "__main__":
    asyncio.run(heartbeat())
