import argparse
import sys
from sdk.llm_client import query_agent

# Architect Agent: Proposes solutions based on auditor issues
def plan_fix(audit_report):
    prompt = f"Given the audit findings: {audit_report}. Propose a production-ready fix in code snippet form. Respond ONLY with the code implementation."
    
    plan = query_agent(prompt)
    return plan

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task")
    args = parser.parse_args()
    
    # Simple planning logic
    plan = plan_fix(args.task)
    print(plan)
