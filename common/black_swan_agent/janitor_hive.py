
import subprocess
import time
import argparse

JANITORS = [
    "syntax_janitor.py",
    "structure_janitor.py",
    "variable_janitor.py",
    "naming_janitor.py",
    "function_janitor.py",
    "import_janitor.py"
]

def run_janitors():
    print("[JANITOR HIVE] Dispatching janitors...")
    for janitor in JANITORS:
        print(f"[JANITOR HIVE] Running {janitor}")
        subprocess.run(["python3", janitor])

def main():
    parser = argparse.ArgumentParser(description="Run all janitor modules.")
    parser.add_argument("--loop", action="store_true", help="Run continuously")
    parser.add_argument("--interval", type=int, default=60, help="Loop interval in seconds")
    args = parser.parse_args()

    if args.loop:
        while True:
            run_janitors()
            print(f"[JANITOR HIVE] Sleeping for {args.interval} seconds...")
            time.sleep(args.interval)
    else:
        run_janitors()

if __name__ == "__main__":
    main()
