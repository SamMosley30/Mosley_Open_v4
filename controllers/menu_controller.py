"""This file contains the MenuController class and its associated functions."""

from views.menu_view import MenuView
from views.course_list_view import CourseListView
from views.player_list_view import PlayerListView
from views.score_view import ScoreView
from models.leaderboard import Leaderboard

class MenuController:
    """Controller for menu used to navigate scorekeeping application."""

    def __init__(self, application, view: MenuView):
        self.application = application
        self.view = view
        self.view.set_controller(self)

    def show_course_list(self):
        """Display the CourseListView frame of the application."""
        self.application.show_frame(CourseListView)

    def show_player_list(self):
        """Display the PlayerListView frame of the application."""
        self.application.show_frame(PlayerListView)

    def show_score_page(self):
        """Display the ScoreView frame of the application."""
        self.application.show_frame(ScoreView)

    def generate_leaderboard(self):
        """Generate a leaderboard of the current results."""
        Leaderboard(
            self.application.score_controller.player_list_model, 
            self.application.score_controller.calcutta_team_list
            )
