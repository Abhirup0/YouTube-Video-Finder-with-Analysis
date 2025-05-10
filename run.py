#!/usr/bin/env python3
"""
Entry point script for YouTube Video Finder
"""
import os
import sys

# Add src directory to path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
sys.path.append(src_path)

# Import main module and run
from main import main

if __name__ == "__main__":
    sys.exit(main()) 