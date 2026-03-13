import os
import subprocess
import json
import datetime
from pathlib import Path

class EvoMemory:
    def __init__(self, storage_path="D:/project-evo/meta-swarms/memory.json"):
        self.storage_path = storage_path
        if not os.path.exists(storage_path):
            with open(storage_path, "w") as f:
                json.dump({"history": [], "knowledge_graph": {}}, f)

    def log_success(self, task, solution):
        with open(self.storage_path, "r+") as f:
            data = json.load(f)
            data["history"].append({
                "timestamp": str(datetime.datetime.now()),
                "task": task,
                "solution": solution,
                "status": "success"
            })
            f.seek(0)
            json.dump(data, f, indent=4)

    def log_failure(self, task, error):
        with open(self.storage_path, "r+") as f:
            data = json.load(f)
            data["history"].append({
                "timestamp": str(datetime.datetime.now()),
                "task": task,
                "error": error,
                "status": "failure"
            })
            f.seek(0)
            json.dump(data, f, indent=4)

# Coder Agent implementation with Git
def apply_change(change_description):
    # This agent assumes a git repository environment
    try:
        # Simulate applying change and committing
        # In a real environment, this would involve patching files
        subprocess.run(["git", "commit", "-am", f"Evo-Agent: {change_description}"], check=True)
        return True
    except Exception as e:
        return False
