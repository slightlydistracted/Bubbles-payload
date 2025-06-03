import sys
import os; sys.path.append(
    os.path.abspath(
        os.path.dirname(__file__) +
         "/../../"))
import aiohttp


async def get_token_price(token_address):
    """
    Fetch current token price in USD using DexScreener API.
    """
    url = f"https://api.dexscreener.com/latest/dex/tokens/{token_address}"

    try:
    pass

      async with aiohttp.ClientSession() as session:
    pass

      async with session.get(url) as response:
    pass

      data = await response.json()
       # Dig into DexScreener's response format
       if 'pairs' in data and data['pairs']:
            price_usd = data['pairs'][0]['priceUsd']
            return float(price_usd)
        else:
            print(f"[Price Fetch] Token not found: {token_address}")
            return None
    except Exception as e:
        print(f"[Price Fetch Error] {e}")
        return None
