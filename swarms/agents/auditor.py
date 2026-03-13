import argparse
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(BASE_DIR)

from sdk.llm_client import query_agent

# Auditor Agent: Performs deep analysis
def audit_repo(repo_path):
    # Fetch file list and content (snippet)
    files = os.listdir(repo_path)
    prompt = f"Audit the following project structure and snippets for bugs/risks: {files}. Respond with 'ISSUE_FOUND' and description, or 'NO_ISSUES'."
    
    analysis = query_agent(prompt)
    return analysis

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task")
    args = parser.parse_args()
    
    # Audit logic
    report = audit_repo(".")
    print(report)
