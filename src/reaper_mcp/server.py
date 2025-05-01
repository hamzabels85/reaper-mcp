#!/usr/bin/env python3
"""
REAPER MCP Server implementation
This module provides the core server implementation for the REAPER MCP server
"""

import sys
import os
import time
import traceback
import logging
import reapy
from mcp.server.fastmcp import FastMCP

# Set up logging
logger = logging.getLogger("reaper_mcp.server")

class ReaperMCPServer:
    """
    REAPER MCP Server implementation using ReaScript API
    """
    
    def __init__(self):
        """Initialize the REAPER MCP Server"""
        # Create the MCP server
        self.mcp = FastMCP("ReaperMCP")
        
        # Connect to REAPER
        try:
            logger.info("Attempting to connect to REAPER...")
            reapy.connect()
            logger.info("Successfully connected to REAPER")
        except Exception as e:
            logger.error(f"Failed to connect to REAPER: {e}")
            logger.error("Make sure REAPER is running with ReaScript API enabled")
            raise
        
        # Register MCP tools
        self.register_mcp_tools()
    
    def register_mcp_tools(self):
        """Register all MCP tools"""
        
        @self.mcp.tool()
        def create_project(name, template=None):
            """Creates a new REAPER project."""
            try:
                project = reapy.Project()
                if name:
                    project.save(os.path.join(os.path.expanduser("~/Documents/REAPER Projects"), f"{name}.rpp"))
                return {"success": True, "message": f"Created project: {name}"}
            except Exception as e:
                logger.error(f"Error creating project: {e}")
                return {"success": False, "error": str(e)}
        
        @self.mcp.tool()
        def create_track(name=None):
            """Creates a new track in the current project."""
            try:
                project = reapy.Project()
                track = project.add_track(index=project.n_tracks, name=name)
                return {"success": True, "track_index": track.index}
            except Exception as e:
                logger.error(f"Error creating track: {e}")
                return {"success": False, "error": str(e)}
        
        @self.mcp.tool()
        def list_tracks():
            """Lists all tracks in the current project."""
            try:
                project = reapy.Project()
                tracks = []
                for i in range(project.n_tracks):
                    track = project.tracks[i]
                    tracks.append({
                        "index": i,
                        "name": track.name,
                        "is_selected": track.is_selected
                    })
                return {"success": True, "tracks": tracks}
            except Exception as e:
                logger.error(f"Error listing tracks: {e}")
                return {"success": False, "error": str(e)}
        
        @self.mcp.tool()
        def add_midi_note(track_index, note, start_time, duration, velocity=100):
            """Adds a MIDI note to a track."""
            try:
                project = reapy.Project()
                track = project.tracks[track_index]
                item = track.add_item(start=start_time, length=duration)
                take = item.add_take()
                take.add_note(note=note, start=0, end=duration, velocity=velocity)
                return {"success": True, "message": f"Added note {note} to track {track_index}"}
            except Exception as e:
                logger.error(f"Error adding MIDI note: {e}")
                return {"success": False, "error": str(e)}
        
        @self.mcp.tool()
        def get_project_info():
            """Gets information about the current project."""
            try:
                project = reapy.Project()
                return {
                    "success": True,
                    "name": project.name,
                    "path": project.path,
                    "length": project.length,
                    "track_count": project.n_tracks,
                    "selected_track_count": project.n_selected_tracks
                }
            except Exception as e:
                logger.error(f"Error getting project info: {e}")
                return {"success": False, "error": str(e)}
    
    def run(self, transport='stdio', **kwargs):
        """Run the MCP server"""
        logger.info("Starting ReaScript-based REAPER MCP Server...")
        try:
            # Use specified transport for MCP protocol
            self.mcp.run(transport=transport, **kwargs)
        except Exception as e:
            logger.error(f"Error running MCP server: {e}")
            traceback.print_exc(file=sys.stderr)
            sys.exit(1)


def create_server():
    """
    Create and return a REAPER MCP Server instance
    
    Returns:
        ReaperMCPServer: The REAPER MCP Server instance
    """
    return ReaperMCPServer()


def main():
    """Main entry point for the REAPER MCP Server"""
    # Set up logging
    logging.basicConfig(level=logging.DEBUG, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        stream=sys.stderr)
    
    # Create and run the server
    try:
        server = create_server()
        server.run()
    except Exception as e:
        logger.error(f"Error initializing server: {e}")
        logger.error("Falling back to OSC mode...")
        
        # Import and use OSC server as fallback
        from reaper_mcp.osc_server import create_server as create_osc_server
        server = create_osc_server()
        server.run()


if __name__ == "__main__":
    main()
