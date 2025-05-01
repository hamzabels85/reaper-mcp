#!/bin/bash
# Start REAPER MCP Server
# This script starts the REAPER MCP server in the appropriate mode

# Default settings
MODE="osc"
HOST="127.0.0.1"
SEND_PORT=8000
RECEIVE_PORT=9000
TRANSPORT="stdio"
DEBUG=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --mode=*)
      MODE="${1#*=}"
      shift
      ;;
    --host=*)
      HOST="${1#*=}"
      shift
      ;;
    --send-port=*)
      SEND_PORT="${1#*=}"
      shift
      ;;
    --receive-port=*)
      RECEIVE_PORT="${1#*=}"
      shift
      ;;
    --transport=*)
      TRANSPORT="${1#*=}"
      shift
      ;;
    --debug)
      DEBUG=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Ensure REAPER is running
if ! pgrep -x "REAPER" > /dev/null; then
    echo "Starting REAPER..."
    open /Applications/REAPER.app
    # Give REAPER time to start up
    sleep 3
fi

# Activate the Python virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Set debug flag if needed
DEBUG_FLAG=""
if [ "$DEBUG" = true ]; then
    DEBUG_FLAG="--debug"
fi

# Run the MCP server with the specified options
echo "Starting REAPER MCP Server in $MODE mode..."
python -m reaper_mcp --mode=$MODE --host=$HOST --send-port=$SEND_PORT --receive-port=$RECEIVE_PORT --transport=$TRANSPORT $DEBUG_FLAG
