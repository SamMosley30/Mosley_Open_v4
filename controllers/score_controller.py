"""This file contains the ScoreController class and its associated functions."""

import os
import yaml

from views.score_view import ScoreView
from views.menu_view import MenuView
from models.active_player_list import ActivePlayerList
from models.day import Day
from models.calcutta_team import CalcuttaTeam
from models.active_player import ActiveTournament

COURSE_LENGTH = 18
CALCUTTA_TEAM_PATH = '\\Users\\sammo\Mosley_Open_v4\\active_data_lib\\calcutta_teams'

class ScoreController:
    """Controller for interfacing with ActivePlayer models and ScoreView"""

    def __init__(self, application, model: ActivePlayerList, view: ScoreView):
        self.application = application
        self.player_list_model = model
        self.calcutta_team_list = self.load_calcutta_teams()
        self.view = view
        self.view.set_controller(self)
        self.populate_course_box()
        self.set_up_player_list()
        self.populate_player_data()

    def open_menu(self):
        """Return to the menu page."""
        self.application.show_frame(MenuView)

    def get_player(self, player_name):
        """Get the ActivePlayer model by player name."""
        return self.player_list_model.active_player_list[player_name]
    
    def get_player_names(self):
        """Get a list of all active player names."""
        return list(self.player_list_model.active_player_list.keys())
    
    def get_score_list(self, player_frame):
        """Get the score list for the input player on the input day."""
        try:
            score_list = [int(score.get()) for score in list(player_frame.score_entry_dict.values())]
        except ValueError:
            raise ValueError(f"Please input valid scores for {player_frame.name_label.cget('text')}")
        
        if len(score_list) != COURSE_LENGTH:
            raise ValueError(f"Invalid score list length for {player_frame.name_label.cget('text')}")
        
        return score_list

    def set_up_player_list(self):
        """This function will construct and fill the frames of the ActivePlayerLists."""
        for frame in self.view.active_player_list_frames.values():
            frame.generate_active_player_frames(self.get_player_names())
    
    def populate_course_box(self):
        """This function loads in the course names to the Course ComboBox."""
        course_names = self.application.course_list_controller.get_course_names()
        self.view.set_courses(course_names)
    
    def load_course(self, event):
        """Loads the course currently selected in the combobox."""
        course_name = self.view.course_box.get()
        self.current_course_model = self.application.course_list_controller.get_course(course_name)

    def populate_player_data(self):
        """Populate the player data into the ActivePlayerView frames."""
        for day, player_list_frame in self.view.active_player_list_frames.items():
            for player_name, player_frame in player_list_frame.active_player_frames.items():
                player_model = self.get_player(player_name)
                day_info = player_model.days[day]
                player_frame.name_label.configure(text=player_model.player_info.name)
                mosley_open_hc = player_model.player_info.mosley_open_handicap
                twisted_creek_hc = player_model.player_info.twisted_creek_handicap
                player_frame.hc_label.configure(text=f'{mosley_open_hc}/{twisted_creek_hc}')
                if day_info:
                    player_frame.set_score_data(day_info.raw_score_list, day_info.total_raw_score)

    def calculate_scores(self):
        """This function calls functions to calculate score information and then save it to
        each player."""
        self.save_score_data()
        if self.view.current_day == 'Day 1':
            self.calcutta_team_list = self.generate_calcutta_teams()
        elif self.view.current_day == 'Day 2':
            player_list = list(self.player_list_model.active_player_list.values())
            sorted_player_list = sorted(player_list, key=lambda player: (player.net_mosley_open_points, player.total_raw_score), reverse=True)
            cutline_score = self.view.request_cut_line(sorted_player_list)
            self.split_players(cutline_score)

        if self.calcutta_team_list is None:
            self.calcutta_team_list = self.load_calcutta_teams()
        
        for team in self.calcutta_team_list.values():
            self.update_calcutta_scores(team)

    def generate_calcutta_teams(self):
        player_list = list(self.player_list_model.active_player_list.values())
        ranked_players = sorted(player_list, key=lambda player: (player.get_twisted_creek_daily_points(self.view.current_day), player.days[self.view.current_day].points), reverse=True)
        if len(ranked_players) % 2 != 0:
            double_player_name = self.view.request_double_player(ranked_players)
            player_idx = [i for i, player in enumerate(ranked_players) if player.player_info.name == double_player_name]
            ranked_players.insert(player_idx[0], ranked_players[player_idx[0]])

        teams = [
            [ranked_players[i].player_info.name, ranked_players[-1 - i].player_info.name]
            for i in range(len(ranked_players))
            if i < 0.5 * len(ranked_players)
        ]
        calcutta_teams = [CalcuttaTeam(team[0], team[1]) for team in teams]
        for team in calcutta_teams:
            team.save()
        
        return calcutta_teams

    def load_calcutta_teams(self):
        calcutta_dict = dict()
        for filename in os.listdir(CALCUTTA_TEAM_PATH):
            if not filename.endswith('yaml'):
                continue

            filepath = os.path.join(CALCUTTA_TEAM_PATH, filename)
            with open(filepath, 'r') as file:
                calcutta_team = yaml.load(file, Loader=yaml.Loader)

            if not isinstance(calcutta_team, CalcuttaTeam):
                raise TypeError(f"Invalid CalcuttaTeam file.")
            
            calcutta_dict[f'{calcutta_team.player_1} and {calcutta_team.player_2}'] = calcutta_team
        return calcutta_dict

    def update_calcutta_scores(self, team):
        player_1 = self.get_player(team.player_1)
        player_2 = self.get_player(team.player_2)
        day = self.view.current_day
        player_1_scores, player_1_modifiers = player_1.days[day].get_calcutta_scores(player_1.player_info.twisted_creek_handicap)
        player_2_scores, player_2_modifiers = player_2.days[day].get_calcutta_scores(player_2.player_info.twisted_creek_handicap)
        team.calculate_scores(player_1_scores, player_1_modifiers, player_2_scores, player_2_modifiers, day)
        team.save()

    def split_players(self, cutline_score):
        """This function will assign single tournament values to each player based on the cutline."""
        for player in self.player_list_model.active_player_list.values():
            if player.net_mosley_open_points >= cutline_score:
                player.active_tournament = ActiveTournament.MosleyOpen
            else:
                player.active_tournament = ActiveTournament.TwistedCreek

            player.save()

    def save_score_data(self):
        """This function saves all of the data found in the entry boxes and course box to
        each player's ActivePlayer object file."""
        active_player_list_frame = self.view.active_player_list_frames[self.view.current_day]
        for player_name, player_frame in active_player_list_frame.active_player_frames.items():
            player_model = self.get_player(player_name)
            try:
                player_model.days[self.view.current_day] = Day(self.current_course_model, self.get_score_list(player_frame))
            except AttributeError:
                raise ValueError("Please select a course before calculating scores.")
            player_model.save()
            player_frame.total_score_label.config(text=str(player_model.days[self.view.current_day].total_raw_score))

    def refresh_player_list(self, player_list_model):
        """Destroys and recreates the player list in the event that a new player is activated/deactivated."""
        self.player_list_model.refresh_player_list(player_list_model)
        for frame in self.view.active_player_list_frames.values():
            frame.destroy_active_player_frames
        self.set_up_player_list()
        self.populate_player_data()
        