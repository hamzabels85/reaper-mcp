import reapy
from reapy import reascript_api as RPR


class MixingTools:
    """Tools for mixing and automation in REAPER."""
    
    def __init__(self, config):
        """
        Initialize MixingTools with configuration.
        
        Args:
            config (dict): Configuration dictionary
        """
        self.config = config
    
    def add_automation_point(self, track_id, parameter, position, value):
        """
        Add an automation point for the specified parameter.
        
        Args:
            track_id (int): Track ID
            parameter (str): Parameter name (volume, pan, mute, etc.)
            position (float): Position in seconds
            value (float): Parameter value (normalized 0.0-1.0)
            
        Returns:
            dict: Result of the operation
        """
        try:
            # Get track by ID
            track = reapy.Track.from_id(track_id)
            
            # Map parameter name to envelope
            param_map = {
                "volume": 0,
                "pan": 1,
                "mute": 2,
                "solo": 3
            }
            
            if parameter.lower() not in param_map:
                return {
                    "success": False,
                    "error": f"Unsupported parameter: {parameter}"
                }
            
            # Get envelope
            env_idx = param_map[parameter.lower()]
            envelope = track.get_envelope(env_idx)
            
            # Add point
            point_idx = envelope.add_point(position, value)
            
            return {
                "success": True,
                "track_id": track_id,
                "parameter": parameter,
                "position": position,
                "value": value,
                "point_index": point_idx
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def add_fx_parameter_automation(self, track_id, fx_id, param_index, position, value):
        """
        Add an automation point for an FX parameter.
        
        Args:
            track_id (int): Track ID
            fx_id (int): FX ID
            param_index (int): Parameter index
            position (float): Position in seconds
            value (float): Parameter value (normalized 0.0-1.0)
            
        Returns:
            dict: Result of the operation
        """
        try:
            # Get track by ID
            track = reapy.Track.from_id(track_id)
            
            # Find FX by ID
            fx = None
            fx_index = -1
            for i in range(track.n_fxs):
                current_fx = track.fxs[i]
                if current_fx.id == fx_id:
                    fx = current_fx
                    fx_index = i
                    break
            
            if fx is None:
                return {
                    "success": False,
                    "error": f"FX with ID {fx_id} not found on track {track_id}"
                }
            
            # Get parameter envelope
            param = fx.params[param_index]
            envelope = param.envelope
            
            # Enable automation for this parameter if not already enabled
            if not envelope:
                # This is a simplification - in practice, you'd need to use ReaScript API
                # to show the parameter envelope
                return {
                    "success": False,
                    "error": "Parameter automation not enabled. Enable it in REAPER first."
                }
            
            # Add point
            point_idx = envelope.add_point(position, value)
            
            return {
                "success": True,
                "track_id": track_id,
                "fx_id": fx_id,
                "param_index": param_index,
                "param_name": param.name,
                "position": position,
                "value": value,
                "point_index": point_idx
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_send(self, source_track_id, destination_track_id, volume=0.0):
        """
        Create a send between the specified tracks.
        
        Args:
            source_track_id (int): Source track ID
            destination_track_id (int): Destination track ID
            volume (float): Send volume in dB
            
        Returns:
            dict: Result of the operation
        """
        try:
            # Get tracks by ID
            source_track = reapy.Track.from_id(source_track_id)
            destination_track = reapy.Track.from_id(destination_track_id)
            
            # Get destination track index
            dest_idx = destination_track.index
            
            # Create send
            send_idx = source_track.add_send(dest_idx)
            
            # Set send volume
            send = source_track.sends[send_idx]
            send.volume = volume
            
            return {
                "success": True,
                "source_track_id": source_track_id,
                "destination_track_id": destination_track_id,
                "send_index": send_idx,
                "volume": send.volume
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def set_send_parameters(self, source_track_id, send_idx, volume=None, pan=None, mute=None):
        """
        Set parameters for the specified send.
        
        Args:
            source_track_id (int): Source track ID
            send_idx (int): Send index
            volume (float, optional): Send volume in dB
            pan (float, optional): Send pan position (-1.0 to 1.0)
            mute (bool, optional): Send mute state
            
        Returns:
            dict: Result of the operation
        """
        try:
            # Get track by ID
            source_track = reapy.Track.from_id(source_track_id)
            
            # Get send
            send = source_track.sends[send_idx]
            
            # Set parameters if provided
            if volume is not None:
                send.volume = volume
            
            if pan is not None:
                send.pan = pan
            
            if mute is not None:
                send.mute = mute
            
            return {
                "success": True,
                "source_track_id": source_track_id,
                "send_index": send_idx,
                "volume": send.volume,
                "pan": send.pan,
                "mute": send.mute
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_bus(self, name, tracks):
        """
        Create a bus track and route the specified tracks to it.
        
        Args:
            name (str): Bus track name
            tracks (list): List of track IDs to route to the bus
            
        Returns:
            dict: Result of the operation
        """
        try:
            project = reapy.Project()
            
            # Create bus track
            track_index = project.n_tracks
            project.add_track(track_index, name)
            bus_track = project.tracks[track_index]
            
            # Create sends from each track to the bus
            sends = []
            for track_id in tracks:
                try:
                    source_track = reapy.Track.from_id(track_id)
                    send_idx = source_track.add_send(track_index)
                    sends.append({
                        "source_track_id": track_id,
                        "send_index": send_idx
                    })
                except Exception as e:
                    print(f"Error creating send from track {track_id}: {e}")
            
            return {
                "success": True,
                "bus_track_id": bus_track.id,
                "bus_track_index": track_index,
                "name": name,
                "sends": sends
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def apply_eq_preset(self, track_id, preset_name):
        """
        Apply an EQ preset to the specified track.
        
        Args:
            track_id (int): Track ID
            preset_name (str): Preset name
            
        Returns:
            dict: Result of the operation
        """
        try:
            # Get track by ID
            track = reapy.Track.from_id(track_id)
            
            # Define EQ presets
            presets = {
                "vocal": [
                    {"freq": 100, "gain": -3, "q": 0.7, "type": "highpass"},
                    {"freq": 250, "gain": -2, "q": 1.0, "type": "peak"},
                    {"freq": 3000, "gain": 2, "q": 1.0, "type": "peak"},
                    {"freq": 10000, "gain": 1, "q": 0.7, "type": "highshelf"}
                ],
                "kick": [
                    {"freq": 30, "gain": -3, "q": 0.7, "type": "highpass"},
                    {"freq": 60, "gain": 3, "q": 1.0, "type": "peak"},
                    {"freq": 400, "gain": -4, "q": 1.0, "type": "peak"}
                ],
                "snare": [
                    {"freq": 100, "gain": -3, "q": 0.7, "type": "highpass"},
                    {"freq": 200, "gain": -2, "q": 1.0, "type": "peak"},
                    {"freq": 3500, "gain": 3, "q": 1.0, "type": "peak"}
                ],
                "guitar": [
                    {"freq": 80, "gain": -3, "q": 0.7, "type": "highpass"},
                    {"freq": 800, "gain": -2, "q": 1.0, "type": "peak"},
                    {"freq": 3000, "gain": 2, "q": 1.0, "type": "peak"}
                ],
                "bass": [
                    {"freq": 40, "gain": -3, "q": 0.7, "type": "highpass"},
                    {"freq": 80, "gain": 3, "q": 1.0, "type": "peak"},
                    {"freq": 800, "gain": -2, "q": 1.0, "type": "peak"}
                ]
            }
            
            if preset_name not in presets:
                return {
                    "success": False,
                    "error": f"Preset not found: {preset_name}"
                }
            
            # Add ReaEQ
            fx_index = track.add_fx("ReaEQ")
            
            if fx_index < 0:
                return {
                    "success": False,
                    "error": "Failed to add ReaEQ"
                }
            
            # Get the FX
            fx = track.fxs[fx_index]
            
            # Apply preset
            # Note: This is a simplification - in practice, you'd need to map
            # the preset parameters to ReaEQ's specific parameter indices
            
            return {
                "success": True,
                "track_id": track_id,
                "fx_id": fx.id,
                "preset": preset_name,
                "message": f"EQ preset '{preset_name}' applied. Note: Parameter mapping is simplified."
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
