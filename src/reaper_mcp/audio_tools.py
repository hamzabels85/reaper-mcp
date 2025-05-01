import os
from pathlib import Path

import reapy
from reapy import reascript_api as RPR


class AudioTools:
    """Tools for audio recording and editing in REAPER."""
    
    def __init__(self, config):
        """
        Initialize AudioTools with configuration.
        
        Args:
            config (dict): Configuration dictionary
        """
        self.config = config
    
    def import_audio_file(self, file_path, track_id, position=0.0):
        """
        Import an audio file to the specified track.
        
        Args:
            file_path (str): Path to the audio file
            track_id (int): Track ID
            position (float): Position in seconds
            
        Returns:
            dict: Audio item information
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return {
                    "success": False,
                    "error": f"Audio file not found: {file_path}"
                }
            
            # Get track by ID
            track = reapy.Track.from_id(track_id)
            
            # Import audio file
            item = track.add_item(position, 0)  # Length will be determined by file
            take = item.add_take(file_path)
            
            # Update item length based on media source
            source = take.source
            item.length = source.length
            
            return {
                "success": True,
                "item_id": item.id,
                "take_id": take.id,
                "position": item.position,
                "length": item.length,
                "track_id": track_id,
                "file_path": file_path
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def record_audio(self, track_id, length, input=""):
        """
        Record audio on the specified track.
        
        Args:
            track_id (int): Track ID
            length (float): Recording length in seconds
            input (str): Input device/channel (optional)
            
        Returns:
            dict: Recording information
        """
        try:
            # Get project and track
            project = reapy.Project()
            track = reapy.Track.from_id(track_id)
            
            # Set track input if specified
            if input:
                track.input = input
            
            # Arm track for recording
            track.armed = True
            
            # Get current cursor position
            start_position = project.cursor_position
            
            # Create time selection for recording
            project.time_selection = (start_position, start_position + length)
            
            # Start recording
            RPR.Main_OnCommand(1013, 0)  # Transport: Record
            
            # Wait for recording to complete
            RPR.time_precise()
            start_time = RPR.time_precise()
            
            # Return immediately with recording information
            # The recording will continue in REAPER
            return {
                "success": True,
                "track_id": track_id,
                "start_position": start_position,
                "expected_end_position": start_position + length,
                "expected_length": length,
                "recording_in_progress": True,
                "message": "Recording started. Use stop_recording tool to stop recording before the specified length."
            }
        except Exception as e:
            # Make sure to disarm track if there's an error
            try:
                track = reapy.Track.from_id(track_id)
                track.armed = False
            except:
                pass
                
            return {
                "success": False,
                "error": str(e)
            }
    
    def stop_recording(self):
        """
        Stop the current recording.
        
        Returns:
            dict: Result of the operation
        """
        try:
            # Stop recording
            RPR.Main_OnCommand(1016, 0)  # Transport: Stop
            
            # Get the last recorded item
            project = reapy.Project()
            
            return {
                "success": True,
                "message": "Recording stopped"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def edit_audio_item(self, item_id, start_trim=None, end_trim=None, fade_in=None, fade_out=None):
        """
        Edit the specified audio item.
        
        Args:
            item_id (int): Item ID
            start_trim (float): Seconds to trim from start
            end_trim (float): Seconds to trim from end
            fade_in (float): Fade in length in seconds
            fade_out (float): Fade out length in seconds
            
        Returns:
            dict: Result of the operation
        """
        try:
            # Get item by ID
            item = reapy.Item.from_id(item_id)
            
            # Apply edits
            original_length = item.length
            original_position = item.position
            
            # Trim start
            if start_trim is not None and start_trim > 0:
                if start_trim < item.length:
                    item.position += start_trim
                    item.length -= start_trim
                    
                    # Adjust take offset
                    take = item.active_take
                    take.start_offset += start_trim
            
            # Trim end
            if end_trim is not None and end_trim > 0:
                if end_trim < item.length:
                    item.length -= end_trim
            
            # Set fade in
            if fade_in is not None:
                item.fade_in_length = fade_in
            
            # Set fade out
            if fade_out is not None:
                item.fade_out_length = fade_out
            
            return {
                "success": True,
                "item_id": item_id,
                "original_position": original_position,
                "original_length": original_length,
                "new_position": item.position,
                "new_length": item.length,
                "fade_in": item.fade_in_length,
                "fade_out": item.fade_out_length
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def adjust_item_pitch(self, item_id, semitones):
        """
        Adjust the pitch of an audio item.
        
        Args:
            item_id (int): Item ID
            semitones (float): Semitones to adjust pitch
            
        Returns:
            dict: Result of the operation
        """
        try:
            # Get item by ID
            item = reapy.Item.from_id(item_id)
            take = item.active_take
            
            # Set pitch adjustment
            take.pitch = semitones
            
            return {
                "success": True,
                "item_id": item_id,
                "pitch_adjustment": take.pitch
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def adjust_item_playback_rate(self, item_id, rate):
        """
        Adjust the playback rate of an audio item.
        
        Args:
            item_id (int): Item ID
            rate (float): Playback rate (1.0 = normal)
            
        Returns:
            dict: Result of the operation
        """
        try:
            # Get item by ID
            item = reapy.Item.from_id(item_id)
            take = item.active_take
            
            # Set playback rate
            take.playback_rate = rate
            
            return {
                "success": True,
                "item_id": item_id,
                "playback_rate": take.playback_rate
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
