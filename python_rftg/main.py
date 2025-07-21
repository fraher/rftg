"""
Main entry point for Race for the Galaxy Python implementation.
"""

import sys
import os

# Add src directory to path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src import main

if __name__ == "__main__":
    main()
