#!/usr/bin/env python3
"""
Test script for OSC-based MCP server
This script directly tests the OSC communication with REAPER
"""

import sys
import time
from pythonosc import udp_client

# OSC settings (matching our server configuration)
REAPER_OSC_HOST = "192.168.1.110"
REAPER_OSC_PORT = 8000

def main():
    print("Testing OSC communication with REAPER...")
    
    # Create OSC client
    client = udp_client.SimpleUDPClient(REAPER_OSC_HOST, REAPER_OSC_PORT)
    
    # Test 1: Create a new project
    print("\nTest 1: Creating a new project...")
    client.send_message("/new", None)
    time.sleep(1)
    
    # Test 2: Add a track
    print("\nTest 2: Adding a new track...")
    client.send_message("/track/add", None)
    time.sleep(1)
    
    # Test 3: Name the track
    print("\nTest 3: Naming the track...")
    client.send_message("/track/0/name", ["OSC Test Track"])
    time.sleep(1)
    
    # Test 4: Insert MIDI item
    print("\nTest 4: Inserting MIDI item...")
    client.send_message("/track/0/select", [1])
    time.sleep(0.5)
    client.send_message("/insert/midi", None)
    time.sleep(1)
    
    # Test 5: Get project info
    print("\nTest 5: Getting project info...")
    client.send_message("/project/name/get", None)
    time.sleep(0.5)
    
    print("\nTests completed. Check REAPER to see the results.")

if __name__ == "__main__":
    main()
