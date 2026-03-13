import json
import math

class SynapticMatrix:
    def __init__(self, path="D:/project-evo/meta-swarms/synapses.json"):
        self.path = path
        self.matrix = self._load()

    def _load(self):
        if not os.path.exists(self.path):
            return {"swarm_weights": {"auditor": 1.0, "architect": 1.0, "coder": 1.0}}
        with open(self.path, "r") as f:
            return json.load(f)

    def reinforce(self, swarm_name, success_delta):
        # Hebbian Learning: "Cells that fire together, wire together."
        # Increase the weight of successful swarm paths
        self.matrix["swarm_weights"][swarm_name] = self.matrix["swarm_weights"].get(swarm_name, 1.0) + success_delta
        self._save()

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.matrix, f, indent=4)

    def get_strategy(self):
        # Probability-based pathing (The "Genomic" choice)
        return sorted(self.matrix["swarm_weights"].items(), key=lambda x: x[1], reverse=True)
