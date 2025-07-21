#!/usr/bin/env python3
"""
Development helper script for Race for the Galaxy Python implementation.

This script provides common development tasks like testing, linting, and running the game.
"""

import sys
import subprocess
import os
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and return the result."""
    if description:
        print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode == 0

def check_venv():
    """Check if we're running in a virtual environment."""
    return hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python dev.py <command>")
        print("Commands:")
        print("  test      - Run tests")
        print("  lint      - Run code quality checks")
        print("  format    - Format code with black")
        print("  type      - Run type checking")
        print("  install   - Install dependencies")
        print("  clean     - Clean up build artifacts")
        print("  run       - Run the game")
        return

    if not check_venv():
        print("Warning: Not running in a virtual environment!")
        print("Please activate the virtual environment first:")
        if os.name == 'nt':  # Windows
            print("  .\\venv\\Scripts\\Activate.ps1")
        else:  # Unix/Linux/Mac
            print("  source venv/bin/activate")
        return

    command = sys.argv[1]
    
    if command == "test":
        run_command(["pytest", "-v"], "Running tests")
    
    elif command == "lint":
        success = True
        success &= run_command(["flake8", "src/", "tests/"], "Running flake8")
        success &= run_command(["mypy", "src/"], "Running mypy")
        if not success:
            print("Linting failed!")
            sys.exit(1)
    
    elif command == "format":
        run_command(["black", "src/", "tests/"], "Formatting code")
    
    elif command == "type":
        run_command(["mypy", "src/"], "Running type checking")
    
    elif command == "install":
        run_command(["pip", "install", "--upgrade", "pip"], "Upgrading pip")
        run_command(["pip", "install", "-r", "requirements.txt"], "Installing dependencies")
        run_command(["pip", "install", "-e", "."], "Installing package in development mode")
    
    elif command == "clean":
        import shutil
        dirs_to_clean = ["__pycache__", ".pytest_cache", ".mypy_cache", "htmlcov", "build", "dist"]
        for root, dirs, files in os.walk("."):
            for d in dirs:
                if d in dirs_to_clean:
                    dir_path = Path(root) / d
                    print(f"Removing {dir_path}")
                    shutil.rmtree(dir_path, ignore_errors=True)
    
    elif command == "run":
        run_command(["python", "main.py"], "Running Race for the Galaxy")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
