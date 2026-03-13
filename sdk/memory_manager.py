import os
import subprocess
import json
import datetime
from pathlib import Path

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
import sys
sys.path.append(BASE_DIR)
from sdk.synaptic_matrix import SynapticMatrix

class EvoMemory:
    def __init__(self, storage_path=None):
        if storage_path is None:
            storage_path = os.path.join(BASE_DIR, "meta-swarms", "memory.json")
        self.storage_path = storage_path
        self.synapses = SynapticMatrix()
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, "w") as f:
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
        
        # Reinforce learning and trigger telemetry to Hive Mind
        self.synapses.reinforce(
            swarm_name="architect_adversary_quantum", 
            success_delta=0.5,
            full_path=["auditor", "architect", "adversary", "quantum_optimizer", "coder", "tester"]
        )

    def log_failure(self, task, error):
        with open(self.storage_path, "r+") as f:
            data = json.load(f)
            data.setdefault("excluded_issues", []).append(task)
            data["history"].append({
                "timestamp": str(datetime.datetime.now()),
                "task": task,
                "error": error,
                "status": "failure"
            })
            f.seek(0)
            json.dump(data, f, indent=4)
        
        # Penalize learning (no telemetry sent on failure)
        self.synapses.reinforce(swarm_name="architect_adversary_quantum", success_delta=-0.1)
    
    def get_excluded_issues(self):
        with open(self.storage_path, "r") as f:
            data = json.load(f)
            return data.get("excluded_issues", [])

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
