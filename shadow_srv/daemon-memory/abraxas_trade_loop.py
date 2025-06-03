
import subprocess
import json
import time
from datetime import datetime

TELEGRAM_SCRIPT = "telegram_telemetry_reporter.py"
TX_CONSTRUCTOR_SCRIPT = "living_tx_constructor.py"
LOG_FILE = "abraxas_trade_log.txt"
QUEUE_FILE = "token_queue.json"
RESULT_LOG = "obsidian_first_contact.json"
CONFIDENCE_THRESHOLD = 0.7


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


def load_token_from_queue():
    try:
        with open(QUEUE_FILE, "r") as f:
            queue = json.load(f)
            if not queue:
                return None, []
            return queue.pop(0), queue
    except Exception as e:
        log(f"Error reading token queue: {str(e)}")
        return None, []


def write_queue(queue):
    try:
        with open(QUEUE_FILE, "w") as f:
            json.dump(queue, f)
    except Exception as e:
        log(f"Error writing token queue: {str(e)}")


def save_result_to_memory(result):
    try:
        with open(RESULT_LOG, "a") as f:
            f.write(json.dumps(result) + "\n")
    except Exception as e:
        log(f"Error saving result to memory: {str(e)}")


def execute_trade(token_info):
    symbol = token_info.get("symbol", "UNKNOWN")
    confidence = token_info.get("confidence", 0)
    if confidence >= CONFIDENCE_THRESHOLD:
        try:
            result = subprocess.run(["python3", TX_CONSTRUCTOR_SCRIPT, json.dumps(token_info)],
                                    capture_output=True, text=True)
            output = result.stdout.strip()
            log(f"Executed trade for {symbol}: {output}")
            save_result_to_memory({
                "timestamp": datetime.now().isoformat(),
                "symbol": symbol,
                "confidence": confidence,
                "result": output
            })
            message = f"[ABRAXAS TRADE]\nSymbol: {symbol}\nConfidence: {confidence}\nResult: {output}"
        except Exception as e:
            message = f"[ABRAXAS TRADE FAILURE]\nSymbol: {symbol}\nConfidence: {confidence}\nError: {str(e)}"
            log(message)
    else:
        message = f"[ABRAXAS SKIPPED]\nSymbol: {symbol}\nConfidence: {confidence} below threshold"
        log(message)

    subprocess.run(["python3", TELEGRAM_SCRIPT])


if __name__ == "__main__":
    token, remaining_queue = load_token_from_queue()
    if token:
        write_queue(remaining_queue)
        execute_trade(token)
    else:
        log("Token queue empty.")
