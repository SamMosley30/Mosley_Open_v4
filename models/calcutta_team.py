"""This file contains the CalcuttaTeam class and all of its related functions."""

import yaml
from os import path, remove
from numpy import array

DATA_LIB_DIR = 'active_data_lib'
COURSE_LENGTH = 18

class CalcuttaTeam:

    def __init__(self, player_1: str, player_2: str):
        self.player_1 = player_1
        self.player_2 = player_2
        self.days = {
            'Day 1': None,
            'Day 2': None,
            'Day 3': None
        }
        self.save_path = path.abspath(f'{DATA_LIB_DIR}/calcutta_teams/{self.player_1}_{self.player_2}.yaml')

    @property
    def total_points(self):
        return sum(list(self.days.values()))
    
    def calculate_scores(self, player_1_scores, player_1_modifiers, player_2_scores, player_2_modifiers, day):
        if day not in self.days:
            raise KeyError(f"Invalid day string.")
        
        team_score_list = [min(player_1_scores[i], player_2_scores[i]) for i in range(COURSE_LENGTH)]
        point_list = -1*array(team_score_list)+2
        self.days[day] = int(sum(point_list)+player_1_modifiers+player_2_modifiers)-36
    
    def save(self):
        try:
            with open(self.save_path, 'w') as calcutta_file:
                yaml.dump(self, calcutta_file)
        except Exception as e:
            raise IOError(f"Failed to save player: {e}")
        
    def delete(self):
        try:
            if path.exists(self.save_path):
                remove(self.save_path)
            else:
                raise FileNotFoundError(f"CalcuttaTeam file {self.save_path} does not exist.")
        except Exception as e:
            raise IOError(f"Failed to delete plaeyrs: {e}")
        
