
import os
from datetime import datetime
import json

JOURNAL_DIR = os.path.expanduser("~/feralsys/tools/black_swan_agent/journals")

def ensure_dir():
    if not os.path.exists(JOURNAL_DIR):
        os.makedirs(JOURNAL_DIR)

def write_daily_journal(portfolio, memory, patterns, mutation_log=None):
    ensure_dir()
    today = datetime.utcnow().strftime("%Y-%m-%d")
    timestamped = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    journal_path = os.path.join(JOURNAL_DIR, f"journal_{timestamped}.md")

    lines = [
        f"# Daily Journal - {today}",
        "",
        "## Budget Summary",
        f"Remaining Budget: ${portfolio.get('budget', 0.0):.2f}",
        f"Total Tokens: {len(portfolio.get('tokens', []))}",
        "",
        "## Token Holdings",
        json.dumps(portfolio.get("tokens", []), indent=2),
        "",
        "## Transaction History",
        json.dumps(portfolio.get("history", []), indent=2),
        "",
        "## Mutation Log",
        json.dumps(mutation_log if mutation_log else [], indent=2),
        "",
        "## Patterns",
        json.dumps(patterns if patterns else {}, indent=2),
        "",
        "## Memory Snapshot",
        json.dumps(memory if memory else {}, indent=2)
    ]

    with open(journal_path, "w") as f:
        f.write("\n".join(lines))
