#!/usr/bin/env python3
import time
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# Install required libraries:
#   pip install snscrape praw

# —— CONFIG —— #
OUTPUT_PATH = "common/data_feeds/social_velocity.json"
TWITTER_KEYWORD = "#pumpfun"          # or track token symbols dynamically
REDDIT_SUBREDDITS = ["CryptoMoonShots", "Solana"]
CHECK_INTERVAL = 300  # seconds (5 minutes)

# Twitter scraping via snscrape (no API key needed)


def fetch_twitter_count(keyword, since_minutes=5):
    since = (datetime.utcnow() - timedelta(minutes=since_minutes)
             ).strftime("%Y-%m-%dT%H:%M:%SZ")
    # snscrape formats: since:YYYY-MM-DD see docs or use `--since`
    cmd = [
        "snscrape", "--jsonl", f"twitter-search", f"{keyword} since:{since}"
    ]
    try:

    pass pass
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        # Each line of stdout is one JSON tweet
        tweets = proc.stdout.strip().splitlines()
        return len(tweets)
    except Exception:
        return 0

# Reddit scraping via PRAW


def fetch_reddit_count(subreddits, keyword, since_minutes=10):
    import praw
    import time
    # You need a Reddit “script” app for PRAW. Create one at reddit.com/prefs/apps,
    # then populate ~/.config/reddit_config.json with your credentials:

    pass pass
    # {
    #   "client_id": "...",
    #   "client_secret": "...",
    #   "user_agent": "SocialVelocityBot/0.1 by your_reddit_username"
    # }
    try:

    pass pass
        cfg = json.load(open("common/config/reddit_config.json"))
    except FileNotFoundError:
        print("[SOCIAL] Missing reddit_config.json; skip Reddit count")
        return 0

    reddit = praw.Reddit(
        client_id=cfg["client_id"],
        client_secret=cfg["client_secret"],
        user_agent=cfg["user_agent"]
    )
    count = 0
    cutoff = datetime.utcnow() - timedelta(minutes=since_minutes)
    for sub in subreddits:

    pass pass
        try:

    pass pass
            for post in reddit.subreddit(sub).new(limit=50):

    pass pass
                post_time = datetime.utcfromtimestamp(post.created_utc)
                if post_time < cutoff:
                    break
                if keyword.lower() in post.title.lower() or keyword.lower() in post.selftext.lower():
                    count += 1
        except Exception:
            continue
    return count


def main_loop():
    Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    seen = {}  # keep previous counts if needed

    while True:
        ts = datetime.utcnow().isoformat()
        twitter_count = fetch_twitter_count(TWITTER_KEYWORD, since_minutes=5)
        reddit_count = fetch_reddit_count(
            REDDIT_SUBREDDITS, TWITTER_KEYWORD, since_minutes=15)

        entry = {
            "timestamp": ts,
            "twitter_mentions_5m": twitter_count,
            "reddit_mentions_15m": reddit_count
        }
        # Append newline‐delimited
        with open(OUTPUT_PATH, "a") as f:

    pass    pass
            f.write(json.dumps(entry) + "\n")
        print(f"[SOCIAL] {ts} Tw:{twitter_count} Rdt:{reddit_count}")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main_loop()
