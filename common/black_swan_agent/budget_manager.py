
import os
import json
from datetime import datetime

BUDGET_FILE = os.path.expanduser("~/feralsys/tools/black_swan_agent/portfolio_budget.json")
DEFAULT_BUDGET = 100.0

def timestamp():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def load_portfolio():
    if not os.path.exists(BUDGET_FILE):
        return {
            "budget": DEFAULT_BUDGET,
            "tokens": [],
            "history": []
        }
    try:
        with open(BUDGET_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {
            "budget": DEFAULT_BUDGET,
            "tokens": [],
            "history": []
        }

def save_portfolio(portfolio):
    with open(BUDGET_FILE, "w") as f:
        json.dump(portfolio, f, indent=2)

def reset_portfolio():
    portfolio = {
        "budget": DEFAULT_BUDGET,
        "tokens": [],
        "history": []
    }
    save_portfolio(portfolio)
    return portfolio

def update_budget(portfolio, amount, reason=""):
    portfolio["budget"] += amount
    portfolio["history"].append({
        "type": "earn" if amount > 0 else "spend",
        "amount": amount,
        "reason": reason,
        "timestamp": timestamp()
    })
    save_portfolio(portfolio)
    return portfolio

def is_budget_exhausted(portfolio):
    return portfolio.get("budget", 0.0) <= 0

def get_budget_amount(portfolio):
    return portfolio.get("budget", 0.0)
