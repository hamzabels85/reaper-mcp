#!/usr/bin/env python3
"""
HTTP Transport version of the REAPER MCP Server
This script runs the REAPER MCP server with HTTP transport instead of stdio
"""

import sys
import os
from reaper_mcp.server import create_server

def main():
    """Run the REAPER MCP server with HTTP transport"""
    server = create_server()
    if server:
        print("Starting REAPER MCP Server with HTTP transport...")
        # Run with HTTP transport
        server.run(transport='http')
    else:
        print("Failed to create REAPER MCP Server")
        sys.exit(1)

if __name__ == "__main__":
    main()
