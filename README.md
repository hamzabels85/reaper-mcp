# REAPER MCP Server

A comprehensive Model Context Protocol (MCP) server that enables AI agents to create fully mixed and mastered tracks in REAPER with both MIDI and audio capabilities.

## Features

- Complete project management (creation, saving, rendering)
- Track operations (creation, routing, parameter adjustment)
- MIDI composition and editing
- Audio recording and importing
- Virtual instrument and effect management
- Mixing and automation
- Mastering tools
- Audio analysis and feedback

## Requirements

- REAPER DAW installed
- Python 3.8+
- ReaPy (Python bindings for REAPER)
- MCP Server library

## Installation

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

## Usage

1. Start REAPER
2. Launch the MCP server:
   ```bash
   python -m reaper_mcp.server
   ```
3. Connect your AI client to the MCP server

## Tools

The server provides a comprehensive set of tools for AI-driven music production:

- Project management tools
- Track and routing tools
- MIDI composition tools
- Audio recording and editing tools
- Virtual instrument and effect tools
- Mixing and automation tools
- Mastering tools
- Analysis and feedback tools

## Configuration

Configure the server by editing the `config.json` file:

```json
{
  "reaper_path": "/path/to/reaper",
  "default_project_directory": "/path/to/projects",
  "vst_directories": ["/path/to/vsts"],
  "sample_libraries": ["/path/to/samples"]
}
```

## License

MIT
