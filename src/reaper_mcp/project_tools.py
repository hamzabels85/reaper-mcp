import os
from pathlib import Path
import time

import reapy
from reapy import reascript_api as RPR


class ProjectTools:
    """Tools for managing REAPER projects."""
    
    def __init__(self, config):
        """
        Initialize ProjectTools with configuration.
        
        Args:
            config (dict): Configuration dictionary
        """
        self.config = config
        self.default_project_dir = Path(config["default_project_directory"])
        
        # Create default project directory if it doesn't exist
        os.makedirs(self.default_project_dir, exist_ok=True)
    
    def create_new_project(self, tempo=None, time_signature=None, name=None):
        """
        Create a new REAPER project with specified parameters.
        
        Args:
            tempo (float, optional): Project tempo in BPM
            time_signature (str, optional): Time signature (e.g., "4/4")
            name (str, optional): Project name
            
        Returns:
            dict: Project information
        """
        try:
            # Use default values from config if not specified
            tempo = tempo or self.config["default_tempo"]
            time_signature = time_signature or self.config["default_time_signature"]
            name = name or f"New Project {time.strftime('%Y-%m-%d %H-%M-%S')}"
            
            # Create new project
            RPR.Main_OnCommand(41929, 0)  # New project command
            
            # Get project
            project = reapy.Project()
            
            # Set project parameters
            project.bpm = tempo
            
            # Set time signature
            if time_signature:
                num, denom = map(int, time_signature.split('/'))
                project.time_signature = (num, denom)
            
            # Return project info
            return {
                "success": True,
                "project_id": project.id,
                "name": name,
                "tempo": project.bpm,
                "time_signature": f"{project.time_signature[0]}/{project.time_signature[1]}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def save_project(self, project_path=""):
        """
        Save the current project to the specified path.
        
        Args:
            project_path (str, optional): Path to save the project
            
        Returns:
            dict: Result of the save operation
        """
        try:
            project = reapy.Project()
            
            # If no path specified, use default directory with project name
            if not project_path:
                project_name = project.name or f"Project {time.strftime('%Y-%m-%d %H-%M-%S')}"
                project_path = os.path.join(self.default_project_dir, f"{project_name}.rpp")
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(os.path.abspath(project_path)), exist_ok=True)
            
            # Save project
            project.save(project_path)
            
            return {
                "success": True,
                "project_path": project_path
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def load_project(self, project_path):
        """
        Load a REAPER project from the specified path.
        
        Args:
            project_path (str): Path to the project file
            
        Returns:
            dict: Result of the load operation
        """
        try:
            # Check if file exists
            if not os.path.exists(project_path):
                return {
                    "success": False,
                    "error": f"Project file not found: {project_path}"
                }
            
            # Load project
            RPR.Main_openProject(project_path)
            
            # Get project info
            project = reapy.Project()
            
            return {
                "success": True,
                "project_id": project.id,
                "name": project.name,
                "tempo": project.bpm,
                "time_signature": f"{project.time_signature[0]}/{project.time_signature[1]}",
                "project_path": project_path
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_project_info(self):
        """
        Get information about the current project.
        
        Returns:
            dict: Project information
        """
        try:
            project = reapy.Project()
            
            # Get track count
            track_count = project.n_tracks
            
            # Get project length
            length = project.length
            
            # Get markers
            markers = []
            for i in range(project.n_markers):
                marker = project.get_marker(i)
                markers.append({
                    "index": i,
                    "name": marker.name,
                    "position": marker.position
                })
            
            # Get regions
            regions = []
            for i in range(project.n_regions):
                region = project.get_region(i)
                regions.append({
                    "index": i,
                    "name": region.name,
                    "start": region.start,
                    "end": region.end
                })
            
            return {
                "success": True,
                "name": project.name,
                "path": project.path,
                "tempo": project.bpm,
                "time_signature": f"{project.time_signature[0]}/{project.time_signature[1]}",
                "length": length,
                "track_count": track_count,
                "markers": markers,
                "regions": regions
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
