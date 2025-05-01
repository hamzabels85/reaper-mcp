import reapy
from reapy import reascript_api as RPR


class TrackTools:
    """Tools for managing REAPER tracks."""
    
    def __init__(self, config):
        """
        Initialize TrackTools with configuration.
        
        Args:
            config (dict): Configuration dictionary
        """
        self.config = config
    
    def create_track(self, name, track_type="audio"):
        """
        Create a new track with the specified name and type.
        
        Args:
            name (str): Track name
            track_type (str): Track type (audio, midi, instrument, folder)
            
        Returns:
            dict: Track information
        """
        try:
            project = reapy.Project()
            
            # Create new track at the end of the project
            track_index = project.n_tracks
            project.add_track(track_index, name)
            
            # Get the new track
            track = project.tracks[track_index]
            
            # Set track properties based on type
            if track_type == "midi":
                # Configure for MIDI input
                track.input_mode = reapy.InputMode.ALL_MIDI
            elif track_type == "instrument":
                # Configure for MIDI input and add instrument placeholder
                track.input_mode = reapy.InputMode.ALL_MIDI
                # Note: Actual instrument would be added with FXTools
            elif track_type == "folder":
                # Make it a folder track
                track.is_folder = True
            
            # Return track info
            return {
                "success": True,
                "track_id": track.id,
                "index": track_index,
                "name": track.name,
                "type": track_type
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def set_track_parameters(self, track_id, volume=None, pan=None, mute=None, solo=None):
        """
        Set parameters for the specified track.
        
        Args:
            track_id (int): Track ID
            volume (float, optional): Volume in dB (-inf to +12)
            pan (float, optional): Pan position (-1.0 to 1.0)
            mute (bool, optional): Mute state
            solo (bool, optional): Solo state
            
        Returns:
            dict: Result of the operation
        """
        try:
            # Get track by ID
            track = reapy.Track.from_id(track_id)
            
            # Set parameters if provided
            if volume is not None:
                # Convert dB to REAPER's volume scale
                track.volume = volume
            
            if pan is not None:
                track.pan = pan
            
            if mute is not None:
                track.mute = mute
            
            if solo is not None:
                track.solo = solo
            
            # Return updated track info
            return {
                "success": True,
                "track_id": track.id,
                "name": track.name,
                "volume": track.volume,
                "pan": track.pan,
                "mute": track.mute,
                "solo": track.solo
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_track_info(self, track_id):
        """
        Get information about the specified track.
        
        Args:
            track_id (int): Track ID
            
        Returns:
            dict: Track information
        """
        try:
            # Get track by ID
            track = reapy.Track.from_id(track_id)
            
            # Get FX on track
            fx_list = []
            for i in range(track.n_fxs):
                fx = track.fxs[i]
                fx_list.append({
                    "index": i,
                    "name": fx.name,
                    "enabled": fx.enabled
                })
            
            # Get items on track
            items = []
            for i in range(track.n_items):
                item = track.items[i]
                item_info = {
                    "index": i,
                    "position": item.position,
                    "length": item.length,
                    "name": item.name,
                    "is_midi": item.is_midi
                }
                items.append(item_info)
            
            # Return track info
            return {
                "success": True,
                "track_id": track.id,
                "index": track.index,
                "name": track.name,
                "volume": track.volume,
                "pan": track.pan,
                "mute": track.mute,
                "solo": track.solo,
                "armed": track.armed,
                "input": track.input,
                "fx": fx_list,
                "items": items,
                "is_folder": track.is_folder,
                "folder_depth": track.folder_depth,
                "color": track.color
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def list_tracks(self):
        """
        List all tracks in the current project.
        
        Returns:
            dict: List of tracks
        """
        try:
            project = reapy.Project()
            
            tracks = []
            for i in range(project.n_tracks):
                track = project.tracks[i]
                tracks.append({
                    "track_id": track.id,
                    "index": i,
                    "name": track.name,
                    "is_folder": track.is_folder,
                    "folder_depth": track.folder_depth
                })
            
            return {
                "success": True,
                "count": len(tracks),
                "tracks": tracks
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
