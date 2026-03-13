from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import json
import os
from typing import Dict

app = FastAPI(title="Project Evo - Hive Mind API", description="Global Synaptic Matrix Aggregator")

MASTER_MATRIX_FILE = "master_synapses.json"

class TelemetryPayload(BaseModel):
    instance_id: str
    language: str
    issue_type: str
    successful_swarm_path: list[str]
    weight_delta: float

def load_master_matrix() -> Dict:
    if not os.path.exists(MASTER_MATRIX_FILE):
        return {"global_weights": {}}
    with open(MASTER_MATRIX_FILE, "r") as f:
        return json.load(f)

def save_master_matrix(matrix: Dict):
    with open(MASTER_MATRIX_FILE, "w") as f:
        json.dump(matrix, f, indent=4)

def aggregate_synapse(payload: TelemetryPayload):
    matrix = load_master_matrix()
    
    # Create a unique signature for this evolutionary path
    path_signature = "->".join(payload.successful_swarm_path)
    
    if path_signature not in matrix["global_weights"]:
        matrix["global_weights"][path_signature] = 1.0
        
    # Aggregate the learning
    matrix["global_weights"][path_signature] += payload.weight_delta
    
    save_master_matrix(matrix)

@app.post("/telemetry/sync")
async def sync_telemetry(payload: TelemetryPayload, background_tasks: BackgroundTasks):
    """
    Receives successful evolutionary paths from global Evo instances.
    Privacy-First: NO CODE IS TRANSMITTED. Only swarm topologies and weights.
    """
    if payload.weight_delta <= 0:
        raise HTTPException(status_code=400, detail="Only successful delta weights are aggregated.")
        
    # Process asynchronously to keep client response instant
    background_tasks.add_task(aggregate_synapse, payload)
    
    return {"status": "success", "message": "Synaptic data merged into Hive Mind."}

@app.get("/matrix/download")
async def download_master_matrix():
    """
    Allows premium/enterprise clients to download the hyper-optimized Master Brain.
    """
    return load_master_matrix()

# Run with: uvicorn main:app --reload
