#!/usr/bin/env python3
"""
OSC-based MCP Server for REAPER
This module provides an MCP server implementation using python-osc to communicate with REAPER
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
logger = logging.getLogger("reaper_mcp.osc_server")

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


class ReaperOSCServer:
    """
    REAPER OSC Server implementation for MCP
    """
    
    def __init__(self, host="127.0.0.1", send_port=8000, receive_port=9000):
        """
        Initialize the REAPER OSC Server
        
        Args:
            host (str): The IP address of the REAPER instance
            send_port (int): The port REAPER listens on for OSC messages
            receive_port (int): The port we listen on for REAPER responses
        """
        self.host = host
        self.send_port = send_port
        self.receive_port = receive_port
        
        # Create the MCP server
        self.mcp = FastMCP("ReaperOSCMCP")
        
        # Create OSC client for sending commands to REAPER
        self.client = udp_client.SimpleUDPClient(self.host, self.send_port)
        
        # Global variables to store project state
        self.current_project = {
            "name": "Untitled",
            "path": "",
            "tracks": []
        }
        
        # Set up OSC dispatcher
        self.dispatcher = Dispatcher()
        self.dispatcher.map("/track/*/name", self.handle_track_info)
        self.dispatcher.map("/project/name", self.handle_project_info)
        self.dispatcher.map("/project/path", self.handle_project_info)
        
        # Start OSC server in a separate thread
        self.osc_thread = threading.Thread(target=self.start_osc_server, daemon=True)
        self.osc_thread.start()
        
        # Register MCP tools
        self.register_mcp_tools()
        
        # Request initial project info
        self.request_project_info()
    
    def start_osc_server(self):
        """Start the OSC server to listen for REAPER responses"""
        server = BlockingOSCUDPServer((self.host, self.receive_port), self.dispatcher)
        logger.info(f"OSC server listening on {self.host}:{self.receive_port}")
        server.serve_forever()
    
    def handle_track_info(self, address, *args):
        """Handle track info messages from REAPER"""
        logger.debug(f"Received track info: {address} {args}")
        # Update our track info cache
        track_idx = int(address.split('/')[-1])
        if track_idx >= len(self.current_project["tracks"]):
            self.current_project["tracks"].extend([{} for _ in range(track_idx - len(self.current_project["tracks"]) + 1)])
        self.current_project["tracks"][track_idx]["name"] = args[0] if args else f"Track {track_idx+1}"
    
    def handle_project_info(self, address, *args):
        """Handle project info messages from REAPER"""
        logger.debug(f"Received project info: {address} {args}")
        if address == "/project/name" and args:
            self.current_project["name"] = args[0]
        elif address == "/project/path" and args:
            self.current_project["path"] = args[0]
    
    def request_project_info(self):
        """Request project information from REAPER"""
        self.client.send_message("/project/name/get", None)
        self.client.send_message("/project/path/get", None)
        self.client.send_message("/track/count/get", None)
        time.sleep(0.1)  # Give REAPER time to respond
    
    def refresh_track_list(self):
        """Refresh the track list from REAPER"""
        self.client.send_message("/track/count/get", None)
        time.sleep(0.1)  # Wait for response
        
        # Request info for each track
        for i in range(len(self.current_project["tracks"])):
            self.client.send_message(f"/track/{i}/name/get", None)
        time.sleep(0.1)  # Wait for responses
    
    def select_track(self, track_index):
        """Select a track by index using action IDs"""
        if track_index == 0:
            self.client.send_message("/action", [ACTION_SELECT_TRACK_1])
        elif track_index == 1:
            self.client.send_message("/action", [ACTION_SELECT_TRACK_2])
        elif track_index == 2:
            self.client.send_message("/action", [ACTION_SELECT_TRACK_3])
        elif track_index == 3:
            self.client.send_message("/action", [ACTION_SELECT_TRACK_4])
        elif track_index == 4:
            self.client.send_message("/action", [ACTION_SELECT_TRACK_5])
        elif track_index == 5:
            self.client.send_message("/action", [ACTION_SELECT_TRACK_6])
        elif track_index == 6:
            self.client.send_message("/action", [ACTION_SELECT_TRACK_7])
        elif track_index == 7:
            self.client.send_message("/action", [ACTION_SELECT_TRACK_8])
        else:
            # For tracks beyond 8, we'll use the OSC method (less reliable)
            self.client.send_message(f"/track/{track_index}/select", [1])
        time.sleep(0.2)  # Wait for REAPER to process
    
    def register_mcp_tools(self):
        """Register all MCP tools"""
        
        @self.mcp.tool()
        def create_project(name, template=None):
            """Creates a new REAPER project."""
            try:
                # Send action to create new project
                self.client.send_message("/action", [ACTION_NEW_PROJECT])
                time.sleep(0.5)  # Give REAPER time to create the project
                
                # Set project name by saving it
                if name:
                    save_path = os.path.join(os.path.expanduser("~/Documents/REAPER Projects"), f"{name}.rpp")
                    self.client.send_message("/action", [ACTION_SAVE_PROJECT])
                    time.sleep(0.3)
                    # We can't directly set the save path via OSC, but we can update our state
                    self.current_project["name"] = name
                    self.current_project["path"] = save_path
                
                # Request updated project info
                self.request_project_info()
                
                return {"success": True, "message": f"Created project: {name}"}
            except Exception as e:
                logger.error(f"Error creating project: {e}")
                return {"success": False, "error": str(e)}
        
        @self.mcp.tool()
        def create_track(name=None):
            """Creates a new track in the current project."""
            try:
                # Use action ID to create new track (more reliable)
                self.client.send_message("/action", [ACTION_INSERT_TRACK])
                time.sleep(0.5)  # Give REAPER time to create the track
                
                # Get track count and assume new track is at the end
                self.client.send_message("/track/count/get", None)
                time.sleep(0.2)
                
                # Set track name if provided
                if name and self.current_project["tracks"]:
                    track_index = len(self.current_project["tracks"]) - 1
                    self.client.send_message(f"/track/{track_index}/name", [name])
                    self.current_project["tracks"][track_index]["name"] = name
                
                # Refresh track list
                self.refresh_track_list()
                
                return {"success": True, "track_index": len(self.current_project["tracks"]) - 1}
            except Exception as e:
                logger.error(f"Error creating track: {e}")
                return {"success": False, "error": str(e)}
        
        @self.mcp.tool()
        def list_tracks():
            """Lists all tracks in the current project."""
            try:
                # Refresh track information
                self.refresh_track_list()
                
                tracks = []
                for i, track in enumerate(self.current_project["tracks"]):
                    tracks.append({
                        "index": i,
                        "name": track.get("name", f"Track {i+1}"),
                        "is_selected": False  # We don't have this info via OSC by default
                    })
                
                return {"success": True, "tracks": tracks}
            except Exception as e:
                logger.error(f"Error listing tracks: {e}")
                return {"success": False, "error": str(e)}
        
        @self.mcp.tool()
        def add_midi_note(track_index, note, start_time, duration, velocity=100):
            """Adds a MIDI note to a track."""
            try:
                # First, make sure we have a MIDI item at the right position
                # Select the track using action IDs (more reliable)
                self.select_track(track_index)
                
                # Insert new MIDI item using action ID
                self.client.send_message("/action", [ACTION_INSERT_MIDI_ITEM])
                time.sleep(0.5)
                
                # We can't directly add MIDI notes via OSC
                # This is a limitation of the OSC implementation
                
                return {"success": True, "message": f"Created MIDI item on track {track_index}. Note: Adding specific MIDI notes requires ReaScript or external MIDI file import."}
            except Exception as e:
                logger.error(f"Error adding MIDI note: {e}")
                return {"success": False, "error": str(e)}
        
        @self.mcp.tool()
        def get_project_info():
            """Gets information about the current project."""
            try:
                # Request updated project info
                self.request_project_info()
                self.refresh_track_list()
                
                return {
                    "success": True,
                    "name": self.current_project["name"],
                    "path": self.current_project["path"],
                    "track_count": len(self.current_project["tracks"]),
                    "selected_track_count": 0  # We don't have this info via OSC by default
                }
            except Exception as e:
                logger.error(f"Error getting project info: {e}")
                return {"success": False, "error": str(e)}
    
    def run(self, transport='stdio'):
        """Run the MCP server"""
        logger.info("Starting OSC-based REAPER MCP Server...")
        try:
            # Use specified transport for MCP protocol
            self.mcp.run(transport=transport)
        except Exception as e:
            logger.error(f"Error running MCP server: {e}")
            traceback.print_exc(file=sys.stderr)
            sys.exit(1)


def create_server(host="127.0.0.1", send_port=8000, receive_port=9000):
    """
    Create and return a REAPER OSC Server instance
    
    Args:
        host (str): The IP address of the REAPER instance
        send_port (int): The port REAPER listens on for OSC messages
        receive_port (int): The port we listen on for REAPER responses
        
    Returns:
        ReaperOSCServer: The REAPER OSC Server instance
    """
    return ReaperOSCServer(host, send_port, receive_port)


def main():
    """Main entry point for the REAPER OSC Server"""
    # Set up logging
    logging.basicConfig(level=logging.DEBUG, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        stream=sys.stderr)
    
    # Create and run the server
    server = create_server()
    server.run()


if __name__ == "__main__":
    main()
