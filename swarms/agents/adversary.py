import argparse
import sys
from sdk.llm_client import query_agent

# Adversarial Auditor Agent: Tries to break the code
def find_weaknesses(code_snippet):
    prompt = f"Perform a 'Red Team' attack on this code: {code_snippet}. Find edge cases, race conditions, or security flaws. Return only the exploit vectors."
    
    exploit_vectors = query_agent(prompt)
    return exploit_vectors

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task") # The proposed code change
    args = parser.parse_args()
    
    # Analyze the architect's plan for weaknesses
    weaknesses = find_weaknesses(args.task)
    if "No weaknesses" in weaknesses:
        print("NO_WEAKNESSES")
    else:
        print(f"WEAKNESSES_FOUND: {weaknesses}")
