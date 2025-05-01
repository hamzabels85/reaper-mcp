"""
REAPER MCP Server Package
A comprehensive Model Context Protocol (MCP) server for REAPER DAW
"""

__version__ = "0.1.0"

from .server import create_server as create_reapy_server
from .osc_server import create_server as create_osc_server

# Convenience function to create the appropriate server based on mode
def create_server(mode="osc", **kwargs):
    """
    Create a REAPER MCP server instance
    
    Args:
        mode (str): Server mode - 'osc' for OSC-based server, 'reapy' for ReaScript-based server
        **kwargs: Additional arguments to pass to the server constructor
        
    Returns:
        The REAPER MCP server instance
    """
    if mode == "osc":
        return create_osc_server(**kwargs)
    else:
        return create_reapy_server(**kwargs)
