import asyncio
import json
import logging
import os
import sys

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

    async def deploy_agent(self, agent_role, task):
        self.logger.info(f"Deploying {agent_role} to address: {task[:50]}...")
        
        # Use Rust bridge if available, else fallback to subprocess
        if evo_core:
            return evo_core.invoke_swarm_agent(agent_role, task)
            
        agent_script = os.path.join(BASE_DIR, "swarms", "agents", f"{agent_role}.py")
        process = await asyncio.create_subprocess_exec(
            sys.executable, agent_script, "--task", task,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=os.getcwd()  # Execute in the target repo's working directory
        )
        stdout, stderr = await process.communicate()
        # Log stderr if it crashed
        if process.returncode != 0:
            self.logger.error(f"{agent_role} failed: {stderr.decode().strip()}")
        return stdout.decode().strip()

    async def run_parallel_evolution(self, repo_path):
        self.logger.info("Starting Parallel Evolution Cycle on: " + repo_path)
        
        # 1. Audit (Parallelize with context gathering)
        repo_context = self.retriever.get_repo_map()
        auditor_task = asyncio.create_task(self.deploy_agent("auditor", repo_context))
        issues = await auditor_task
        
        if "ISSUE_FOUND" in issues:
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
            else:
                self.memory.log_failure(issues, report)
                self.logger.error("Evolution cycle failed.")
        else:
            self.logger.info("System is optimal. No changes required.")

if __name__ == "__main__":
    orchestrator = SwarmOrchestrator()
    asyncio.run(orchestrator.run_parallel_evolution("."))
