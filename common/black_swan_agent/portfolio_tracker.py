import os
import json
from datetime import datetime, timedelta
import random

PORTFOLIO_PATH = '/root/feralsys/tools/black_swan_agent/simulated_portfolio.json'
SALES_LOG_PATH = '/root/feralsys/tools/black_swan_agent/sales_log.json'

# Mocked current price simulator
def simulate_current_price(entry_price):
    # Assume random walk +/- 70%
    movement = random.uniform(-0.7, 1.0)
    return round(entry_price * (1 + movement), 8)

# Simulate checking portfolio and executing sells
async def check_and_sell():
    if not os.path.exists(PORTFOLIO_PATH):
        print("No portfolio found.")
        return

    with open(PORTFOLIO_PATH, 'r') as f:
        portfolio = json.load(f)

    updated_portfolio = []
    sales_log = []

    for position in portfolio:
        token = position["token_address"]
        amount = position["amount_purchased"]
        buy_price = position["price_at_purchase"]
        buy_time = datetime.fromisoformat(position["timestamp"])

        # Simulate current price
        current_price = simulate_current_price(buy_price)

        # Calculate % change
        price_change = (current_price - buy_price) / buy_price

        sell_reason = None

        # SELL CONDITIONS
        if price_change >= 1.0:
            sell_reason = "Take Profit"
        elif price_change <= -0.5:
            sell_reason = "Stop Loss"
        elif datetime.utcnow() - buy_time > timedelta(hours=24):
            sell_reason = "Max Hold Time Expired"

        if sell_reason:
            profit_loss_usd = (current_price - buy_price) * amount
            sales_log.append({
                "token_address": token,
                "sell_reason": sell_reason,
                "amount": amount,
                "buy_price": buy_price,
                "sell_price": current_price,
                "profit_or_loss_usd": round(profit_loss_usd, 4),
                "time_sold": datetime.utcnow().isoformat()
            })
            print(f"[SIMULATED SELL] {token} - Reason: {sell_reason} - PnL: {round(profit_loss_usd,4)} USD")
        else:
            updated_portfolio.append(position)

    # Write updated portfolio back
    with open(PORTFOLIO_PATH, 'w') as f:
        json.dump(updated_portfolio, f, indent=2)

    # Append sales to log
    if os.path.exists(SALES_LOG_PATH):
        with open(SALES_LOG_PATH, 'r') as f:
            old_sales = json.load(f)
    else:
        old_sales = []

    all_sales = old_sales + sales_log
    with open(SALES_LOG_PATH, 'w') as f:
        json.dump(all_sales, f, indent=2)

if __name__ == "__main__":
    check_and_sell()
