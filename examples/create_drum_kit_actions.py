#!/usr/bin/env python3
"""
Create a drum kit in REAPER using OSC action IDs
This script uses REAPER's specific action IDs to create tracks properly
"""

import sys
import time
from pythonosc import udp_client

# OSC settings (matching our server configuration)
REAPER_OSC_HOST = "192.168.1.110"
REAPER_OSC_PORT = 8000

# REAPER Action IDs
ACTION_NEW_PROJECT = 40023
ACTION_INSERT_TRACK = 40001
ACTION_SELECT_TRACK_1 = 40939
ACTION_SELECT_TRACK_2 = 40940
ACTION_SELECT_TRACK_3 = 40941
ACTION_SELECT_TRACK_4 = 40942
ACTION_INSERT_MIDI_ITEM = 40214
ACTION_SET_TEMPO = 40364

def main():
    print("Creating a drum kit in REAPER using action IDs...")
    
    # Create OSC client
    client = udp_client.SimpleUDPClient(REAPER_OSC_HOST, REAPER_OSC_PORT)
    
    # Create a new project
    print("Creating a new project...")
    client.send_message("/action", [ACTION_NEW_PROJECT])
    time.sleep(1.5)
    
    # Create drum tracks (we need to create 4 tracks)
    track_names = ["Kick", "Snare", "Hi-Hat", "Crash"]
    
    for i, name in enumerate(track_names):
        if i > 0:  # First track already exists, create additional tracks
            print(f"Creating track {i+1}...")
            client.send_message("/action", [ACTION_INSERT_TRACK])
            time.sleep(0.8)
        
        # Select the track (track 1 is already selected after creation)
        if i == 1:
            client.send_message("/action", [ACTION_SELECT_TRACK_2])
        elif i == 2:
            client.send_message("/action", [ACTION_SELECT_TRACK_3])
        elif i == 3:
            client.send_message("/action", [ACTION_SELECT_TRACK_4])
        time.sleep(0.5)
        
        # Name the track
        print(f"Naming track: {name}...")
        client.send_message(f"/track/{i}/name", [name])
        time.sleep(0.5)
        
        # Insert MIDI item
        print(f"Adding MIDI item to {name} track...")
        client.send_message("/action", [ACTION_INSERT_MIDI_ITEM])
        time.sleep(0.8)
    
    # Set project tempo to 120 BPM
    print("Setting project tempo to 120 BPM...")
    # First select tempo dialog
    client.send_message("/action", [ACTION_SET_TEMPO])
    time.sleep(0.8)
    # Then send the tempo value (this might not work via OSC, but worth trying)
    client.send_message("/tempo", [120.0])
    time.sleep(0.5)
    
    print("\nDrum kit created with the following tracks:")
    for name in track_names:
        print(f"- {name}")
    
    print("\nCheck REAPER to see if the tracks were created properly.")
    print("You may need to manually set the tempo to 120 BPM if that didn't work via OSC.")

if __name__ == "__main__":
    main()
