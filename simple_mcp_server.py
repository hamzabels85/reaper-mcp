#!/usr/bin/env python3
"""
Simple MCP Server for REAPER
This script provides a minimal MCP server that should work with IDE integration
"""

import json
import sys
import os
import reapy
from mcp.server.fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("ReaperMCP")

# Connect to REAPER
try:
    reapy.connect()
    print("Successfully connected to REAPER", file=sys.stderr)
except Exception as e:
    print(f"Failed to connect to REAPER: {e}", file=sys.stderr)
    print("Make sure REAPER is running with ReaScript API enabled", file=sys.stderr)
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
        return {"success": False, "error": str(e)}

@mcp.tool()
def create_track(name=None):
    """Creates a new track in the current project."""
    try:
        project = reapy.Project()
        track = project.add_track(index=project.n_tracks, name=name)
        return {"success": True, "track_index": track.index}
    except Exception as e:
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
        return {"success": False, "error": str(e)}

# Run the server
if __name__ == "__main__":
    print("Starting simple REAPER MCP Server...", file=sys.stderr)
    mcp.run()
