import numpy as np
import time
from typing import List, Dict, Any

class TensorMemory:
    """
    Holographic Tensor Memory (HTM) for Project EVO.
    Simulates storing and retrieving multi-modal vector embeddings (latent context).
    """
    def __init__(self, dimensions: int = 1536):
        self.dimensions = dimensions
        # Each entry: {"id": str, "vector": np.ndarray, "metadata": dict, "timestamp": float}
        self.memory_store = []

    def write_latent(self, latent_vector: np.ndarray, metadata: Dict[str, Any] = None) -> str:
        """Writes latent context to the tensor memory."""
        if metadata is None:
            metadata = {}
        
        # Ensure it's a numpy array for simulation
        if not isinstance(latent_vector, np.ndarray):
            latent_vector = np.array(latent_vector, dtype=float)
            
        entry_id = f"htm_{int(time.time() * 1000)}"
        self.memory_store.append({
            "id": entry_id,
            "vector": latent_vector,
            "metadata": metadata,
            "timestamp": time.time()
        })
        return entry_id

    def read_latent(self, query_vector: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieves closest latent contexts based on a query vector using cosine similarity."""
        if not self.memory_store:
            return []
            
        if not isinstance(query_vector, np.ndarray):
            query_vector = np.array(query_vector, dtype=float)
            
        results = []
        for entry in self.memory_store:
            # Cosine similarity calculation
            norm_q = np.linalg.norm(query_vector)
            norm_v = np.linalg.norm(entry["vector"])
            if norm_q == 0 or norm_v == 0:
                sim = 0.0
            else:
                sim = np.dot(query_vector, entry["vector"]) / (norm_q * norm_v)
            
            results.append({
                "id": entry["id"],
                "similarity": float(sim),
                "metadata": entry["metadata"],
                "timestamp": entry["timestamp"]
            })
            
        # Sort by similarity descending
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]
