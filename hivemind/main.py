from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
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
    
    path_signature = "->".join(payload.successful_swarm_path)
    
    if path_signature not in matrix["global_weights"]:
        matrix["global_weights"][path_signature] = 1.0
        
    matrix["global_weights"][path_signature] += payload.weight_delta
    
    save_master_matrix(matrix)

@app.get("/")
async def root():
    return {"status": "Hive Mind is Online", "version": "1.0", "message": "Project Evo Telemetry Server is active. Visit /dashboard for God View."}

@app.post("/telemetry/sync")
async def sync_telemetry(payload: TelemetryPayload, background_tasks: BackgroundTasks):
    if payload.weight_delta <= 0:
        raise HTTPException(status_code=400, detail="Only successful delta weights are aggregated.")
    background_tasks.add_task(aggregate_synapse, payload)
    return {"status": "success", "message": "Synaptic data merged into Hive Mind."}

@app.get("/matrix/download")
async def download_master_matrix():
    return load_master_matrix()

@app.get("/dashboard", response_class=HTMLResponse)
async def god_view_dashboard():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Evo Hive Mind | God View</title>
        <style>
            body { background-color: #0d1117; color: #00ff00; font-family: monospace; padding: 40px; }
            h1 { color: #58a6ff; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
            .matrix-container { background: #161b22; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
            .pathway { margin-bottom: 15px; }
            .bar-bg { background: #30363d; height: 20px; border-radius: 4px; overflow: hidden; width: 100%; margin-top: 5px; }
            .bar-fill { background: #238636; height: 100%; }
            .meta { color: #8b949e; font-size: 0.9em; }
        </style>
        <script>
            async function fetchMatrix() {
                const response = await fetch('/matrix/download');
                const data = await response.json();
                const weights = data.global_weights || {};
                
                let html = '';
                let maxWeight = 1.0;
                
                // Find max weight for scaling bars
                for (let key in weights) {
                    if (weights[key] > maxWeight) maxWeight = weights[key];
                }
                
                for (let path in weights) {
                    let weight = weights[path];
                    let width = (weight / maxWeight) * 100;
                    html += `<div class="pathway">
                        <div><strong>Neural Pathway:</strong> ${path}</div>
                        <div class="meta">Synaptic Weight: ${weight.toFixed(2)}</div>
                        <div class="bar-bg"><div class="bar-fill" style="width: ${width}%;"></div></div>
                    </div>`;
                }
                
                if(html === '') html = '<p>Awaiting first telemetry sync from global swarm...</p>';
                document.getElementById('matrix-data').innerHTML = html;
            }
            setInterval(fetchMatrix, 5000); // Poll every 5 seconds
            window.onload = fetchMatrix;
        </script>
    </head>
    <body>
        <h1>Project Evo: Global Hive Mind</h1>
        <p>Live Synaptic Matrix Telemetry (Auto-updating)</p>
        <div class="matrix-container" id="matrix-data">
            Loading neural pathways...
        </div>
    </body>
    </html>
    """
    return html_content

