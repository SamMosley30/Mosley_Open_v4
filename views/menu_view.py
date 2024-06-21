"""This file contains the MenuView class and its associated functions."""

import tkinter as tk
from tkinter import ttk

PAGE_NAME_STR = 'Menu'
WELCOME_STR = 'Welcome to the Mosley Open'
MAJOR_LABEL_FONT = ('Times New Roman', 14, 'bold')
MINOR_LABEL_FONT = ('Times New Roman', 12, 'bold')
FILL_HORIZONTAL = 'ew'
FILL_VERTICAL = 'ns'
FILL_FRAME = 'nsew'

class MenuView(ttk.Frame):
    """View for displaying page options and navigation."""

    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=0, sticky=FILL_FRAME)
        self.columnconfigure(0, weight=1)

        # Create and layout widgets
        self.create_widgets()
    
    def create_widgets(self):
        """Create and layout the widgets contained in the Menu."""

        # Create a label at the top of the window with the page name.
        page_name_label = ttk.Label(self, text=WELCOME_STR, font=MAJOR_LABEL_FONT,
                                    anchor=tk.CENTER)
        page_name_label.grid(row=0, column=0, columnspan=1, sticky=FILL_HORIZONTAL)

        # Divide Page Name Label from other widgets
        divider = ttk.Separator(master=self, orient='horizontal')
        divider.grid(row=1, column=0, columnspan=1, sticky=FILL_HORIZONTAL)

        # Create all frame buttons.
        self.course_list_btn = ttk.Button(self, text='Course List')
        self.course_list_btn.grid(row=3, column=0, columnspan=1, sticky=FILL_HORIZONTAL,
                                  padx=(150, 150), pady=(60, 5))
        self.player_list_btn = ttk.Button(self, text='Player List')
        self.player_list_btn.grid(row=4, column=0, columnspan=1, sticky=FILL_HORIZONTAL,
                                  padx=(150, 150), pady=(0, 5))
        self.score_page_btn = ttk.Button(self, text='Score Entry')
        self.score_page_btn.grid(row=5, column=0, columnspan=1, sticky=FILL_HORIZONTAL,
                                  padx=(150, 150), pady=(0,5))
        self.leaderboard_btn = ttk.Button(self, text='Generate Leaderboard')
        self.leaderboard_btn.grid(row=6, column=0, columnspan=1, sticky=FILL_HORIZONTAL,
                                  padx=(150, 150), pady=(0,5))

    def set_controller(self, controller):
        """Set the controller and configure button commands."""
        self.controller = controller
        self.course_list_btn.configure(command=controller.show_course_list)
        self.player_list_btn.configure(command=controller.show_player_list)
        self.score_page_btn.configure(command=controller.show_score_page)
        self.leaderboard_btn.configure(command=controller.generate_leaderboard)