"""This file contains the Player class and all of its related functions."""

import yaml
from os import path, remove

from .observable_model import ObservableModel

PLAYER_LIB_DIR = 'playerlib'

class Player(ObservableModel):
    """An object to represent all of the data and logic unique to a player."""

    def __init__(self, player_name: str, handicap: int):

        self._validate_name(player_name)
        self._validate_handicap(handicap)

        self.name = player_name
        self.save_path = path.abspath(f'{PLAYER_LIB_DIR}/{self.name}.yaml')
        self._generate_handicaps(handicap)
        self.active = False
            
    def _validate_name(self, player_name):
        if not isinstance(player_name, str):
            raise TypeError("Player name must be a string.")
        
        if not player_name:
            raise ValueError("Player name must not be empty.")
        
    def _validate_handicap(self, handicap):
        if not isinstance(handicap, int):
            raise TypeError("Handicap must be an integer.")
        
        if handicap < 0 or handicap > 30:
            raise ValueError("Handicap {handicap} must be between 0 and 30.")
        
    def _generate_handicaps(self, handicap):
        """Calculate the handicaps for the individual tournaments."""
        
        # The twisted creek handicap can range from 0-30
        self.twisted_creek_handicap = handicap
        
        # The Mosley Open handicap is restricted to 0-20
        self.mosley_open_handicap = min(20, handicap)

    def save(self):
        """Save the Player object to the player library as a YAML file."""

        try:
            with open(self.save_path, 'w') as player_file:
                yaml.dump(self, player_file)
        except Exception as e:
            raise IOError(f"Failed to save player: {e}")
        
    def delete(self):
        """Delete the player file from the course library."""
        try:
            if path.exists(self.save_path):
                remove(self.save_path)
            else:
                raise FileNotFoundError(f"Player file {self.save_path} does not exist.")
        except Exception as e:
            raise IOError(f"Failed to delete player: {e}")
