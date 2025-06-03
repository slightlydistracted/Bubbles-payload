import asyncio
import datetime
import os
from mutation_engine import apply_mutations


async def update_prices():
    try:
        os.system("python3 price_fetcher.py")
    except Exception as e:
        print("[ERROR during price update]", e)


async def generate_daily_report():
    try:
        os.system("python3 daily_reporter.py")
    except Exception as e:
        print("[ERROR during daily report]", e)


async def simulate_buy():
    print("[SIMULATED BUY] Placeholder executed.")


async def simulate_sell():
    print("[SIMULATED SELL] Placeholder executed.")


async def heartbeat():
    print("[HEARTBEAT]", datetime.datetime.utcnow().isoformat())
    await update_prices()
    await generate_daily_report()
    await simulate_buy()
    await simulate_sell()
    apply_mutations()


async def main_loop():
    while True:
        await heartbeat()
        await asyncio.sleep(300)  # 5 minutes between heartbeats

if __name__ == "__main__":
    asyncio.run(main_loop())
