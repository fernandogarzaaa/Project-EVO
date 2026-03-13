import os
import glob

class ContextRetriever:
    def __init__(self, repo_path="."):
        self.repo_path = repo_path
        self.ignore_dirs = {".git", ".venv", "node_modules", "__pycache__", "dist", "build"}

    def get_repo_map(self):
        """Generates a structural map of the repository."""
        repo_map = []
        for root, dirs, files in os.walk(self.repo_path):
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            level = root.replace(self.repo_path, '').count(os.sep)
            indent = ' ' * 4 * (level)
            repo_map.append(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                if not f.endswith(('.pyc', '.log', '.exe', '.dll', '.so')):
                    repo_map.append(f"{subindent}{f}")
        return "\n".join(repo_map[:200]) # Limit size

    def retrieve_relevant_snippets(self, issue_keywords):
        """Mock RAG: Finds files matching keywords and extracts snippets."""
        snippets = ""
        for root, dirs, files in os.walk(self.repo_path):
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.rs', '.md')):
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if any(k in content for k in issue_keywords):
                                snippets += f"\n--- File: {path} ---\n"
                                snippets += content[:500] + "...\n" # First 500 chars as snippet
                    except:
                        pass
        return snippets[:2000] # Limit context window

if __name__ == "__main__":
    retriever = ContextRetriever()
    print(retriever.get_repo_map())
