import json
import os

# Status Dashboard Agent: Visualizes the brain
def generate_status():
    memory_path = "D:/project-evo/meta-swarms/memory.json"
    synapse_path = "D:/project-evo/meta-swarms/synapses.json"
    
    with open(memory_path, "r") as f:
        mem = json.load(f)
    
    with open(synapse_path, "r") as f:
        syn = json.load(f)
        
    print(f"--- PROJECT EVO STATUS ---")
    print(f"Cycles Completed: {len(mem['history'])}")
    print(f"Neural Synapses (Paths): {len(syn['swarm_weights'])}")
    print(f"Health: OPERATIONAL")
    
if __name__ == "__main__":
    generate_status()
