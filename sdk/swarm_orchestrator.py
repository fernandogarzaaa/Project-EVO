import asyncio
import json
import logging
import os
import sys
import hashlib

class CircuitBreaker(Exception):
    pass

class CycleDetector:
    def __init__(self):
        self.history = {}

    def check(self, agent_id, task, input_data):
        input_hash = hashlib.sha256(str(input_data).encode('utf-8')).hexdigest()
        triplet = f"{agent_id}:{task}:{input_hash}"
        self.history[triplet] = self.history.get(triplet, 0) + 1
        if self.history[triplet] > 3:
            raise CircuitBreaker(f"CircuitBreaker tripped for {triplet}")

    def reset(self):
        self.history.clear()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from sdk.memory_manager import EvoMemory
from sdk.context_retriever import ContextRetriever
try:
    import evo_core  # Importing the Rust-based swarm bridge
except ImportError:
    evo_core = None # Fallback to standard Python subprocess

class SwarmOrchestrator:
    def __init__(self, registry_path=None):
        if registry_path is None:
            registry_path = os.path.join(BASE_DIR, "swarms", "registry.json")
        with open(registry_path, "r") as f:
            self.registry = json.load(f)
        self.logger = logging.getLogger("EvoOrchestrator")
        logging.basicConfig(level=logging.INFO)
        self.memory = EvoMemory()
        self.retriever = ContextRetriever()
        self.excluded_issues = self.memory.get_excluded_issues()
        self.cycle_detector = CycleDetector()

    def _get_python_executable(self):
        """Resolves the correct python executable path based on platform and availability."""
        # 1. Try to use current environment's python if .venv doesn't exist
        venv_path = os.path.join(BASE_DIR, ".venv")
        if not os.path.exists(venv_path):
            return sys.executable
            
        # 2. Use .venv if it exists
        if os.name == 'nt':
            return os.path.join(venv_path, "Scripts", "python.exe")
        return os.path.join(venv_path, "bin", "python")

    def _checkpoint_state(self, agent_role, task):
        """Serializes current state to disk before task execution."""
        checkpoint_dir = os.path.join(BASE_DIR, ".checkpoints")
        os.makedirs(checkpoint_dir, exist_ok=True)
        checkpoint_file = os.path.join(checkpoint_dir, "latest_state.json")
        state_data = {
            "agent_role": agent_role,
            "task_preview": task[:200] if isinstance(task, str) else str(task)[:200],
            "excluded_issues": self.excluded_issues
        }
        try:
            with open(checkpoint_file, "w") as f:
                json.dump(state_data, f, indent=2)
            self.logger.info(f"Checkpoint saved for {agent_role} transition.")
        except Exception as e:
            self.logger.error(f"Failed to save checkpoint: {e}")

    async def deploy_agent(self, agent_role, task):
        self.cycle_detector.check(agent_role, "deploy", task)
        self._checkpoint_state(agent_role, task)
        self.logger.info(f"Deploying {agent_role} to address: {task[:50]}...")
        
        # Use Rust bridge if available, else fallback to subprocess
        if evo_core:
            return evo_core.invoke_swarm_agent(agent_role, task)
            
        agent_script = os.path.join(BASE_DIR, "swarms", "agents", f"{agent_role}.py")
        venv_python = self._get_python_executable()
        
        process = await asyncio.create_subprocess_exec(
            venv_python, agent_script, "--task", task,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=os.getcwd()
        )
        stdout, stderr = await process.communicate()
        # Log stderr if it crashed
        if process.returncode != 0:
            self.logger.error(f"{agent_role} failed: {stderr.decode().strip()}")
        return stdout.decode().strip()

    def _is_looping(self, current_issue):
        """Checks the memory log to see if we recently tried (and failed) to fix this exact issue."""
        with open(self.memory.storage_path, "r") as f:
            history = json.load(f).get("history", [])
            
        # Check the last 3 actions. If they are failures for the same issue, abort.
        recent_failures = [h for h in history[-3:] if h.get("status") == "failure"]
        for failure in recent_failures:
            # Simple heuristic: If the issue string is heavily similar to a recent failure
            if current_issue[:100] in failure.get("task", ""):
                return True
        return False

    async def run_parallel_evolution(self, repo_path):
        self.logger.info("Starting Parallel Evolution Cycle on: " + repo_path)
        
        # 1. Audit (Parallelize with context gathering)
        while True:
            try:
                repo_context = self.retriever.get_repo_map()
                if self.excluded_issues:
                    repo_context += "\nALREADY FAILED THESE ISSUES: " + "\n".join(self.excluded_issues)
                
                auditor_task = asyncio.create_task(self.deploy_agent("auditor", repo_context))
                issues = await auditor_task
                
                if "ISSUE_FOUND" in issues:
                    # --- THE ANTI-LOOP CHECK ---
                    if self._is_looping(issues):
                        self.logger.critical("ANTI-LOOP ENGAGED: Swarm has repeatedly failed to fix this exact issue. Pivoting to new issue...")
                        self.excluded_issues.append(issues)
                        continue
                    
                    self.logger.warning("Vulnerabilities detected. Entering Multi-Agent Debate Loop...")
                    
                    # The Cortex: Multi-Agent Debate (Max 3 rounds)
                    plan = ""
                    for debate_round in range(3):
                        self.logger.info(f"--- Debate Round {debate_round + 1} ---")
                        # Add specific file context based on issue
                        snippets = self.retriever.retrieve_relevant_snippets(["error", "bug", "fail"])
                        plan = await self.deploy_agent("architect", issues + "\nContext:\n" + snippets)
                        
                        adversary_check = await self.deploy_agent("adversary", plan)
                        if "WEAKNESSES_FOUND" not in adversary_check:
                            self.logger.info("Adversary approved the architecture.")
                            break
                        
                        self.logger.warning("Adversary caught an edge case. Re-architecting...")
                        issues = adversary_check # Feed weakness back as the new issue
                        
                    # 2.5 Quantum Superposition Optimization
                    optimized_plan = await self.deploy_agent("quantum_optimizer", plan)
                    self.logger.info(f"Quantum Swarm selected path: {optimized_plan[:30]}")
                    
                    # 3. Code (Implement fix with GitPython)
                    commit = await self.deploy_agent("coder", optimized_plan)
                    
                    # 4. Verify (Dynamic test execution)
                    report = await self.deploy_agent("tester", commit)
                    
                    # 5. Metabolic Pruning (Self-Optimization)
                    pruning_report = await self.deploy_agent("meta_optimizer", "run")
                    self.logger.info(f"Metabolic Optimization complete: {pruning_report}")

                    if "VERIFIED" in report:
                        self.memory.log_success(issues, report)
                        self.logger.info("Self-Evolution Successful.")
                        break # Break the loop on success
                    else:
                        self.memory.log_failure(issues, report)
                        self.logger.error("Evolution cycle failed.")
                        self.excluded_issues.append(issues)
                        continue # Continue to next issue
                else:
                    self.logger.info("System is optimal. No changes required.")
                    break # Exit on optimal state

            except CircuitBreaker as e:
                self.logger.error(f"CIRCUIT BREAKER TRIGGERED: {e}. Transitioning to reset state.")
                self.cycle_detector.reset()
                if 'issues' in locals() and "ISSUE_FOUND" in issues:
                    self.excluded_issues.append(issues)
                continue

if __name__ == "__main__":
    orchestrator = SwarmOrchestrator()
    asyncio.run(orchestrator.run_parallel_evolution("."))

