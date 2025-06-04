
import json
from collections import defaultdict
from pathlib import Path

# Load interface map
interface_path = Path("interface_map.json")
with open(interface_path, "r") as f:
    interface_map = json.load(f)

# Track all defined and imported functions
defined_functions = defaultdict(set)
imported_functions = defaultdict(list)

for filename, data in interface_map.items():
    if "defines" in data:
        for func in data["defines"]["functions"]:
            defined_functions[filename].add(func)
    if "imports" in data:
        for imp in data["imports"]["imports"]:
            imported_functions[filename].append((imp["from"], imp["import"]))

# Identify mismatched imports (not defined anywhere)
conflicts = defaultdict(list)

for filename, imports in imported_functions.items():
    for mod, func in imports:
        found = False
        for other_file, defs in defined_functions.items():
            if func in defs and mod in other_file:
                found = True
                break
        if not found:
            conflicts[filename].append(f"{func} from {mod}")

# Save results
conflict_report_path = Path("interface_conflicts.json")
with open(conflict_report_path, "w") as f:
    json.dump(conflicts, f, indent=2)

print("[Interface Validator] Scan complete. Results saved to interface_conflicts.json.")
