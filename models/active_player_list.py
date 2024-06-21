"""This file contains the ActivePlayerList class and all of its related functions."""

import os
import yaml

from .active_player import ActivePlayer
from .player import Player
from .player_list import PlayerList

PLAYER_LIB_PATH = '\\Users\\sammo\Mosley_Open_v4\\playerlib'
DATA_LIB_PATH = '\\Users\\sammo\Mosley_Open_v4\\active_data_lib\\active_players'

class ActivePlayerList:

    def __init__(self, player_list_model: PlayerList):
        self.active_player_list = self._load_player_list(player_list_model)

    def _load_player_list(self, player_list_model):

        player_dict = dict()
        for player_name, player in player_list_model.player_list.items():
            active_player_path = os.path.join(DATA_LIB_PATH, f'{player_name}_active.yaml')
            active_player_model = None
            try:
                with open(active_player_path, 'r') as file:
                    active_player_model = yaml.load(file, Loader=yaml.Loader)
                
                if not player.active:
                    active_player_model.delete()
                    active_player_model = None
                elif active_player_model.player_info.__dict__ != player.__dict__:
                    active_player_model.delete()
                    active_player_model = ActivePlayer(player)
                    active_player_model.save()
            except FileNotFoundError:
                if player.active:
                    active_player_model = ActivePlayer(player)
                    active_player_model.save()

            if active_player_model:
                player_dict[active_player_model.player_info.name] = active_player_model

        return player_dict

    def destroy_player_list(self):
        """Remove all active player objects from the active data library."""
        for active_player_model in self.active_player_list.values():
            active_player_model.delete()
    
    def refresh_player_list(self, player_list_model):
        """Refresh the active player list model to get updated/new data."""
        self.destroy_player_list()
        self.active_player_list = self._load_player_list(player_list_model)