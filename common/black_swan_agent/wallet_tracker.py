
import aiohttp
import asyncio

WHALE_WALLETS = [
    # Add high-value wallets here
    "0x123...", "0x456...", "0x789..."
]

ETHERSCAN_API = "https://api.etherscan.io/api"
ETHERSCAN_KEY = "YOUR_ETHERSCAN_API_KEY"

async def fetch_wallet_activity(wallet_address):
    params = {
        "module": "account",
        "action": "txlist",
        "address": wallet_address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "desc",
        "apikey": ETHERSCAN_KEY
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(ETHERSCAN_API, params=params) as resp:
                data = await resp.json()
                return data.get("result", [])
    except Exception as e:
        print(f"[Wallet Tracker] Error: {e}")
        return []

async def track_whale_wallets():
    all_activity = {}
    for wallet in WHALE_WALLETS:
        txns = await fetch_wallet_activity(wallet)
        all_activity[wallet] = txns[:10]
        print(f"[Wallet Tracker] {wallet}: {len(txns)} recent txns")
    return all_activity

# Usage: asyncio.run(track_whale_wallets())
