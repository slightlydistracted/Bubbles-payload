
import os
import ast

class VariableJanitor:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.issues = []

    def scan(self):
        raise NotImplementedError("Each janitor must implement its own scan method.")

    def report(self):
        for issue in self.issues:
            print(f"[{self.__class__.__name__}] {issue}")
