#!/usr/bin/env python3
"""
Create a simple drum pattern in REAPER using OSC
This script demonstrates how to create a more complex musical pattern using OSC
"""

import sys
import time
from pythonosc import udp_client

# OSC settings (matching our server configuration)
REAPER_OSC_HOST = "192.168.1.110"
REAPER_OSC_PORT = 8000

def main():
    print("Creating a drum pattern in REAPER using OSC...")
    
    # Create OSC client
    client = udp_client.SimpleUDPClient(REAPER_OSC_HOST, REAPER_OSC_PORT)
    
    # Create a new project
    print("Creating a new project...")
    client.send_message("/new", None)
    time.sleep(1)
    
    # Set project tempo to 120 BPM
    print("Setting project tempo to 120 BPM...")
    client.send_message("/tempo", [120.0])
    time.sleep(0.5)
    
    # Create drum tracks
    track_names = ["Kick", "Snare", "Hi-Hat", "Crash"]
    
    for i, name in enumerate(track_names):
        print(f"Creating track: {name}...")
        client.send_message("/track/add", None)
        time.sleep(0.5)
        client.send_message(f"/track/{i}/name", [name])
        time.sleep(0.2)
    
    # Create a 4-bar pattern (16 beats at 4/4)
    print("Creating MIDI items for the pattern...")
    
    # Pattern definitions (1 = hit, 0 = rest)
    patterns = {
        "Kick":   [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        "Snare":  [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        "Hi-Hat": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        "Crash":  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }
    
    # Create MIDI items for each track
    for i, (track_name, pattern) in enumerate(patterns.items()):
        # Select the track
        client.send_message(f"/track/{i}/select", [1])
        time.sleep(0.2)
        
        # Insert a 4-bar MIDI item
        client.send_message("/insert/midi", None)
        time.sleep(0.5)
        
        # We can't directly add MIDI notes via OSC
        # But we've created the MIDI items that can be edited in REAPER
        
        print(f"Created pattern for {track_name}")
    
    print("\nDrum pattern created! You'll need to add the actual MIDI notes in REAPER.")
    print("The pattern structure is:")
    
    # Print the pattern as a visual representation
    for name, pattern in patterns.items():
        pattern_str = ""
        for beat in pattern:
            pattern_str += "X " if beat == 1 else "- "
        print(f"{name.ljust(8)}: {pattern_str}")
    
    print("\nYou can now open the MIDI editor in REAPER to add the notes according to this pattern.")

if __name__ == "__main__":
    main()
