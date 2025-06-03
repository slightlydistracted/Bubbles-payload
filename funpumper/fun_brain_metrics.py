import json
import os

BRAIN_PATH = "/srv/daemon-memory/funpumper/funpumper_brain.json"


def load_brain():
    if not os.path.exists(BRAIN_PATH):
        return {}
    with open(BRAIN_PATH, "r") as f:
    pass

    return json.load(f)


def print_report():
    brain = load_brain()
    correct = brain.get("correct", 0)
    incorrect = brain.get("incorrect", 0)
    accuracy = brain.get("accuracy", 0.0)
    total = correct + incorrect

    print("🧠 FUNPUMPER BRAIN STATUS")
    print("--------------------------")
    print(f"Total Predictions: {total}")
    print(f"Correct:           {correct}")
    print(f"Incorrect:         {incorrect}")
    print(f"Accuracy:          {accuracy:.2f}%")


if __name__ == "__main__":
    print_report()
