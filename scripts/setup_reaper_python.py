#!/usr/bin/env python3
"""
Setup REAPER Python API Configuration

This script sets up REAPER to work with Python by:
1. Enabling the distant API
2. Setting the Python library path
"""

import os
import subprocess
import sys

def setup_reaper_python():
    # Create the .config/REAPER directory if it doesn't exist
    config_dir = os.path.expanduser("~/.config/REAPER")
    os.makedirs(config_dir, exist_ok=True)
    
    # Create the enable_distant_api.txt file
    with open(os.path.join(config_dir, "enable_distant_api.txt"), "w") as f:
        f.write("1")
    
    # Create reaper-python.ini file with the Python library path
    python_lib_path = "/opt/homebrew/Cellar/python@3.13/3.13.2/Frameworks/Python.framework/Versions/3.13/Python"
    
    with open(os.path.join(config_dir, "reaper-python.ini"), "w") as f:
        f.write(f"PYTHONLIBRARY={python_lib_path}\n")
    
    print("REAPER Python configuration has been set up.")
    print("Python library path:", python_lib_path)
    print("Distant API has been enabled.")
    print("Please restart REAPER for the changes to take effect.")

if __name__ == "__main__":
    setup_reaper_python()
