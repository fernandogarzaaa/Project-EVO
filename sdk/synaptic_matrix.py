import json
import math
import os
import requests
import uuid
import threading

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class SynapticMatrix:
    def __init__(self, path=None):
        if path is None:
            path = os.path.join(BASE_DIR, "meta-swarms", "synapses.json")
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self.matrix = self._load()
        # Unique ID for this specific organism instance
        self.instance_id = self.matrix.get("instance_id", str(uuid.uuid4()))
        self.hive_mind_url = os.getenv("HIVEMIND_URL", "https://project-evo-teal.vercel.app") # Production Hive Mind

    def _load(self):
        if not os.path.exists(self.path):
            return {"instance_id": str(uuid.uuid4()), "swarm_weights": {"auditor": 1.0, "architect": 1.0, "coder": 1.0}}
        with open(self.path, "r") as f:
            return json.load(f)

    def reinforce(self, swarm_name, success_delta, full_path=None):
        # Hebbian Learning: "Cells that fire together, wire together."
        self.matrix["swarm_weights"][swarm_name] = self.matrix["swarm_weights"].get(swarm_name, 1.0) + success_delta
        self._save()
        
        # Telemetry: Send anonymous success data to the Hive Mind
        if full_path and success_delta > 0:
            threading.Thread(target=self._sync_with_hivemind, args=(full_path, success_delta)).start()

    def _sync_with_hivemind(self, full_path, delta):
        if os.getenv("EVO_OPT_OUT_TELEMETRY") == "true":
            return
            
        payload = {
            "instance_id": self.instance_id,
            "language": "auto-detect", # Will be dynamic later
            "issue_type": "autonomous_fix",
            "successful_swarm_path": full_path,
            "weight_delta": delta
        }
        try:
            requests.post(f"{self.hive_mind_url}/telemetry/sync", json=payload, timeout=2)
        except:
            pass # Fail silently, do not interrupt the local organism

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.matrix, f, indent=4)

    def get_strategy(self):
        # Probability-based pathing (The "Genomic" choice)
        return sorted(self.matrix["swarm_weights"].items(), key=lambda x: x[1], reverse=True)
