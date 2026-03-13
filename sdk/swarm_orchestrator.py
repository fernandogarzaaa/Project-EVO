import asyncio
import json
import logging
import os
from sdk.memory_manager import EvoMemory
try:
    import evo_core  # Importing the Rust-based swarm bridge
except ImportError:
    evo_core = None # Fallback to standard Python subprocess

class SwarmOrchestrator:
    def __init__(self, registry_path="D:/project-evo/swarms/registry.json"):
        with open(registry_path, "r") as f:
            self.registry = json.load(f)
        self.logger = logging.getLogger("EvoOrchestrator")
        logging.basicConfig(level=logging.INFO)
        self.memory = EvoMemory()

    async def deploy_agent(self, agent_role, task):
        self.logger.info(f"Deploying {agent_role} to address: {task[:50]}...")
        
        # Use Rust bridge if available, else fallback to subprocess
        if evo_core:
            return evo_core.invoke_swarm_agent(agent_role, task)
            
        process = await asyncio.create_subprocess_exec(
            "python", f"D:/project-evo/swarms/agents/{agent_role}.py", "--task", task,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return stdout.decode().strip()

    async def run_parallel_evolution(self, repo_path):
        self.logger.info("Starting Parallel Evolution Cycle on: " + repo_path)
        
        # 1. Audit (Parallelize with context gathering)
        auditor_task = asyncio.create_task(self.deploy_agent("auditor", repo_path))
        issues = await auditor_task
        
        if "ISSUE_FOUND" in issues:
            self.logger.warning("Vulnerabilities detected. Orchestrating mitigation...")
            
            # 2. Architect + Adversary in parallel (Generate plan & Red-team simultaneously)
            plan = await self.deploy_agent("architect", issues)
            adversary_check = await self.deploy_agent("adversary", plan)
            
            if "WEAKNESSES_FOUND" in adversary_check:
                self.logger.warning("Adversary caught an edge case. Re-architecting...")
                plan = await self.deploy_agent("architect", adversary_check)
                
            # 2.5 Quantum Superposition Optimization (The "Intelligence" Layer)
            optimized_plan = await self.deploy_agent("quantum_optimizer", plan)
            self.logger.info(f"Quantum Swarm selected architectural path: {optimized_plan[:30]}")
            
            # 3. Code (Implement fix)
            commit = await self.deploy_agent("coder", optimized_plan)
            
            # 4. Verify
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
    asyncio.run(orchestrator.run_parallel_evolution("D:/project-evo"))
