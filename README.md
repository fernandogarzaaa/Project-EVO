# Project Evo: The Autonomous Self-Evolution Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Project Evo** is an autonomous software organism. It manages, heals, and evolves your codebases automatically. You don't need to be a developer to run it—it is designed to act as your tireless software engineer.

---

## The Concept: Digital Biology
Project Evo acts as an organism with a "brain" (LLM-agnostic) and a "swarm" of internal specialists:
*   **Auditor:** Constant security and stability monitoring.
*   **Architect:** Plans optimized, robust code changes.
*   **Adversary:** Stress-tests your code to find hidden bugs *before* they are applied.
*   **Coder:** Applies fixes via Pull Requests (PRs).
*   **Tester:** Verifies changes to ensure 0% regression risk.

---

## How to use Project Evo

You don't need to edit code. Use the **Evo CLI** to control your swarm.

### 1. Initial Setup
Download the `evo.exe` binary, or run it via Python:
```bash
python D:\project-evo\cli\evo_cli.py setup
```
The wizard will securely ask for your API credentials (OpenAI/Anthropic) to power the swarm's intelligence.

### 2. Launching Evolution
Start your autonomous swarm bot in the background:
```bash
python D:\project-evo\cli\evo_cli.py start
```
The bot will begin auditing your repository, identifying risks, and generating PRs for fixes—all autonomously.

### 3. Monitoring Status
Check the bot's health and evolution progress anytime:
```bash
python D:\project-evo\cli\evo_cli.py status
```
*This provides a human-readable summary of how many bugs were healed, synaptic pathways optimized, and evolutions completed.*

---

## Safety & Governance
*   **Human-in-the-Loop:** Evo never commits directly to your `main` branch. It opens a **Pull Request (PR)**. You (or your team) retain 100% control over the final merge.
*   **Adversarial Defense:** Every autonomous fix is "Red-Teamed" by our Adversary swarm agent to ensure security before it reaches your Pull Requests.

---

## Advanced Usage (Power Users)
If you prefer a portable, containerized deployment, you can use our Docker image:

1. **Build:** `docker build -t project-evo .`
2. **Run:** `docker run -it -v $(pwd):/app project-evo`

---

## License
MIT
