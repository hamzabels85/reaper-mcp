import argparse
import json
import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP
import reapy

from .project_tools import ProjectTools
from .track_tools import TrackTools
from .midi_tools import MidiTools
from .audio_tools import AudioTools
from .fx_tools import FXTools
from .mixing_tools import MixingTools
from .mastering_tools import MasteringTools
from .render_tools import RenderTools
from .analysis_tools import AnalysisTools
from .config import load_config


def create_server():
    """Create and configure the MCP server with all REAPER tools."""
    parser = argparse.ArgumentParser(description='REAPER MCP Server')
    parser.add_argument('--config', type=str, default='config.json',
                       help='Path to configuration file')
    args = parser.parse_args()
    
    # Load configuration
    config_path = args.config
    config = load_config(config_path)
    
    # Connect to REAPER
    try:
        reapy.connect()
        print("Successfully connected to REAPER")
    except Exception as e:
        print(f"Failed to connect to REAPER: {e}")
        print("Make sure REAPER is running with ReaScript API enabled")
        return None
    
    # Create MCP server
    server = FastMCP("reaper-mcp-server")
    
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
    
    # Register Project Management Tools
    @server.tool()
    def create_new_project(tempo: float = 120.0, time_signature: str = "4/4", name: str = "New Project"):
        """Creates a new REAPER project with specified parameters."""
        return json.dumps(project_tools.create_new_project(tempo, time_signature, name))
    
    @server.tool()
    def save_project(project_path: str = ""):
        """Saves the current project to the specified path."""
        return json.dumps(project_tools.save_project(project_path))
    
    @server.tool()
    def load_project(project_path: str):
        """Loads a REAPER project from the specified path."""
        return json.dumps(project_tools.load_project(project_path))
    
    @server.tool()
    def get_project_info():
        """Returns information about the current project."""
        return json.dumps(project_tools.get_project_info())
    
    # Register Track Tools
    @server.tool()
    def create_track(name: str, track_type: str = "audio"):
        """Creates a new track with the specified name and type."""
        return json.dumps(track_tools.create_track(name, track_type))
    
    @server.tool()
    def set_track_parameters(track_id: int, volume: float = None, pan: float = None, 
                            mute: bool = None, solo: bool = None):
        """Sets parameters for the specified track."""
        return json.dumps(track_tools.set_track_parameters(
            track_id, volume, pan, mute, solo))
    
    @server.tool()
    def get_track_info(track_id: int):
        """Gets information about the specified track."""
        return json.dumps(track_tools.get_track_info(track_id))
    
    @server.tool()
    def list_tracks():
        """Lists all tracks in the current project."""
        return json.dumps(track_tools.list_tracks())
    
    # Register MIDI Tools
    @server.tool()
    def create_midi_item(track_id: int, start_position: float, length: float):
        """Creates a new MIDI item on the specified track."""
        return json.dumps(midi_tools.create_midi_item(track_id, start_position, length))
    
    @server.tool()
    def add_midi_note(item_id: int, pitch: int, start: float, length: float, velocity: int = 100):
        """Adds a MIDI note to the specified MIDI item."""
        return json.dumps(midi_tools.add_midi_note(item_id, pitch, start, length, velocity))
    
    @server.tool()
    def create_chord_progression(track_id: int, chords: str, start_position: float, 
                               beats_per_chord: int = 4):
        """Creates a chord progression on the specified track."""
        return json.dumps(midi_tools.create_chord_progression(
            track_id, chords, start_position, beats_per_chord))
    
    @server.tool()
    def create_drum_pattern(track_id: int, pattern: str, start_position: float, 
                          beats: int = 4, repeats: int = 1):
        """Creates a drum pattern on the specified track."""
        return json.dumps(midi_tools.create_drum_pattern(
            track_id, pattern, start_position, beats, repeats))
    
    # Register Audio Tools
    @server.tool()
    def import_audio_file(file_path: str, track_id: int, position: float = 0.0):
        """Imports an audio file to the specified track."""
        return json.dumps(audio_tools.import_audio_file(file_path, track_id, position))
    
    @server.tool()
    def record_audio(track_id: int, length: float, input: str = ""):
        """Records audio on the specified track."""
        return json.dumps(audio_tools.record_audio(track_id, length, input))
    
    @server.tool()
    def edit_audio_item(item_id: int, start_trim: float = None, end_trim: float = None, 
                      fade_in: float = None, fade_out: float = None):
        """Edits the specified audio item."""
        return json.dumps(audio_tools.edit_audio_item(
            item_id, start_trim, end_trim, fade_in, fade_out))
    
    # Register FX Tools
    @server.tool()
    def add_vst_instrument(track_id: int, vst_name: str):
        """Adds a VST instrument to the specified track."""
        return json.dumps(fx_tools.add_vst_instrument(track_id, vst_name))
    
    @server.tool()
    def add_vst_effect(track_id: int, vst_name: str):
        """Adds a VST effect to the specified track."""
        return json.dumps(fx_tools.add_vst_effect(track_id, vst_name))
    
    @server.tool()
    def set_vst_parameter(track_id: int, fx_id: int, param_index: int, value: float):
        """Sets a parameter value for the specified VST."""
        return json.dumps(fx_tools.set_vst_parameter(track_id, fx_id, param_index, value))
    
    @server.tool()
    def list_available_vsts(vst_type: str = "all"):
        """Lists all available VSTs of the specified type."""
        return json.dumps(fx_tools.list_available_vsts(vst_type))
    
    # Register Mixing Tools
    @server.tool()
    def add_automation_point(track_id: int, parameter: str, position: float, value: float):
        """Adds an automation point for the specified parameter."""
        return json.dumps(mixing_tools.add_automation_point(track_id, parameter, position, value))
    
    @server.tool()
    def create_send(source_track_id: int, destination_track_id: int, volume: float = 0.0):
        """Creates a send between the specified tracks."""
        return json.dumps(mixing_tools.create_send(source_track_id, destination_track_id, volume))
    
    @server.tool()
    def create_bus(name: str, tracks: list):
        """Creates a bus track and routes the specified tracks to it."""
        return json.dumps(mixing_tools.create_bus(name, tracks))
    
    # Register Mastering Tools
    @server.tool()
    def add_master_fx(fx_name: str):
        """Adds an effect to the master track."""
        return json.dumps(mastering_tools.add_master_fx(fx_name))
    
    @server.tool()
    def analyze_loudness():
        """Analyzes the project loudness and returns metrics."""
        return json.dumps(mastering_tools.analyze_loudness())
    
    @server.tool()
    def apply_mastering_chain(preset: str = "default"):
        """Applies a mastering chain to the master track."""
        return json.dumps(mastering_tools.apply_mastering_chain(preset))
    
    # Register Render Tools
    @server.tool()
    def render_project(output_path: str, format: str = "wav", 
                     sample_rate: int = 44100, bit_depth: int = 24):
        """Renders the project to the specified file."""
        return json.dumps(render_tools.render_project(
            output_path, format, sample_rate, bit_depth))
    
    @server.tool()
    def render_stems(output_directory: str, tracks: list = None):
        """Renders stems for the specified tracks."""
        return json.dumps(render_tools.render_stems(output_directory, tracks))
    
    # Register Analysis Tools
    @server.tool()
    def analyze_frequency_spectrum(item_id: int = None):
        """Analyzes the frequency spectrum of the specified item or project."""
        return json.dumps(analysis_tools.analyze_frequency_spectrum(item_id))
    
    @server.tool()
    def detect_clipping():
        """Detects clipping in the project."""
        return json.dumps(analysis_tools.detect_clipping())
    
    @server.tool()
    def analyze_mix_balance():
        """Analyzes the mix balance across the frequency spectrum."""
        return json.dumps(analysis_tools.analyze_mix_balance())
    
    return server


def main():
    """Main entry point for the REAPER MCP server."""
    server = create_server()
    if server:
        print("Starting REAPER MCP Server...")
        server.run(transport='stdio')  # Can be changed to 'http' for HTTP transport
    else:
        print("Failed to create REAPER MCP Server")


if __name__ == "__main__":
    main()
