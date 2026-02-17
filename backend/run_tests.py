#!/usr/bin/env python3
"""
Test runner for the Todo App Backend.
Executes all tests and validates coverage.
"""

import subprocess
import sys
import os

def run_tests():
    """Run all tests and validate coverage."""
    print("Running tests for Todo App Backend...")

    # Change to the backend directory if not already there
    if os.getcwd().endswith('fullstacktodoApp'):
        os.chdir('backend')

    # Run pytest with coverage
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--cov=src",
        "--cov-report=html",
        "--cov-report=term-missing"
    ]

    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("\n✓ All tests passed!")
        print("✓ Coverage report generated in htmlcov/ directory")
        return True
    else:
        print(f"\n✗ Tests failed with return code: {result.returncode}")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)