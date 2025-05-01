import os
from pathlib import Path

import reapy
from reapy import reascript_api as RPR


class FXTools:
    """Tools for managing VST instruments and effects in REAPER."""
    
    def __init__(self, config):
        """
        Initialize FXTools with configuration.
        
        Args:
            config (dict): Configuration dictionary
        """
        self.config = config
        self.vst_directories = config.get("vst_directories", [])
    
    def add_vst_instrument(self, track_id, vst_name):
        """
        Add a VST instrument to the specified track.
        
        Args:
            track_id (int): Track ID
            vst_name (str): VST instrument name
            
        Returns:
            dict: FX information
        """
        try:
            # Get track by ID
            track = reapy.Track.from_id(track_id)
            
            # Add VST instrument
            fx_index = track.add_fx(vst_name)
            
            if fx_index < 0:
                return {
                    "success": False,
                    "error": f"VST instrument not found: {vst_name}"
                }
            
            # Get the FX
            fx = track.fxs[fx_index]
            
            # Configure track for MIDI input
            track.input_mode = reapy.InputMode.ALL_MIDI
            
            return {
                "success": True,
                "fx_id": fx.id,
                "index": fx_index,
                "name": fx.name,
                "track_id": track_id,
                "preset": fx.preset_name
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def add_vst_effect(self, track_id, vst_name):
        """
        Add a VST effect to the specified track.
        
        Args:
            track_id (int): Track ID
            vst_name (str): VST effect name
            
        Returns:
            dict: FX information
        """
        try:
            # Get track by ID
            track = reapy.Track.from_id(track_id)
            
            # Add VST effect
            fx_index = track.add_fx(vst_name)
            
            if fx_index < 0:
                return {
                    "success": False,
                    "error": f"VST effect not found: {vst_name}"
                }
            
            # Get the FX
            fx = track.fxs[fx_index]
            
            return {
                "success": True,
                "fx_id": fx.id,
                "index": fx_index,
                "name": fx.name,
                "track_id": track_id,
                "preset": fx.preset_name
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def set_vst_parameter(self, track_id, fx_id, param_index, value):
        """
        Set a parameter value for the specified VST.
        
        Args:
            track_id (int): Track ID
            fx_id (int): FX ID
            param_index (int): Parameter index
            value (float): Parameter value (normalized 0.0-1.0)
            
        Returns:
            dict: Result of the operation
        """
        try:
            # Get track by ID
            track = reapy.Track.from_id(track_id)
            
            # Find FX by ID
            fx = None
            for i in range(track.n_fxs):
                current_fx = track.fxs[i]
                if current_fx.id == fx_id:
                    fx = current_fx
                    break
            
            if fx is None:
                return {
                    "success": False,
                    "error": f"FX with ID {fx_id} not found on track {track_id}"
                }
            
            # Set parameter value
            fx.params[param_index].normalized_value = value
            
            # Get parameter name
            param_name = fx.params[param_index].name
            
            return {
                "success": True,
                "fx_id": fx_id,
                "param_index": param_index,
                "param_name": param_name,
                "value": value,
                "track_id": track_id
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_fx_parameters(self, track_id, fx_id):
        """
        Get all parameters for the specified FX.
        
        Args:
            track_id (int): Track ID
            fx_id (int): FX ID
            
        Returns:
            dict: FX parameters
        """
        try:
            # Get track by ID
            track = reapy.Track.from_id(track_id)
            
            # Find FX by ID
            fx = None
            for i in range(track.n_fxs):
                current_fx = track.fxs[i]
                if current_fx.id == fx_id:
                    fx = current_fx
                    break
            
            if fx is None:
                return {
                    "success": False,
                    "error": f"FX with ID {fx_id} not found on track {track_id}"
                }
            
            # Get parameters
            params = []
            for i in range(fx.n_params):
                param = fx.params[i]
                params.append({
                    "index": i,
                    "name": param.name,
                    "value": param.normalized_value,
                    "formatted_value": param.formatted_value
                })
            
            return {
                "success": True,
                "fx_id": fx_id,
                "name": fx.name,
                "track_id": track_id,
                "preset": fx.preset_name,
                "parameters": params
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def load_fx_preset(self, track_id, fx_id, preset_name):
        """
        Load a preset for the specified FX.
        
        Args:
            track_id (int): Track ID
            fx_id (int): FX ID
            preset_name (str): Preset name
            
        Returns:
            dict: Result of the operation
        """
        try:
            # Get track by ID
            track = reapy.Track.from_id(track_id)
            
            # Find FX by ID
            fx = None
            for i in range(track.n_fxs):
                current_fx = track.fxs[i]
                if current_fx.id == fx_id:
                    fx = current_fx
                    break
            
            if fx is None:
                return {
                    "success": False,
                    "error": f"FX with ID {fx_id} not found on track {track_id}"
                }
            
            # Load preset
            fx.preset_name = preset_name
            
            return {
                "success": True,
                "fx_id": fx_id,
                "name": fx.name,
                "track_id": track_id,
                "preset": fx.preset_name
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def list_available_vsts(self, vst_type="all"):
        """
        List all available VSTs of the specified type.
        
        Args:
            vst_type (str): VST type (all, instrument, effect)
            
        Returns:
            dict: List of available VSTs
        """
        try:
            # Use REAPER's built-in function to get VST list
            # This is a simplified implementation - in practice, you'd need to parse
            # REAPER's FX browser or use a more complex approach
            
            # For now, return some common VSTs as an example
            common_instruments = [
                "ReaSynth",
                "ReaSamplOmatic5000",
                "VSTi: Surge XT (Surge Synth Team)",
                "VSTi: Vital (Vital)",
                "VSTi: TAL-NoiseMaker (Togu Audio Line)"
            ]
            
            common_effects = [
                "ReaEQ",
                "ReaComp",
                "ReaDelay",
                "ReaVerb",
                "VST: FabFilter Pro-Q 3 (FabFilter)",
                "VST: Valhalla VintageVerb (Valhalla DSP)",
                "VST: Soundtoys EchoBoy (Soundtoys)"
            ]
            
            if vst_type.lower() == "instrument":
                vsts = common_instruments
            elif vst_type.lower() == "effect":
                vsts = common_effects
            else:
                vsts = common_instruments + common_effects
            
            return {
                "success": True,
                "vst_type": vst_type,
                "vsts": vsts
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
