import argparse
import os
import json
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def setup():
    print("--- Project Evo Setup Wizard ---")
    api_key = input("Enter your OpenAI/Anthropic API Key: ")
    with open(os.path.join(BASE_DIR, ".env"), "w") as f:
        f.write(f"OPENAI_API_KEY={api_key}\n")
    print("Configuration saved! You are ready to evolve.")

def start():
    import subprocess
    print("Initializing Evo Swarm...")
    subprocess.run([sys.executable, os.path.join(BASE_DIR, "swarm_bot.py"), "--run"])

def status():
    # Simple plain-english report from the memory manager
    try:
        with open(os.path.join(BASE_DIR, "meta-swarms/memory.json"), "r") as f:
            mem = json.load(f)
            history = mem.get("history", [])
            last = history[-1] if history else {"status": "No evolution cycles yet."}
            print(f"Current Evo Status: {last.get('status', 'Stable')}")
    except:
        print("Evo is not running. Run 'evo start' to initialize.")

def main():
    parser = argparse.ArgumentParser(description="Project Evo Command Center")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("setup", help="Interactive setup wizard")
    subparsers.add_parser("start", help="Start the autonomous swarm bot")
    subparsers.add_parser("status", help="Get a human-readable status report")

    args = parser.parse_args()

    if args.command == "setup":
        setup()
    elif args.command == "start":
        start()
    elif args.command == "status":
        status()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
