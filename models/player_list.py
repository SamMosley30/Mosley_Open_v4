"""This file contains the PlayerList model class and the associated functions needed
for handling it."""

import os
import yaml

from .observable_model import ObservableModel
from .player import Player

PLAYER_LIB_PATH = '\\Users\\sammo\Mosley_Open_v4\\playerlib'

class PlayerList(ObservableModel):
    """Model for maintaining and processing a list of all players within the player library."""

    def __init__(self):
        self.player_list = self._load_player_library()

    def _load_player_library(self):
        player_dict = dict()
        for filename in os.listdir(PLAYER_LIB_PATH):

            if not filename.endswith('.yaml'):
                continue

            filepath = os.path.join(PLAYER_LIB_PATH, filename)
            with open(filepath, 'r') as file:
                player_model = yaml.load(file, Loader=yaml.Loader)

            if not isinstance(player_model, Player):
                raise TypeError(f"Invalid Player File at {filepath}.")
            
            player_dict[player_model.name] = player_model

        return player_dict
    
    def refresh_player_list(self):
        """Refresh the player list model to get updated/new data then trigger an event."""
        self.player_list = self._load_player_library()
