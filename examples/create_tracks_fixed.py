#!/usr/bin/env python3
"""
Create tracks in REAPER using OSC with a different approach
This script tries different OSC commands to properly create new tracks
"""

import sys
import time
from pythonosc import udp_client

# OSC settings (matching our server configuration)
REAPER_OSC_HOST = "192.168.1.110"
REAPER_OSC_PORT = 8000

def main():
    print("Testing different methods to create tracks in REAPER...")
    
    # Create OSC client
    client = udp_client.SimpleUDPClient(REAPER_OSC_HOST, REAPER_OSC_PORT)
    
    # Method 1: Using the specific insert track command
    print("\nMethod 1: Using /track/insert command...")
    client.send_message("/track/insert", None)
    time.sleep(1)
    client.send_message("/track/0/name", ["Method 1 Track"])
    time.sleep(1)
    
    # Method 2: Using the action ID for insert track
    print("\nMethod 2: Using action ID for insert track...")
    client.send_message("/action", [40001])  # Action ID for "Insert new track"
    time.sleep(1)
    client.send_message("/track/1/name", ["Method 2 Track"])
    time.sleep(1)
    
    # Method 3: Using the track/add command with position
    print("\nMethod 3: Using /track/add with position parameter...")
    client.send_message("/track/add/last", None)
    time.sleep(1)
    client.send_message("/track/2/name", ["Method 3 Track"])
    time.sleep(1)
    
    # Method 4: Using a different command structure
    print("\nMethod 4: Using /insert/track command...")
    client.send_message("/insert/track", None)
    time.sleep(1)
    client.send_message("/track/3/name", ["Method 4 Track"])
    time.sleep(1)
    
    print("\nTest completed. Check REAPER to see which method worked for creating new tracks.")

if __name__ == "__main__":
    main()
