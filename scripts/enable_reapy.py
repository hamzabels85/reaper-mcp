"""
Enable ReaPy Server Script for REAPER

This script enables the ReaPy server in REAPER, allowing external Python scripts
to control REAPER via the ReaPy library.

To use:
1. In REAPER, go to Actions > Show action list
2. Click on "New..." button
3. Select "Run Python script" and choose this file
4. Run the action

After running this script, restart REAPER for the changes to take effect.
"""

# This is the simplest way to enable the ReaPy server
import os

def enable_reapy_server():
    # Create the .config/REAPER directory if it doesn't exist
    config_dir = os.path.expanduser("~/.config/REAPER")
    os.makedirs(config_dir, exist_ok=True)
    
    # Create the enable_distant_api.txt file
    with open(os.path.join(config_dir, "enable_distant_api.txt"), "w") as f:
        f.write("1")
    
    # Print confirmation message
    print("ReaPy distant API has been enabled.")
    print("Please restart REAPER for the changes to take effect.")

# Run the function
enable_reapy_server()
