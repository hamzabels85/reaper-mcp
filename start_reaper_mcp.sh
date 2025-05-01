#!/bin/bash
# Start REAPER MCP Server for Windsurf

# Ensure REAPER is running
if ! pgrep -x "REAPER" > /dev/null; then
    echo "Starting REAPER..."
    open /Applications/REAPER.app
    # Give REAPER time to start up
    sleep 3
fi

# Activate the Python virtual environment
source "$(dirname "$0")/venv/bin/activate"

# Set the Python path to include the reaper-mcp directory
export PYTHONPATH="$(dirname "$0"):$PYTHONPATH"

# Run the MCP server with stdio transport
exec python "$(dirname "$0")/windsurf_mcp_server.py"
