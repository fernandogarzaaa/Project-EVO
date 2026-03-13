import argparse
import logging
import asyncio
from sdk.swarm_orchestrator import SwarmOrchestrator

# The Swarm Bot: The orchestrator's public interface, similar to AppForge's entry point
class SwarmBot:
    def __init__(self):
        self.orchestrator = SwarmOrchestrator()
        self.logger = logging.getLogger("SwarmBot")
        logging.basicConfig(level=logging.INFO)

    def start_autonomous_loop(self):
        self.logger.info("Initializing Autonomous Evolution Swarm...")
        asyncio.run(self.orchestrator.run_parallel_evolution("."))
        self.logger.info("Evolution loop completed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()

    if args.run:
        bot = SwarmBot()
        bot.start_autonomous_loop()
    else:
        print("Usage: python swarm_bot.py --run")
