#!/bin/bash
# Evo Setup Script for Linux/macOS
echo "Setting up Project EVO..."
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
echo "Setup complete. Run with: python cli/evo_cli.py start"
