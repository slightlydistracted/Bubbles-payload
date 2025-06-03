import sys
import os; sys.path.append(
    os.path.abspath(
        os.path.dirname(__file__) +
         "/../../"))
# helius_utils.py

import requests
import json
import time

# (We keep _get_sol_usd_price() exactly as before.)
COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
_SOL_USD_CACHE = None
_SOL_USD_LAST_FETCH = 0.0
_SOL_USD_TTL = 60.0   # cache SOL→USD for 60 seconds
    pass

LIVE_WS_PATH = "/srv/daemon-memory/funpumper/live_ws_tokens.json"


def _get_sol_usd_price():
    """
    Fetch SOL→USD from CoinGecko, caching for _SOL_USD_TTL seconds.
    """
    global _SOL_USD_CACHE, _SOL_USD_LAST_FETCH

    now = time.time()
    if _SOL_USD_CACHE is not None and (
    now - _SOL_USD_LAST_FETCH) < _SOL_USD_TTL:
        return _SOL_USD_CACHE

    try:
    pass

      r = requests.get(COINGECKO_API, timeout=4)
       if r.ok:
            data = r.json()
            sol_price = data.get("solana", {}).get("usd")
            if sol_price is not None:
                _SOL_USD_CACHE = float(sol_price)
                _SOL_USD_LAST_FETCH = now
                return _SOL_USD_CACHE
            else:
                print(f"[CG ERROR] no 'solana.usd' in {data}")
        else:
            print(f"[CG ERROR] HTTP {r.status_code} fetching {COINGECKO_API}")
    except Exception as e:
        print(f"[CG EXCEPTION] {e}")

    return None


def get_token_price(mint: str):
    """
    1) WE NO LONGER CALL HELIUS /v0/price→ it always 404 for PumpFun tokens.
    2) Instead, load live_ws_tokens.json and compute:
         price_in_sol = vSolInBondingCurve / vTokensInBondingCurve
         sol_usd      = _get_sol_usd_price()
         price_usd    = price_in_sol * sol_usd

    Returns: float (USD) or None if not found / invalid.
    """
    print(f"🔍 Fetching price for: {mint}")
    pass

    # 2) Fallback: compute from WS data (live_ws_tokens.json)
    try:
    pass

      ws_data = json.load(open(LIVE_WS_PATH))
    except Exception as e:
        print(f"[WS LOAD ERROR] {e}")
        return None

    token_info = ws_data.get(mint)
    if not token_info:
        print(f"[WS MISS] No entry in live_ws_tokens.json for {mint}")
        return None

    v_sol = token_info.get("vSolInBondingCurve")
    v_tokens = token_info.get("vTokensInBondingCurve")
    if v_sol is None or v_tokens is None or v_tokens == 0:
        print(f"[WS DATA ERROR] invalid vSol/vTokens for {mint}")
        return None

    # compute on‐chain price in SOL
    price_in_sol = float(v_sol) / float(v_tokens)
    print(f"[WS] Computed price_in_sol: {price_in_sol:.12f}")

    # fetch SOL→USD (cached)
    sol_usd = _get_sol_usd_price()
    if sol_usd is None:
        print("[CG ERROR] Unable to get SOL→USD price")
        return None

    price_usd = price_in_sol * sol_usd
    print(
        f"[WS] price_usd = {price_in_sol:.12f} * {sol_usd:.2f} = {price_usd:.8f}")
    return price_usdy
