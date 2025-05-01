#!/usr/bin/env python3
"""
Main entry point for the REAPER MCP Server
"""

import sys
import os
import argparse
import logging
from reaper_mcp.osc_server import create_server as create_osc_server
from reaper_mcp.server import create_server as create_reapy_server

def main():
    """Main entry point for the REAPER MCP Server"""
    # Set up argument parser
    parser = argparse.ArgumentParser(description="REAPER MCP Server")
    parser.add_argument("--mode", choices=["osc", "reapy"], default="osc",
                        help="Server mode: 'osc' for OSC-based server, 'reapy' for ReaScript-based server")
    parser.add_argument("--host", default="127.0.0.1",
                        help="Host IP address for OSC communication (OSC mode only)")
    parser.add_argument("--send-port", type=int, default=8000,
                        help="Port REAPER listens on for OSC messages (OSC mode only)")
    parser.add_argument("--receive-port", type=int, default=9000,
                        help="Port we listen on for REAPER responses (OSC mode only)")
    parser.add_argument("--transport", choices=["stdio", "http"], default="stdio",
                        help="Transport protocol for MCP communication")
    parser.add_argument("--http-port", type=int, default=8080,
                        help="Port for HTTP transport (if transport=http)")
    parser.add_argument("--debug", action="store_true",
                        help="Enable debug logging")
    
    args = parser.parse_args()
    
    # Set up logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        stream=sys.stderr)
    
    logger = logging.getLogger("reaper_mcp")
    logger.info(f"Starting REAPER MCP Server in {args.mode} mode")
    
    try:
        # Create and run the server based on the selected mode
        if args.mode == "osc":
            logger.info(f"Using OSC communication with REAPER at {args.host}:{args.send_port}")
            server = create_osc_server(args.host, args.send_port, args.receive_port)
        else:  # reapy mode
            logger.info("Using ReaScript API for REAPER communication")
            server = create_reapy_server()
        
        # Run the server with the specified transport
        if args.transport == "http":
            logger.info(f"Using HTTP transport on port {args.http_port}")
            server.run(transport="http", port=args.http_port)
        else:
            logger.info("Using stdio transport")
            server.run(transport="stdio")
            
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Error running server: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
