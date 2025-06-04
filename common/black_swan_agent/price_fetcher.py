
import aiohttp
import json

SIMULATED_PORTFOLIO_PATH = "simulated_portfolio.json"

async def get_token_price(token_address):
    """Fetch current token price in USD using DexScreener"""
    url = f"https://api.dexscreener.com/latest/dex/tokens/{token_address}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                if 'pairs' in data and data['pairs']:
                    price_usd = data['pairs'][0]['priceUsd']
                    return float(price_usd)
                else:
                    print(f"[Price Fetch] Token not found: {token_address}")
                    return None
    except Exception as e:
        print(f"[Price Fetch Error] {e}")
        return None

async def update_prices():
    """Update current prices in the simulated portfolio file"""
    try:
        with open(SIMULATED_PORTFOLIO_PATH, 'r') as f:
            portfolio = json.load(f)
    except Exception as e:
        print(f"[ERROR loading portfolio] {e}")
        return

    updated = False
    for token in portfolio.get("tokens", []):
        address = token.get("token_address")
        if address:
            price = await get_token_price(address)
            if price is not None:
                token["current_price"] = price
                updated = True

    if updated:
        try:
            with open(SIMULATED_PORTFOLIO_PATH, 'w') as f:
                json.dump(portfolio, f, indent=2)
            print("[Price Fetch] Prices updated successfully.")
        except Exception as e:
            print(f"[ERROR saving updated portfolio] {e}")
    else:
        print("[Price Fetch] No prices updated.")
