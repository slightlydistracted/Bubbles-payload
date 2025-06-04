
import os
import ast
import json
from collections import defaultdict

def extract_terms_from_ast(tree):
    terms = {
        "functions": [],
        "classes": [],
        "variables": [],
        "imports": []
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            terms["functions"].append(node.name)
        elif isinstance(node, ast.ClassDef):
            terms["classes"].append(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    terms["variables"].append(target.id)
        elif isinstance(node, ast.ImportFrom):
            terms["imports"].extend(alias.name for alias in node.names)
        elif isinstance(node, ast.Import):
            terms["imports"].extend(alias.name for alias in node.names)

    return terms

def scan_directory(directory):
    glossary = defaultdict(lambda: defaultdict(list))
    scanned_files = 0

    print(f"[Lexicon] Scanning: {directory}")
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                scanned_files += 1
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r") as f:
                        tree = ast.parse(f.read())
                        terms = extract_terms_from_ast(tree)
                        for k in terms:
                            glossary[file][k].extend(terms[k])
                except Exception as e:
                    glossary[file]["errors"].append(str(e))

    print(f"[Lexicon] Scanned {scanned_files} Python files.")
    return glossary

def deduplicate_terms(glossary):
    for file, content in glossary.items():
        for k in content:
            if isinstance(content[k], list):
                glossary[file][k] = sorted(set(content[k]))
    return glossary

def write_output(glossary, path):
    with open(path, "w") as f:
        json.dump(glossary, f, indent=2)

if __name__ == "__main__":
    cwd = os.getcwd()
    output_path = os.path.join(cwd, "lexicon_output.json")

    glossary = scan_directory(cwd)
    deduped = deduplicate_terms(glossary)
    write_output(deduped, output_path)
    print(f"[Lexicon] Output written to {output_path}")
