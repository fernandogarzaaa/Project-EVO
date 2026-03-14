import os
import subprocess
import json
import datetime
import numpy as np
from pathlib import Path

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
import sys
sys.path.append(BASE_DIR)
from sdk.synaptic_matrix import SynapticMatrix
from sdk.htm_core import TensorMemory

class EvoMemory:
    def __init__(self, storage_path=None, use_htm=False):
        if storage_path is None:
            storage_path = os.path.join(BASE_DIR, "meta-swarms", "memory.json")
        self.storage_path = storage_path
        self.synapses = SynapticMatrix()
        
        # Initialize HTM optional component
        self.use_htm = use_htm
        self.htm = TensorMemory() if use_htm else None
        
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

    def store_latent_context(self, latent_vector, metadata=None):
        if self.use_htm and self.htm:
            return self.htm.write_latent(latent_vector, metadata)
        return None

    def retrieve_latent_context(self, query_vector, top_k=5):
        if self.use_htm and self.htm:
            return self.htm.read_latent(query_vector, top_k)
        return []

class Librarian:
    """Agent that periodically reads raw daily logs and distills them into a single MEMORY.md summary."""
    def __init__(self, memory_dir=None, output_file=None):
        if memory_dir is None:
            memory_dir = os.path.join(BASE_DIR, "memory")
        if output_file is None:
            output_file = os.path.join(BASE_DIR, "MEMORY.md")
        self.memory_dir = Path(memory_dir)
        self.output_file = Path(output_file)

    def synthesize(self):
        """Read all YYYY-MM-DD.md files in memory_dir and create a distilled MEMORY.md."""
        if not self.memory_dir.exists():
            return "No memory directory found."
        
        compiled_logs = []
        for file in sorted(self.memory_dir.glob("????-??-??.md")):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        compiled_logs.append(f"### {file.name}\n{content}")
            except Exception as e:
                continue
                
        if not compiled_logs:
            return "No logs to synthesize."
            
        # Reflection-based distillation: in a full implementation, this would call an LLM.
        # Here we compile the raw logs into a structured summary document.
        distilled_content = "# System Memory (Distilled)\n\n"
        distilled_content += "This file contains the synthesized reflections from daily logs.\n\n"
        distilled_content += "\n\n---\n\n".join(compiled_logs)
        
        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write(distilled_content)
            
        return f"Synthesized {len(compiled_logs)} daily logs into {self.output_file.name}."

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
