"""This file contains the Player List View Class and the associated functions needed for
displaying the course list page."""

import tkinter as tk
from tkinter import ttk

from .player_frame import PlayerFrame

PAGE_NAME_STR = 'Player Library'
MAJOR_LABEL_FONT = ('Times New Roman', 14, 'bold')
MINOR_LABEL_FONT = ('Times New Roman', 12, 'bold')
ENTRY_FONT = ('Times New Roman', 11)
FILL_HORIZONTAL = 'ew'
FILL_VERTICAL = 'ns'
FILL_FRAME = 'nsew'
LABEL_PADDING = (15, 17)
ENTRY_PADDING = (1, 1)
COURSE_LENGTH = 18

class PlayerListView(ttk.Frame):
    """View for displaying and interacting with the Player Library."""

    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=0, sticky=FILL_FRAME)
        self.columnconfigure(0, weight=1)

        # Create and layout widgets
        self.create_widgets()
        self.player_frames = {}
    
    def create_widgets(self):
        """Create and layout the widgets"""

        # Create a label at the top of window with the page name.
        page_name_label = ttk.Label(self, text=PAGE_NAME_STR, font=MAJOR_LABEL_FONT, anchor=tk.CENTER)
        page_name_label.grid(row=0, column=0, columnspan=3, sticky=FILL_HORIZONTAL)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)

        # Divide Page Name Label from player list.
        divider = ttk.Separator(master=self, orient='horizontal')
        divider.grid(row=1, column=0, columnspan=3, sticky=FILL_HORIZONTAL)
        
        # Create the table header
        header_frame = PlayerFrame(self, header=True)
        header_frame.grid(row=2, column=0, columnspan=2, sticky=FILL_HORIZONTAL)

        # Create canvas to hold list of players.
        self.canvas = tk.Canvas(self, height=515)
        self.canvas.grid(row=3, column=0, columnspan=2, sticky=FILL_FRAME)
        self.canvas.grid_columnconfigure(0, weight=1)
        self.canvas.grid_rowconfigure(0, weight=1)
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        # Create a scrollbar in case player list goes out of bounds
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.grid(row=3, column=2, rowspan=1, sticky=FILL_FRAME)
        scrollbar.grid_columnconfigure(0, weight=1)
        scrollbar.grid_rowconfigure(0, weight=1)

        self.player_list_frame = ttk.Frame(self.canvas)
        self.player_list_frame.grid_columnconfigure(0, weight=1)
        self.player_list_frame.grid_rowconfigure(0, weight=1)
        self.player_list_frame.configure(height=1000)
        self.canvas.create_window((0,0), window=self.player_list_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.player_list_frame.bind('<Configure>', self.on_frame_configure)

        self.player_entry_frame = PlayerFrame(self, entry=True)
        self.player_entry_frame.grid(row=4, column=0, columnspan=2, sticky=FILL_HORIZONTAL)

        self.update_players_btn = ttk.Button(self, text='Update Players')
        self.update_players_btn.grid(row=5, column=0, columnspan=3, sticky=FILL_HORIZONTAL)

        self.return_btn = ttk.Button(self, text="Return")
        self.return_btn.grid(row=6, column=0, columnspan=3, sticky=FILL_HORIZONTAL)

    def on_frame_configure(self, event):
        """Update the scroll region of the canvas."""
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def on_mouse_wheel(self, event):
        """Scroll the canvas on mouse wheel event."""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def set_controller(self, controller):
        """Set the controller and configure button commands."""
        self.controller = controller
        self.update_players_btn.configure(command=self.controller.update_player)
        self.return_btn.configure(command=self.controller.open_menu)

    def generate_player_frames(self, player_names):
        """Generate the PlayerFrames for each player."""

        # Ensure that existing frames are destroyed before regenerating.
        self.destroy_player_frames()
        for i, player_name in enumerate(player_names):
            player_frame = PlayerFrame(self.player_list_frame, controller=self.controller)
            player_frame.grid(row=i, column=0, columnspan=1, sticky=FILL_HORIZONTAL)
            player_frame.grid_columnconfigure(0, weight=1)
            player_frame.grid_rowconfigure(i, weight=1)
            self.player_frames[player_name] = player_frame
        
    def destroy_player_frames(self):
        """Destroy existing player frames and reset player_frames dictionary."""
        
        if self.player_frames:
            for player_frame in self.player_frames.values():
                player_frame.destroy()

        self.player_frames = {}
