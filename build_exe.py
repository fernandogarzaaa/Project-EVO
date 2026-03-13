import os
import subprocess
import shutil

# Build script for Project Evo CLI
def build_evo():
    print("--- Packaging Project Evo into evo.exe ---")
    
    # Ensure pyinstaller is installed
    subprocess.run(["pip", "install", "pyinstaller"], check=True)
    
    # Build the executable
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name", "evo",
        "cli/evo_cli.py",
        "--add-data", "swarms/registry.json;swarms/",
        "--add-data", "sdk/llm_client.py;sdk/",
        "--clean"
    ]
    
    subprocess.run(cmd, check=True)
    print("Build complete! Your binary is in the /dist folder.")

if __name__ == "__main__":
    build_evo()
