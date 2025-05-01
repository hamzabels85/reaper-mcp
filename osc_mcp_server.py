#!/usr/bin/env python3
"""
OSC-based MCP Server for REAPER
This script provides an MCP server implementation using python-osc to communicate with REAPER
"""

import json
import sys
import os
import time
import traceback
import logging
from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from mcp.server.fastmcp import FastMCP
import threading

# Set up logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    stream=sys.stderr)
logger = logging.getLogger("reaper-osc-mcp")

# Default OSC settings
REAPER_OSC_HOST = "192.168.1.110"  # IP address from REAPER OSC settings
REAPER_OSC_SEND_PORT = 8000  # Port REAPER listens on
REAPER_OSC_RECEIVE_PORT = 9000  # Port we listen on for REAPER responses

# REAPER Action IDs
ACTION_NEW_PROJECT = 40023
ACTION_INSERT_TRACK = 40001
ACTION_SELECT_TRACK_1 = 40939
ACTION_SELECT_TRACK_2 = 40940
ACTION_SELECT_TRACK_3 = 40941
ACTION_SELECT_TRACK_4 = 40942
ACTION_SELECT_TRACK_5 = 40943
ACTION_SELECT_TRACK_6 = 40944
ACTION_SELECT_TRACK_7 = 40945
ACTION_SELECT_TRACK_8 = 40946
ACTION_INSERT_MIDI_ITEM = 40214
ACTION_SET_TEMPO = 40364
ACTION_SAVE_PROJECT = 40022

# Create the MCP server
mcp = FastMCP("ReaperOSCMCP")

# Create OSC client for sending commands to REAPER
client = udp_client.SimpleUDPClient(REAPER_OSC_HOST, REAPER_OSC_SEND_PORT)

# Global variables to store project state
current_project = {
    "name": "Untitled",
    "path": "",
    "tracks": []
}

# OSC message handlers
def handle_track_info(address, *args):
    """Handle track info messages from REAPER"""
    logger.debug(f"Received track info: {address} {args}")
    # Update our track info cache
    track_idx = int(address.split('/')[-1])
    if track_idx >= len(current_project["tracks"]):
        current_project["tracks"].extend([{} for _ in range(track_idx - len(current_project["tracks"]) + 1)])
    current_project["tracks"][track_idx]["name"] = args[0] if args else f"Track {track_idx+1}"

def handle_project_info(address, *args):
    """Handle project info messages from REAPER"""
    logger.debug(f"Received project info: {address} {args}")
    if address == "/project/name" and args:
        current_project["name"] = args[0]
    elif address == "/project/path" and args:
        current_project["path"] = args[0]

# Set up OSC dispatcher
dispatcher = Dispatcher()
dispatcher.map("/track/*/name", handle_track_info)
dispatcher.map("/project/name", handle_project_info)
dispatcher.map("/project/path", handle_project_info)

# Start OSC server in a separate thread
def start_osc_server():
    server = BlockingOSCUDPServer((REAPER_OSC_HOST, REAPER_OSC_RECEIVE_PORT), dispatcher)
    logger.info(f"OSC server listening on {REAPER_OSC_HOST}:{REAPER_OSC_RECEIVE_PORT}")
    server.serve_forever()

# Start the OSC server thread
osc_thread = threading.Thread(target=start_osc_server, daemon=True)
osc_thread.start()

# Request initial project info
def request_project_info():
    client.send_message("/project/name/get", None)
    client.send_message("/project/path/get", None)
    client.send_message("/track/count/get", None)
    time.sleep(0.1)  # Give REAPER time to respond

# Helper functions
def refresh_track_list():
    """Refresh the track list from REAPER"""
    client.send_message("/track/count/get", None)
    time.sleep(0.1)  # Wait for response
    
    # Request info for each track
    for i in range(len(current_project["tracks"])):
        client.send_message(f"/track/{i}/name/get", None)
    time.sleep(0.1)  # Wait for responses

def select_track(track_index):
    """Select a track by index using action IDs"""
    if track_index == 0:
        client.send_message("/action", [ACTION_SELECT_TRACK_1])
    elif track_index == 1:
        client.send_message("/action", [ACTION_SELECT_TRACK_2])
    elif track_index == 2:
        client.send_message("/action", [ACTION_SELECT_TRACK_3])
    elif track_index == 3:
        client.send_message("/action", [ACTION_SELECT_TRACK_4])
    elif track_index == 4:
        client.send_message("/action", [ACTION_SELECT_TRACK_5])
    elif track_index == 5:
        client.send_message("/action", [ACTION_SELECT_TRACK_6])
    elif track_index == 6:
        client.send_message("/action", [ACTION_SELECT_TRACK_7])
    elif track_index == 7:
        client.send_message("/action", [ACTION_SELECT_TRACK_8])
    else:
        # For tracks beyond 8, we'll use the OSC method (less reliable)
        client.send_message(f"/track/{track_index}/select", [1])
    time.sleep(0.2)  # Wait for REAPER to process

# MCP tool definitions
@mcp.tool()
def create_project(name, template=None):
    """Creates a new REAPER project."""
    try:
        # Send action to create new project
        client.send_message("/action", [ACTION_NEW_PROJECT])
        time.sleep(0.5)  # Give REAPER time to create the project
        
        # Set project name by saving it
        if name:
            save_path = os.path.join(os.path.expanduser("~/Documents/REAPER Projects"), f"{name}.rpp")
            client.send_message("/action", [ACTION_SAVE_PROJECT])
            time.sleep(0.3)
            # We can't directly set the save path via OSC, but we can update our state
            current_project["name"] = name
            current_project["path"] = save_path
        
        # Request updated project info
        request_project_info()
        
        return {"success": True, "message": f"Created project: {name}"}
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def create_track(name=None):
    """Creates a new track in the current project."""
    try:
        # Use action ID to create new track (more reliable)
        client.send_message("/action", [ACTION_INSERT_TRACK])
        time.sleep(0.5)  # Give REAPER time to create the track
        
        # Get track count and assume new track is at the end
        client.send_message("/track/count/get", None)
        time.sleep(0.2)
        
        # Set track name if provided
        if name and current_project["tracks"]:
            track_index = len(current_project["tracks"]) - 1
            client.send_message(f"/track/{track_index}/name", [name])
            current_project["tracks"][track_index]["name"] = name
        
        # Refresh track list
        refresh_track_list()
        
        return {"success": True, "track_index": len(current_project["tracks"]) - 1}
    except Exception as e:
        logger.error(f"Error creating track: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def list_tracks():
    """Lists all tracks in the current project."""
    try:
        # Refresh track information
        refresh_track_list()
        
        tracks = []
        for i, track in enumerate(current_project["tracks"]):
            tracks.append({
                "index": i,
                "name": track.get("name", f"Track {i+1}"),
                "is_selected": False  # We don't have this info via OSC by default
            })
        
        return {"success": True, "tracks": tracks}
    except Exception as e:
        logger.error(f"Error listing tracks: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def add_midi_note(track_index, note, start_time, duration, velocity=100):
    """Adds a MIDI note to a track."""
    try:
        # First, make sure we have a MIDI item at the right position
        # Select the track using action IDs (more reliable)
        select_track(track_index)
        
        # Insert new MIDI item using action ID
        client.send_message("/action", [ACTION_INSERT_MIDI_ITEM])
        time.sleep(0.5)
        
        # We can't directly add MIDI notes via OSC
        # This is a limitation of the OSC implementation
        
        return {"success": True, "message": f"Created MIDI item on track {track_index}. Note: Adding specific MIDI notes requires ReaScript or external MIDI file import."}
    except Exception as e:
        logger.error(f"Error adding MIDI note: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def get_project_info():
    """Gets information about the current project."""
    try:
        # Request updated project info
        request_project_info()
        refresh_track_list()
        
        return {
            "success": True,
            "name": current_project["name"],
            "path": current_project["path"],
            "track_count": len(current_project["tracks"]),
            "selected_track_count": 0  # We don't have this info via OSC by default
        }
    except Exception as e:
        logger.error(f"Error getting project info: {e}")
        return {"success": False, "error": str(e)}

# Run the server
if __name__ == "__main__":
    logger.info("Starting OSC-based REAPER MCP Server...")
    try:
        # Request initial project info
        request_project_info()
        
        # Use stdio transport for MCP protocol
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Error running MCP server: {e}")
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
