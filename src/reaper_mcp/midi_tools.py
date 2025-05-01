import reapy
from reapy import reascript_api as RPR


class MidiTools:
    """Tools for MIDI composition and editing in REAPER."""
    
    def __init__(self, config):
        """
        Initialize MidiTools with configuration.
        
        Args:
            config (dict): Configuration dictionary
        """
        self.config = config
        
        # Define standard MIDI note mappings for drum patterns
        self.drum_mappings = {
            "kick": 36,      # C1
            "snare": 38,     # D1
            "hihat_closed": 42,  # F#1
            "hihat_open": 46,    # A#1
            "tom_low": 41,   # F1
            "tom_mid": 45,   # A1
            "tom_high": 48,  # C2
            "crash": 49,     # C#2
            "ride": 51       # D#2
        }
        
        # Define chord mappings
        self.chord_types = {
            "maj": [0, 4, 7],
            "min": [0, 3, 7],
            "dim": [0, 3, 6],
            "aug": [0, 4, 8],
            "maj7": [0, 4, 7, 11],
            "min7": [0, 3, 7, 10],
            "dom7": [0, 4, 7, 10],
            "dim7": [0, 3, 6, 9],
            "hdim7": [0, 3, 6, 10],
            "sus2": [0, 2, 7],
            "sus4": [0, 5, 7]
        }
        
        # Note name to MIDI note number mapping
        self.note_to_number = {
            "C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
            "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
            "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11
        }
    
    def create_midi_item(self, track_id, start_position, length):
        """
        Create a new MIDI item on the specified track.
        
        Args:
            track_id (int): Track ID
            start_position (float): Start position in seconds
            length (float): Length in seconds
            
        Returns:
            dict: MIDI item information
        """
        try:
            # Get track by ID
            track = reapy.Track.from_id(track_id)
            
            # Create new MIDI item
            item = track.add_midi_item(start_position, start_position + length)
            
            # Get the MIDI take
            take = item.active_take
            
            return {
                "success": True,
                "item_id": item.id,
                "take_id": take.id,
                "position": item.position,
                "length": item.length,
                "track_id": track_id
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def add_midi_note(self, item_id, pitch, start, length, velocity=100):
        """
        Add a MIDI note to the specified MIDI item.
        
        Args:
            item_id (int): MIDI item ID
            pitch (int): MIDI note number (0-127)
            start (float): Start position in seconds relative to item start
            length (float): Note length in seconds
            velocity (int): Note velocity (1-127)
            
        Returns:
            dict: Result of the operation
        """
        try:
            # Get item by ID
            item = reapy.Item.from_id(item_id)
            
            # Get the active take
            take = item.active_take
            
            # Ensure take is MIDI
            if not take.is_midi:
                return {
                    "success": False,
                    "error": "Take is not MIDI"
                }
            
            # Add MIDI note
            # Note: start is relative to item start
            take.add_note(
                start=start,
                end=start + length,
                pitch=pitch,
                velocity=velocity,
                channel=0  # Default MIDI channel
            )
            
            return {
                "success": True,
                "item_id": item_id,
                "pitch": pitch,
                "start": start,
                "length": length,
                "velocity": velocity
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _parse_chord(self, chord_str):
        """
        Parse a chord string into MIDI note numbers.
        
        Args:
            chord_str (str): Chord string (e.g., "C", "Dm", "G7")
            
        Returns:
            list: List of MIDI note numbers relative to root
        """
        # Extract root note and chord type
        if len(chord_str) == 1:
            root = chord_str
            chord_type = "maj"
        elif len(chord_str) >= 2:
            if chord_str[1] in ["#", "b"]:
                root = chord_str[0:2]
                chord_type = chord_str[2:] or "maj"
            else:
                root = chord_str[0]
                chord_type = chord_str[1:] or "maj"
        
        # Map chord type to intervals
        if chord_type == "m":
            chord_type = "min"
        elif chord_type == "7":
            chord_type = "dom7"
        
        # Get intervals for chord type
        intervals = self.chord_types.get(chord_type, self.chord_types["maj"])
        
        # Get root note number
        root_num = self.note_to_number.get(root, 0)
        
        # Return intervals (will be transposed in the calling function)
        return intervals, root_num
    
    def create_chord_progression(self, track_id, chords, start_position, beats_per_chord=4):
        """
        Create a chord progression on the specified track.
        
        Args:
            track_id (int): Track ID
            chords (str): Comma-separated list of chords (e.g., "C,G,Am,F")
            start_position (float): Start position in seconds
            beats_per_chord (int): Number of beats per chord
            
        Returns:
            dict: Result of the operation
        """
        try:
            # Get project and track
            project = reapy.Project()
            track = reapy.Track.from_id(track_id)
            
            # Parse chord list
            chord_list = [c.strip() for c in chords.split(",")]
            
            # Calculate seconds per beat
            seconds_per_beat = 60.0 / project.bpm
            chord_length = seconds_per_beat * beats_per_chord
            
            # Create MIDI item for the entire progression
            total_length = chord_length * len(chord_list)
            item = track.add_midi_item(start_position, start_position + total_length)
            take = item.active_take
            
            # Add chords
            added_chords = []
            for i, chord_str in enumerate(chord_list):
                try:
                    # Parse chord
                    intervals, root_num = self._parse_chord(chord_str)
                    
                    # Calculate position within item
                    chord_start = i * chord_length
                    
                    # Add chord notes (in middle C octave)
                    for interval in intervals:
                        note_num = 60 + root_num + interval  # Middle C (60) + root + interval
                        take.add_note(
                            start=chord_start,
                            end=chord_start + chord_length * 0.95,  # Slightly shorter than full length
                            pitch=note_num,
                            velocity=80,
                            channel=0
                        )
                    
                    added_chords.append({
                        "chord": chord_str,
                        "position": chord_start,
                        "length": chord_length
                    })
                except Exception as e:
                    # Continue with next chord if one fails
                    print(f"Error adding chord {chord_str}: {e}")
            
            return {
                "success": True,
                "item_id": item.id,
                "chords": added_chords,
                "start_position": start_position,
                "total_length": total_length
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_drum_pattern(self, track_id, pattern, start_position, beats=4, repeats=1):
        """
        Create a drum pattern on the specified track.
        
        Args:
            track_id (int): Track ID
            pattern (str): Drum pattern string (e.g., "k...k...s...k.s.")
                k=kick, s=snare, h=hihat_closed, o=hihat_open, 
                t=tom_low, m=tom_mid, f=tom_high, c=crash, r=ride
            start_position (float): Start position in seconds
            beats (int): Number of beats in the pattern
            repeats (int): Number of times to repeat the pattern
            
        Returns:
            dict: Result of the operation
        """
        try:
            # Get project and track
            project = reapy.Project()
            track = reapy.Track.from_id(track_id)
            
            # Calculate timing
            seconds_per_beat = 60.0 / project.bpm
            pattern_length = seconds_per_beat * beats
            total_length = pattern_length * repeats
            
            # Create MIDI item
            item = track.add_midi_item(start_position, start_position + total_length)
            take = item.active_take
            
            # Map pattern characters to drum notes
            char_to_drum = {
                "k": "kick",
                "s": "snare",
                "h": "hihat_closed",
                "o": "hihat_open",
                "t": "tom_low",
                "m": "tom_mid",
                "f": "tom_high",
                "c": "crash",
                "r": "ride"
            }
            
            # Calculate time per character
            time_per_char = pattern_length / len(pattern)
            
            # Add notes for each repeat
            for repeat in range(repeats):
                offset = repeat * pattern_length
                
                for i, char in enumerate(pattern):
                    if char in char_to_drum:
                        drum_name = char_to_drum[char]
                        note_num = self.drum_mappings[drum_name]
                        
                        # Position within the pattern
                        note_start = offset + (i * time_per_char)
                        
                        # Add note (short duration for drums)
                        take.add_note(
                            start=note_start,
                            end=note_start + (time_per_char * 0.5),
                            pitch=note_num,
                            velocity=100,
                            channel=9  # Standard MIDI drum channel
                        )
            
            return {
                "success": True,
                "item_id": item.id,
                "pattern": pattern,
                "repeats": repeats,
                "start_position": start_position,
                "total_length": total_length
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
