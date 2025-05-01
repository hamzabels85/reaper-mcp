#!/usr/bin/env python3
"""
Setup REAPER OSC Configuration

This script creates a REAPER OSC configuration file to enable OSC control
"""

import os
import sys

def setup_reaper_osc():
    # Create the .config/REAPER directory if it doesn't exist
    config_dir = os.path.expanduser("~/.config/REAPER")
    os.makedirs(config_dir, exist_ok=True)
    
    # Create the reaper-osc.ini file with OSC settings
    osc_config = """
[OSC]
MaxPacketLen=1024
EnableTCP=0
EnableUDP=1
UDPPortTx=9000
UDPPortRx=8000
FilterOutgoing=0
FilterIncoming=0
LocalNetworkOnly=1
ReceiveMidiSysex=0
DeviceName=ReaperMCP
LocalIP=192.168.1.110
"""
    
    with open(os.path.join(config_dir, "reaper-osc.ini"), "w") as f:
        f.write(osc_config)
    
    print("REAPER OSC configuration has been set up.")
    print("OSC is configured to:")
    print("- Device name: ReaperMCP")
    print("- Listen on port 8000")
    print("- Send responses to port 9000")
    print("- IP address: 192.168.1.110")
    print("- Only accept connections from the local network")
    print("Please restart REAPER for the changes to take effect.")

if __name__ == "__main__":
    setup_reaper_osc()
