import argparse
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(BASE_DIR)

from sdk.llm_client import query_agent

# Auditor Agent: Performs deep analysis
def audit_repo(repo_path, task):
    # Fetch file list and content (snippet)
    # The task passed in is the context (repo map)
    prompt = f"Audit the following project structure/issues and suggest specific fixes: {task}. If no specific issue is provided, audit the structure. Respond with 'ISSUE_FOUND: <specific_issue>' and description, or 'NO_ISSUES'."
    
    analysis = query_agent(prompt)
    return analysis

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", default=".")
    args = parser.parse_args()
    
    # Audit logic
    report = audit_repo(".", args.task)
    print(report)
