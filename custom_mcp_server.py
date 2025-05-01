#!/usr/bin/env python3
"""
Custom MCP Server for REAPER
This script provides a robust MCP server implementation that should work with IDE integration
"""

import json
import sys
import os
import reapy
from mcp.server.fastmcp import FastMCP
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    stream=sys.stderr)
logger = logging.getLogger("reaper-mcp")

# Create the MCP server
mcp = FastMCP("ReaperMCP")

# Connect to REAPER
try:
    logger.info("Attempting to connect to REAPER...")
    reapy.connect()
    logger.info("Successfully connected to REAPER")
except Exception as e:
    logger.error(f"Failed to connect to REAPER: {e}")
    logger.error("Make sure REAPER is running with ReaScript API enabled")
    sys.exit(1)

# Simple tool definitions
@mcp.tool()
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

@mcp.tool()
def create_track(name=None):
    """Creates a new track in the current project."""
    try:
        project = reapy.Project()
        track = project.add_track(index=project.n_tracks, name=name)
        return {"success": True, "track_index": track.index}
    except Exception as e:
        logger.error(f"Error creating track: {e}")
        return {"success": False, "error": str(e)}

@mcp.tool()
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

@mcp.tool()
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

@mcp.tool()
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

# Run the server
if __name__ == "__main__":
    logger.info("Starting custom REAPER MCP Server...")
    # Use stdio transport for MCP protocol
    mcp.run(transport='stdio')
