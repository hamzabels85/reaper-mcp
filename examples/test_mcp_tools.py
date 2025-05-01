#!/usr/bin/env python3
"""
Test script for the MCP tools using our OSC-based implementation
This script demonstrates how to use the MCP tools to create a simple project
"""

import sys
import time
import json
import subprocess
import os

def call_mcp_tool(tool_name, **params):
    """Call an MCP tool and return the result"""
    # Create the MCP request
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "callTool",
        "params": {
            "name": tool_name,
            "parameters": params
        }
    }
    
    # Call the MCP server
    cmd = ["/Users/youssefhemimy/Documents/reaper-mcp/start_osc_mcp.sh"]
    proc = subprocess.Popen(cmd, 
                           stdin=subprocess.PIPE, 
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE,
                           universal_newlines=True)
    
    # Send the request
    request_json = json.dumps(request) + "\n"
    stdout, stderr = proc.communicate(input=request_json)
    
    # Parse the response
    try:
        response = json.loads(stdout.strip())
        if "result" in response:
            return response["result"]
        else:
            print(f"Error: {response.get('error', 'Unknown error')}")
            return None
    except json.JSONDecodeError:
        print(f"Error decoding response: {stdout}")
        print(f"Stderr: {stderr}")
        return None

def main():
    print("Testing MCP tools with OSC-based implementation...")
    
    # Test 1: Create a new project
    print("\nTest 1: Creating a new project...")
    result = call_mcp_tool("mcp2_create_project", name="MCP Test Project")
    print(f"Result: {result}")
    
    # Wait for REAPER to process
    time.sleep(2)
    
    # Test 2: Create tracks
    print("\nTest 2: Creating tracks...")
    track_names = ["Drums", "Bass", "Guitar", "Vocals"]
    track_indices = []
    
    for name in track_names:
        result = call_mcp_tool("mcp2_create_track", name=name)
        print(f"Created track '{name}': {result}")
        if result and result.get("success"):
            track_indices.append(result.get("track_index", 0))
        time.sleep(1)
    
    # Test 3: List tracks
    print("\nTest 3: Listing tracks...")
    result = call_mcp_tool("mcp2_list_tracks")
    print(f"Tracks: {result}")
    
    # Test 4: Add MIDI notes
    print("\nTest 4: Adding MIDI notes...")
    if track_indices:
        for i, track_idx in enumerate(track_indices):
            # Add a MIDI note to each track
            note = 60 + i * 4  # C4, E4, G4, C5
            result = call_mcp_tool("mcp2_add_midi_note", 
                                  track_index=track_idx,
                                  note=str(note),
                                  start_time="0.0",
                                  duration="1.0",
                                  velocity="100")
            print(f"Added note to track {track_idx}: {result}")
            time.sleep(1)
    
    # Test 5: Get project info
    print("\nTest 5: Getting project info...")
    result = call_mcp_tool("mcp2_get_project_info")
    print(f"Project info: {result}")
    
    print("\nTests completed. Check REAPER to see the results.")

if __name__ == "__main__":
    main()
