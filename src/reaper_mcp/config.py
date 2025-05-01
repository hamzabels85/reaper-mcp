import json
import os
from pathlib import Path


DEFAULT_CONFIG = {
    "reaper_path": "",
    "default_project_directory": str(Path.home() / "Documents" / "REAPER Projects"),
    "vst_directories": [],
    "sample_libraries": [],
    "default_tempo": 120.0,
    "default_time_signature": "4/4",
    "default_sample_rate": 44100,
    "default_bit_depth": 24,
    "default_audio_format": "wav",
    "mastering_presets": {
        "default": [
            {"name": "ReaEQ", "params": {}},
            {"name": "ReaComp", "params": {"threshold": -18.0, "ratio": 2.0}},
            {"name": "ReaLimit", "params": {"threshold": -0.5, "release": 50.0}}
        ],
        "loud": [
            {"name": "ReaEQ", "params": {}},
            {"name": "ReaComp", "params": {"threshold": -20.0, "ratio": 4.0}},
            {"name": "ReaComp", "params": {"threshold": -12.0, "ratio": 2.0}},
            {"name": "ReaLimit", "params": {"threshold": -0.1, "release": 30.0}}
        ],
        "gentle": [
            {"name": "ReaEQ", "params": {}},
            {"name": "ReaComp", "params": {"threshold": -16.0, "ratio": 1.5}},
            {"name": "ReaLimit", "params": {"threshold": -1.0, "release": 100.0}}
        ]
    }
}


def load_config(config_path):
    """
    Load configuration from a JSON file.
    If the file doesn't exist, create it with default values.
    
    Args:
        config_path (str): Path to the configuration file
        
    Returns:
        dict: Configuration dictionary
    """
    config_path = Path(config_path)
    
    # If config file doesn't exist, create it with default values
    if not config_path.exists():
        os.makedirs(config_path.parent, exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        return DEFAULT_CONFIG
    
    # Load config from file
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Update with any missing default values
        for key, value in DEFAULT_CONFIG.items():
            if key not in config:
                config[key] = value
        
        return config
    except Exception as e:
        print(f"Error loading configuration: {e}")
        print("Using default configuration")
        return DEFAULT_CONFIG


def save_config(config, config_path):
    """
    Save configuration to a JSON file.
    
    Args:
        config (dict): Configuration dictionary
        config_path (str): Path to the configuration file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        config_path = Path(config_path)
        os.makedirs(config_path.parent, exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving configuration: {e}")
        return False
