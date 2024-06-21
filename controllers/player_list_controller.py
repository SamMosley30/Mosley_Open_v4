"""This file contains the PlayerListController class and the associated functions needed for
interfacing with the PlayerList View and PlayerList Model as well as child controllers."""

from views.menu_view import MenuView
from models.player import Player

import tkinter as tk

COURSE_LENGTH = 18

class PlayerListController:
    """Controller for interfacing with the PlayerList view and PlayerList Model."""

    def __init__(self, application, model, view):
        self.application = application
        self.model = model
        self.view = view
        self.view.set_controller(self)
        self.view.generate_player_frames(self.get_player_names())
        self.populate_player_data()

    def open_menu(self):
        """Return to the menu page."""
        self.application.show_frame(MenuView)

    def populate_player_data(self):
        """Populate the player data into the PlayerFrames."""
        for player_name, player_frame in self.view.player_frames.items():
            player_model = self.get_player(player_name)
            player_frame.player.config(text=player_name)
            player_frame.mosley_open_hc.config(text=player_model.mosley_open_handicap)
            player_frame.twisted_creek_hc.config(text=player_model.twisted_creek_handicap)
            player_frame.active_state.set(value=player_model.active)

    def get_player(self, player_name):
        """Get the player model by player name."""
        return self.model.player_list[player_name]
    
    def get_player_names(self):
        """Get a list of all player names."""
        return list(self.model.player_list.keys())
    
    def activate_player(self, player_name, active_state):
        player = self.get_player(player_name)
        player.active = active_state
        player.save()
        self.update_player_list()
        self.application.score_controller.refresh_player_list(self.model)
    
    def update_player_list(self):
        """Update the player list view with the latest data."""
        self.model.refresh_player_list()
        self.view.destroy_player_frames()
        self.view.generate_player_frames(self.get_player_names())
        self.populate_player_data()

    def validate_handicaps(self, mosley_open_hc_str, twisted_creek_hc_str):
        """Validate that the input handicap information is formatted correctly."""
        if ((not mosley_open_hc_str and twisted_creek_hc_str) or 
            (mosley_open_hc_str and not twisted_creek_hc_str)):
            raise ValueError("Both handicaps are required.")
        try:
            mosley_open_hc = int(mosley_open_hc_str)
            twisted_creek_hc = int(twisted_creek_hc_str)
        except ValueError:
            raise TypeError("Handicaps must be integers.")
        return mosley_open_hc, twisted_creek_hc
    
    def update_player(self):
        """Adds a new player, or edits/deletes an exiting one in the library based on
        information in the entry boxes."""
        player_name = self.view.player_entry_frame.player.get()
        mosley_open_hc_str = self.view.player_entry_frame.mosley_open_hc.get()
        twisted_creek_hc_str = self.view.player_entry_frame.twisted_creek_hc.get()
        delete_player = False

        # Check that a player name was provided
        if not player_name:
            raise ValueError("No player name provided.")

        if not (mosley_open_hc_str or twisted_creek_hc_str):
            self.delete_player(player_name)
        else:
            mosley_open_hc, twisted_creek_hc = self.validate_handicaps(mosley_open_hc_str, twisted_creek_hc_str)
            if player_name in self.get_player_names():
                player = self.get_player(player_name)
                player.mosley_open_handicap = min(20, mosley_open_hc)
                player.twisted_creek_handicap = min(30, twisted_creek_hc)
                player.save()
            else:
                player = Player(player_name, twisted_creek_hc)
                player.save()
        
        self.update_player_list()
        self.clear_entry_fields()

    def delete_player(self, player_name):
        """Deletes a player from the library and player list."""
        try:
            player=self.get_player(player_name)
            player.delete()
        except KeyError:
            raise ValueError(f"Attempted to delete {player_name}, but could not find them.")

    def clear_entry_fields(self):
        """Clears the entry fields in the view."""
        self.view.player_entry_frame.player.delete(0, tk.END)
        self.view.player_entry_frame.mosley_open_hc.delete(0, tk.END)
        self.view.player_entry_frame.twisted_creek_hc.delete(0, tk.END)

