"""This file contains the ActivePlayer class and all of its related functions."""

import yaml
from enum import Enum
from os import path, remove

from .player import Player
from .day import Day

DATA_LIB_DIR = 'active_data_lib'

class ActiveTournament(Enum):
    MosleyOpen = 1
    TwistedCreek = 2
    BothTournaments = 3

class ActivePlayer:

    def __init__(self, player: Player, active_tournament: ActiveTournament=ActiveTournament.BothTournaments):
        self.player_info = self._validate_inputs(player, Player)
        self.active_tournament = self._validate_inputs(active_tournament, ActiveTournament)
        self.days = {
            'Day 1': None,
            'Day 2': None,
            'Day 3': None,
            }
        self.save_path = path.abspath(f'{DATA_LIB_DIR}/active_players/{self.player_info.name}_active.yaml')

    def _validate_inputs(self, input, input_class):
        if not isinstance(input, input_class):
            raise TypeError(f"Input {input} must be of Type {input_class}.")
        return input
    
    @property
    def number_of_days_played(self):
        """A property used to get the total number of days played."""
        return len(list(filter(None, self.days.values())))
    
    @property
    def total_raw_score(self):
        """A property used to calculate the total raw score of a player."""
        return sum([day.total_raw_score for day in self.days.values() if isinstance(day, Day)])

    @property
    def net_mosley_open_points(self):
        """A property used to calculate a player's points with their Mosley Open handicap applied."""

        return sum([day.get_net_points(self.player_info.mosley_open_handicap) 
                    for day in self.days.values() if isinstance(day, Day)])
    
    @property
    def net_twisted_creek_score(self):
        """A property used to calculate a player's score with their Twisted Creek Handicap applied."""

        return sum([day.get_net_points(self.player_info.twisted_creek_handicap) 
                    for day in self.days.values() if isinstance(day, Day)])
    
    def get_twisted_creek_daily_points(self, day):
        return self.days[day].get_net_points(self.player_info.twisted_creek_handicap)
    
    def save(self):
        """Save the ActivePlayer object to the data library as a YAML file."""

        try:
            with open(self.save_path, 'w') as player_file:
                yaml.dump(self, player_file)
        except Exception as e:
            raise IOError(f"Failed to save player: {e}")
        
    def delete(self):
        """Delete the player file from the data library."""
        try:
            if path.exists(self.save_path):
                remove(self.save_path)
            else:
                raise FileNotFoundError(f"ActivePlayer file {self.save_path} does not exist.")
        except Exception as e:
            raise IOError(f"Failed to delete player: {e}")