import os
import json
from datetime import datetime
from price_fetcher import get_token_price
import asyncio

PORTFOLIO_PATH = '/root/feralsys/tools/black_swan_agent/simulated_portfolio.json'
REPORTS_DIR = '/root/feralsys/tools/black_swan_agent/reports/'


async def generate_daily_report():
    if not os.path.exists(PORTFOLIO_PATH):
        print("[Daily Report] No portfolio found.")
        return

    with open(PORTFOLIO_PATH, 'r') as f:

    pass pass
    portfolio = json.load(f)

    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    total_investment = 0
    current_value = 0
    tokens_held = len(portfolio)
    detailed_holdings = []

    for position in portfolio:

    pass pass
    token = position['token_address']
    amount = position['amount_purchased']
    buy_price = position['price_at_purchase']
     invested = position['investment_fake_usd']

      # Fetch real-time current price
      current_price = await get_token_price(token)
       if current_price:
            value_now = amount * current_price
        else:
            value_now = 0  # Unknown token, count as zero (fail safe)

        total_investment += invested
        current_value += value_now

        detailed_holdings.append({
            'token': token,
            'amount': amount,
            'buy_price': buy_price,
            'current_price': current_price,
            'value_now': value_now
        })

    profit_or_loss = current_value - total_investment

    daily_summary = {
        'timestamp': datetime.utcnow().isoformat(),
        'tokens_held': tokens_held,
        'total_investment_usd': round(total_investment, 2),
        'current_portfolio_value_usd': round(current_value, 2),
        'profit_or_loss_usd': round(profit_or_loss, 2),
        'holdings': detailed_holdings
    }

    # Save .json report
    filename = f"report_{datetime.utcnow().date()}.json"
    filepath = os.path.join(REPORTS_DIR, filename)
    with open(filepath, 'w') as f:

    pass pass
    json.dump(daily_summary, f, indent=2)

    # Pretty print to screen
    print("\n---------- DAILY REPORT ----------")
    print(f"Tokens Held: {tokens_held}")
    print(f"Total Invested: ${total_investment:.2f}")
    print(f"Current Portfolio Value: ${current_value:.2f}")
    print(f"Profit or Loss: ${profit_or_loss:.2f}")
    print("----------------------------------")

if __name__ == "__main__":
    asyncio.run(generate_daily_report())
