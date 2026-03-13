import argparse
import sys
import subprocess
import os

# Tester Agent: Dynamically executes the correct test suite
def run_tests():
    print("Detecting test environment...")
    
    if os.path.exists("package.json"):
        print("Node.js environment detected. Running npm test...")
        result = subprocess.run(["npm", "test"], capture_output=True, text=True)
    elif os.path.exists("Cargo.toml"):
        print("Rust environment detected. Running cargo test...")
        result = subprocess.run(["cargo", "test"], capture_output=True, text=True)
    elif os.path.exists("pytest.ini") or os.path.exists("tests"):
        print("Python environment detected. Running pytest...")
        result = subprocess.run([sys.executable, "-m", "pytest", "tests"], capture_output=True, text=True)
    else:
        print("No standard test suite detected. Defaulting to Python unittest discover...")
        result = subprocess.run(["python", "-m", "unittest", "discover", "-s", "."], capture_output=True, text=True)

    if result.returncode == 0:
        return "VERIFIED: Test suite passed perfectly."
    else:
        return f"TEST_FAILED: {result.stderr or result.stdout}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task")
    args = parser.parse_args()
    
    # Run actual tests
    verification = run_tests()
    print(verification)
