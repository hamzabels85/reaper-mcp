#!/usr/bin/env python3
"""
HTTP-compatible REAPER MCP Server
This script runs the REAPER MCP server with proper configuration for IDE integration
"""

import sys
import os
import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator
import reapy
from mcp.server.fastmcp import FastMCP, Context

from reaper_mcp.project_tools import ProjectTools
from reaper_mcp.track_tools import TrackTools
from reaper_mcp.midi_tools import MidiTools
from reaper_mcp.audio_tools import AudioTools
from reaper_mcp.fx_tools import FXTools
from reaper_mcp.mixing_tools import MixingTools
from reaper_mcp.mastering_tools import MasteringTools
from reaper_mcp.render_tools import RenderTools
from reaper_mcp.analysis_tools import AnalysisTools
from reaper_mcp.config import load_config

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ReaperMCPServer")

# Global variables for tools
config = None
project_tools = None
track_tools = None
midi_tools = None
audio_tools = None
fx_tools = None
mixing_tools = None
mastering_tools = None
render_tools = None
analysis_tools = None

@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[None]:
    """Manage server startup and shutdown lifecycle"""
    global config, project_tools, track_tools, midi_tools, audio_tools, fx_tools
    global mixing_tools, mastering_tools, render_tools, analysis_tools
    
    logger.info("Starting REAPER MCP Server...")
    
    # Load configuration
    config_path = os.environ.get("REAPER_MCP_CONFIG", "config.json")
    config = load_config(config_path)
    
    # Connect to REAPER
    try:
        reapy.connect()
        logger.info("Successfully connected to REAPER")
        
        # Initialize tool modules
        project_tools = ProjectTools(config)
        track_tools = TrackTools(config)
        midi_tools = MidiTools(config)
        audio_tools = AudioTools(config)
        fx_tools = FXTools(config)
        mixing_tools = MixingTools(config)
        mastering_tools = MasteringTools(config)
        render_tools = RenderTools(config)
        analysis_tools = AnalysisTools(config)
        
        yield
    except Exception as e:
        logger.error(f"Failed to connect to REAPER: {e}")
        logger.error("Make sure REAPER is running with ReaScript API enabled")
    finally:
        logger.info("REAPER MCP Server shutting down...")

# Create the MCP server with lifespan support
mcp = FastMCP(
    "ReaperMCP",
    description="REAPER integration through the Model Context Protocol",
    lifespan=server_lifespan
)

# Tool definitions
@mcp.tool()
def create_project(ctx: Context, name: str, template: str = None):
    """Creates a new REAPER project."""
    result = project_tools.create_project(name, template)
    return {"success": True, "project_path": result}

@mcp.tool()
def save_project(ctx: Context, path: str = None):
    """Saves the current REAPER project."""
    result = project_tools.save_project(path)
    return {"success": True, "project_path": result}

@mcp.tool()
def create_track(ctx: Context, name: str = None):
    """Creates a new track in the current project."""
    track_id = track_tools.create_track(name)
    return {"success": True, "track_id": track_id}

@mcp.tool()
def create_midi_item(ctx: Context, track_id: int, start_time: float, length: float):
    """Creates a new MIDI item on the specified track."""
    item_id = midi_tools.create_midi_item(track_id, start_time, length)
    return {"success": True, "item_id": item_id}

@mcp.tool()
def add_notes(ctx: Context, item_id: int, notes: list):
    """Adds MIDI notes to the specified MIDI item."""
    midi_tools.add_notes(item_id, notes)
    return {"success": True}

@mcp.tool()
def add_vst_plugin(ctx: Context, track_id: int, plugin_name: str):
    """Adds a VST plugin to the specified track."""
    fx_id = fx_tools.add_vst_plugin(track_id, plugin_name)
    return {"success": True, "fx_id": fx_id}

@mcp.tool()
def render_project(ctx: Context, output_path: str, format: str = "wav", 
                  sample_rate: int = 44100, bit_depth: int = 24):
    """Renders the current project to a file."""
    result = render_tools.render_project(output_path, format, sample_rate, bit_depth)
    return {"success": True, "output_path": result}

def main():
    """Run the MCP server"""
    mcp.run()

if __name__ == "__main__":
    main()
