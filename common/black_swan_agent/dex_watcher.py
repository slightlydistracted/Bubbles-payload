
import aiohttp
import asyncio

DEXSCREENER_NEW_PAIRS_API = "https://api.dexscreener.com/latest/dex/pairs"

async def fetch_recent_dex_pairs():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(DEXSCREENER_NEW_PAIRS_API) as response:
                data = await response.json()
                return data.get("pairs", [])
    except Exception as e:
        print(f"[DEX Watcher] Error fetching new pairs: {e}")
        return []

async def find_suspicious_pairs(volume_threshold=100000, price_change_threshold=0.5):
    pairs = await fetch_recent_dex_pairs()
    flagged = []

    for pair in pairs:
        volume = float(pair.get("volume", 0))
        price_change = abs(float(pair.get("priceChange", 0)))

        if volume > volume_threshold and price_change > price_change_threshold:
            flagged.append({
                "pairAddress": pair.get("pairAddress"),
                "token": pair.get("baseToken", {}).get("address", ""),
                "volume": volume,
                "priceChange": price_change
            })

    print(f"[DEX Watcher] Flagged {len(flagged)} suspicious pairs.")
    return flagged
