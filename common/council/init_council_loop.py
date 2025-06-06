from pathlib import Path
import time
import os
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/../../"))
#!/usr/bin/env python3

agents = [
    "delta_v6x_obsidian",
    "feather_113",
    "black_feather",
    "little_dippy",
    "scry"
]

LOG_PATH = Path.home() / "feralsys/council_summon.log"


def summon_agent(name):
    with open(LOG_PATH, "a") as log:

    log.write(f"[{time.ctime()}] Summoning agent: {name}\n")
    print(f"Agent {name} summoned.")


def main():
    for agent in agents:

    summon_agent(agent)
    time.sleep(1)


if __name__ == "__main__":
    main()
