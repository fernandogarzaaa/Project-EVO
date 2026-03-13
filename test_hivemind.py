import requests
import json
payload = {
    "instance_id": "ae04267f-7328-4a35-b28e-211a52f3c845",
    "language": "auto-detect",
    "issue_type": "autonomous_fix",
    "successful_swarm_path": ["auditor", "architect", "adversary", "quantum_optimizer", "coder", "tester"],
    "weight_delta": 0.5
}
resp = requests.post("https://project-evo-teal.vercel.app/telemetry/sync", json=payload)
print(resp.text)
