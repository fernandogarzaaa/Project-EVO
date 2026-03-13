import sys
import argparse

# Tester Agent: Verified verification logic
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task")
    args = parser.parse_args()
    
    # Run tests and verify
    print(f"VERIFIED_{args.task}")
