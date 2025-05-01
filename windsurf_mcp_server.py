#!/usr/bin/env python3
"""
Windsurf-compatible MCP Server for REAPER
This script provides an MCP server implementation specifically designed to work with Windsurf
"""

import json
import sys
import os
import traceback
import reapy
from mcp.server.fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("ReaperMCP")

# Connect to REAPER
try:
    print("Attempting to connect to REAPER...", file=sys.stderr)
    reapy.connect()
    print("Successfully connected to REAPER", file=sys.stderr)
except Exception as e:
    print(f"Failed to connect to REAPER: {e}", file=sys.stderr)
    print("Make sure REAPER is running with ReaScript API enabled", file=sys.stderr)
    # Don't exit, just continue with warnings
    print("Continuing with warnings...", file=sys.stderr)

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
        print(f"Error creating project: {e}", file=sys.stderr)
        return {"success": False, "error": str(e)}

@mcp.tool()
def create_track(name=None):
    """Creates a new track in the current project."""
    try:
        project = reapy.Project()
        track = project.add_track(index=project.n_tracks, name=name)
        return {"success": True, "track_index": track.index}
    except Exception as e:
        print(f"Error creating track: {e}", file=sys.stderr)
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
        print(f"Error listing tracks: {e}", file=sys.stderr)
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
        print(f"Error adding MIDI note: {e}", file=sys.stderr)
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
        print(f"Error getting project info: {e}", file=sys.stderr)
        return {"success": False, "error": str(e)}

# Run the server
if __name__ == "__main__":
    print("Starting Windsurf-compatible REAPER MCP Server...", file=sys.stderr)
    try:
        # Use stdio transport for MCP protocol
        mcp.run(transport='stdio')
    except Exception as e:
        print(f"Error running MCP server: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
