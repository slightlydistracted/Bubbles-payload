
import json
import asyncio
from live_price_fetcher import get_token_price

SIMULATED_PORTFOLIO_PATH = "simulated_portfolio.json"

async def buy_token_if_black_swan(receiver_address, fake_amount, fake_price, memory):
    if is_black_swan(receiver_address, memory):
        print(f"[BLACK SWAN] ALERT: {receiver_address} flagged as suspicious. Halting trade.")
        return

    await buy_token(receiver_address, fake_amount, fake_price)

def is_black_swan(token_address, memory):
    return token_address in memory.get("blacklist", [])

async def buy_token(receiver_address, fake_amount, fake_price):
    await record_simulated_buy(receiver_address, fake_amount, fake_price)

async def record_simulated_buy(token_address, amount, price):
    try:
        with open(SIMULATED_PORTFOLIO_PATH, "r") as f:
            portfolio = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        portfolio = {"tokens": []}

    portfolio["tokens"].append({
        "timestamp": asyncio.get_event_loop().time(),
        "token_address": token_address,
        "amount_purchased": amount,
        "price_at_purchase": price,
        "investment_fake_usd": amount * price,
        "current_price": await get_token_price(token_address) or 0.0
    })

    with open(SIMULATED_PORTFOLIO_PATH, "w") as f:
        json.dump(portfolio, f, indent=2)
