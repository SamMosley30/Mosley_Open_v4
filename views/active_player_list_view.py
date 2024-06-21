"""This file contains the ActivePlayerListView classa and the associated functions."""

import tkinter as tk
from tkinter import ttk

from .active_player_view import ActivePlayerView

FILL_FRAME = 'nsew'
FRAME_PADDING = (2, 2)

class ActivePlayerListView(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.active_player_frames = dict()

    def generate_active_player_frames(self, player_names):
        """Create and layout the ActivePlayerView frames."""
        self.destroy_active_player_frames()
        for i, player_name in enumerate(player_names):
            active_player_frame = ActivePlayerView(self)
            active_player_frame.grid(row=i, column=0, sticky=FILL_FRAME, pady=FRAME_PADDING)
            self.active_player_frames[player_name] = active_player_frame

    def destroy_active_player_frames(self):
        """Destroy existing player frames and reset the dictionary."""
        if self.active_player_frames:
            for player_frame in self.active_player_frames.values():
                player_frame.destroy()

        self.active_player_frames = dict()
        