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
- OSC support enabled in REAPER (for OSC mode)
- ReaScript API enabled in REAPER (for ReaScript mode)

## Installation

```bash
# Clone the repository
git clone https://github.com/itsuzef/reaper-mcp.git
cd reaper-mcp

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

## Usage

### Quick Start

The easiest way to get started is to use the provided startup script:

```bash
# Start REAPER first
open /Applications/REAPER.app  # On macOS
# or start REAPER manually on other platforms

# Then start the MCP server
./scripts/start_reaper_mcp_server.sh  # On Unix/Mac
```

#### Windows Users

For Windows users, use one of the provided Windows scripts:

```cmd
# Using Command Prompt (CMD)
scripts\start_reaper_mcp_server.bat

# Using PowerShell
powershell -ExecutionPolicy Bypass -File scripts\start_reaper_mcp_server.ps1
```

### Configuration

By default, the server will use OSC mode, which is more reliable and doesn't require the ReaScript API to be working correctly. You can configure the server using command-line arguments:

```bash
# Start in OSC mode (default)
./scripts/start_reaper_mcp_server.sh --mode=osc  # Unix/Mac
scripts\start_reaper_mcp_server.bat --mode=osc   # Windows CMD
powershell -File scripts\start_reaper_mcp_server.ps1 -mode osc  # Windows PowerShell

# Start in ReaScript mode
./scripts/start_reaper_mcp_server.sh --mode=reapy  # Unix/Mac
scripts\start_reaper_mcp_server.bat --mode=reapy   # Windows CMD
powershell -File scripts\start_reaper_mcp_server.ps1 -mode reapy  # Windows PowerShell

# Configure OSC settings (Unix/Mac)
./scripts/start_reaper_mcp_server.sh --host=192.168.1.110 --send-port=8000 --receive-port=9000

# Configure OSC settings (Windows CMD)
scripts\start_reaper_mcp_server.bat --host=192.168.1.110 --send-port=8000 --receive-port=9000

# Configure OSC settings (Windows PowerShell)
powershell -File scripts\start_reaper_mcp_server.ps1 -host "192.168.1.110" -sendPort 8000 -receivePort 9000

# Enable debug logging
./scripts/start_reaper_mcp_server.sh --debug  # Unix/Mac
scripts\start_reaper_mcp_server.bat --debug   # Windows CMD
powershell -File scripts\start_reaper_mcp_server.ps1 -debug  # Windows PowerShell
```

### Setting up REAPER for OSC

1. Open REAPER
2. Go to Preferences > Control/OSC/web
3. Click "Add" and select "OSC (Open Sound Control)"
4. Configure the following settings:
   - Device name: ReaperMCP
   - Mode: Local port
   - Local listen port: 8000
   - Local IP: 127.0.0.1 (or your computer's IP address)
   - Allow binding messages to REAPER actions and FX learn: Checked (optional)
   - Outgoing max packet size: 1024
   - Wait between packets: 10ms

### Setting up REAPER for ReaScript

1. Open REAPER
2. Go to Preferences > Plug-ins > ReaScript
3. Make sure "Enable Python for ReaScript" is checked
4. Set the Python DLL/dylib path to your Python installation
   - On macOS: `/opt/homebrew/Cellar/python@3.x/3.x.x/Frameworks/Python.framework/Versions/3.x/Python`
   - On Windows: `C:\Path\to\Python\python3x.dll`
5. Run the setup script:
   ```bash
   python scripts/setup_reaper_python.py
   ```

## Project Structure

- `src/reaper_mcp/`: Main package directory
  - `__main__.py`: Command-line interface
  - `osc_server.py`: OSC-based server implementation
  - `server.py`: ReaScript-based server implementation
- `examples/`: Example scripts demonstrating usage
- `scripts/`: Utility scripts for setup and running

## MCP Tools

The server provides the following MCP tools:

- `create_project`: Creates a new REAPER project
- `create_track`: Creates a new track in the current project
- `list_tracks`: Lists all tracks in the current project
- `add_midi_note`: Adds a MIDI note to a track
- `get_project_info`: Gets information about the current project

## Troubleshooting

### ReaScript API Issues

If you're experiencing issues with the ReaScript API, try using the OSC mode instead:

```bash
./scripts/start_reaper_mcp_server.sh --mode=osc
```

### OSC Communication Issues

Make sure REAPER is configured correctly for OSC:
1. Check that the OSC settings in REAPER match the server settings
2. Verify that no firewall is blocking the communication
3. Try using the local IP address (127.0.0.1) instead of a network IP

### Windows-Specific Troubleshooting

If you're having issues running the MCP server on Windows:

1. **Script Execution Issues**:
   - For PowerShell scripts, you may need to adjust the execution policy: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
   - Alternatively, use the `-ExecutionPolicy Bypass` flag as shown in the examples

2. **Path Issues**:
   - Ensure the REAPER path in the scripts matches your installation location
   - Default is `C:\Program Files\REAPER\reaper.exe`, modify if needed

3. **Virtual Environment**:
   - If you created the venv with a different method, the activation script might be in a different location
   - Try activating manually before running: `venv\Scripts\activate`

4. **Firewall Blocking**:
   - Windows Firewall may block OSC communication
   - Add exceptions for Python and REAPER in Windows Firewall settings

5. **Administrator Rights**:
   - Try running the Command Prompt or PowerShell as Administrator if you encounter permission issues

## License

MIT
