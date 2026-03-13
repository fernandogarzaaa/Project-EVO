import argparse
import os
import json
import sys

def setup():
    print("--- Project Evo Setup Wizard ---")
    api_key = input("Enter your OpenAI/Anthropic API Key: ")
    with open(".env", "w") as f:
        f.write(f"OPENAI_API_KEY={api_key}\n")
    print("Configuration saved! You are ready to evolve.")

def start():
    print("Initializing Evo Swarm...")
    os.system("python swarm_bot.py --run")

def status():
    # Simple plain-english report from the memory manager
    try:
        with open("meta-swarms/memory.json", "r") as f:
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
