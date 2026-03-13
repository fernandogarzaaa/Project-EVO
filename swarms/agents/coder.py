import argparse
import sys
import os
import datetime
import requests
try:
    from git import Repo
except ImportError:
    Repo = None

# Coder Agent: Applies fixes via GitPython and GitHub API
def apply_fix_and_create_pr(patch_plan):
    if not Repo:
        return "ERROR: GitPython not installed. Run pip install GitPython."

    try:
        repo = Repo(".")
        branch_name = f"evo-fix-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        # Create and checkout branch
        new_branch = repo.create_head(branch_name)
        new_branch.checkout()

        # Configure git identity for Actions runner
        with repo.config_writer() as cw:
            cw.set_value("user", "name", "Project Evo Agent")
            cw.set_value("user", "email", "evo-agent@project-evo.ai")
        
        # Ensure safe directory for git in CI
        subprocess.run(["git", "config", "--global", "--add", "safe.directory", "/home/runner/work/Project-EVO/Project-EVO"], check=False)

        # Simulate applying change
        with open("math_engine.py", "w") as f:
            f.write("""def add(a, b):
    '''Adds two numbers together.'''
    return a + b

def multiply(a, b):
    '''Multiplies two numbers.'''
    return a * b
""")
        
        # Commit
        repo.git.add(A=True)
        try:
            repo.index.commit(f"Autonomous Evo Fix: {branch_name}")
        except Exception as e:
            return f"COMMIT_ERROR: {str(e)}"
        
        # Push
        try:
            origin = repo.remote(name='origin')
            origin.push(branch_name)
        except ValueError:
            return f"BRANCH_CREATED: {branch_name} (No origin remote found for PR)"

        # Create PR via GitHub API to remove `gh` CLI dependency
        token = os.getenv("GITHUB_TOKEN")
        if token:
            headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
            remote_url = list(origin.urls)[0]
            # Naive parsing of repo owner/name from remote URL
            repo_path = remote_url.split("github.com/")[-1].replace(".git", "")
            pr_data = {
                "title": f"Autonomous Fix: {branch_name}",
                "body": "Project Evo applied a self-healing patch.\n\n" + patch_plan,
                "head": branch_name,
                "base": "main"
            }
            api_url = f"https://api.github.com/repos/{repo_path}/pulls"
            resp = requests.post(api_url, headers=headers, json=pr_data)
            if resp.status_code == 201:
                return f"PR_CREATED: {resp.json().get('html_url')}"
            else:
                return f"PR_CREATION_FAILED: {resp.text}"
        
        return f"BRANCH_PUSHED: {branch_name} (No GITHUB_TOKEN for PR)"

    except Exception as e:
        return f"ERROR: {str(e)}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task")
    args = parser.parse_args()
    
    pr_status = apply_fix_and_create_pr(args.task)
    print(pr_status)
