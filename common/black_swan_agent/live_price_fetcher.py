
import aiohttp

async def get_token_price(token_address):
    url = f"https://api.dexscreener.com/latest/dex/tokens/{token_address}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                if 'pairs' in data and data['pairs']:
                    price_usd = data['pairs'][0]['priceUsd']
                    return float(price_usd)
                else:
                    print(f"[Live Price] Token not found: {token_address}")
                    return None
    except Exception as e:
        print(f"[Live Price Error] {e}")
        return None
