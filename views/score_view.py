"""This file contains the ScoreView class and its associated functions."""

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

from .active_player_list_view import ActivePlayerListView

PAGE_NAME_STR = "Score Page"
MAJOR_LABEL_FONT = ('Times', 14, 'bold')
FILL_FRAME = 'nsew'
FILL_HORIZONTAL = 'ew'

class ScoreView(ttk.Frame):

    DAYS = ['Day 1', 'Day 2', 'Day 3']
    
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=0, sticky=FILL_FRAME)
        self.columnconfigure(0, weight=1)

        # Create and layout widgets
        self.create_widgets()

    def create_widgets(self):
        """Create and layout the widgets."""

        # Create a label at the top of window with the page name.
        page_name_label = ttk.Label(self, text=PAGE_NAME_STR, font=MAJOR_LABEL_FONT, anchor=tk.CENTER)
        page_name_label.grid(row=0, column=0, columnspan=2)

        # Divide page name label from rest of data.
        divider = ttk.Separator(self, orient='horizontal')
        divider.grid(row=1, column=0, columnspan=2, sticky=FILL_HORIZONTAL)

        # Create a course list 
        self.course_box = ttk.Combobox(self, state='readonly')
        self.course_box.grid(row=2, column=0, columnspan=1, sticky=FILL_HORIZONTAL)

        # Create a notebook to hold the tabs for each day of the tournament.
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=3, column=0, columnspan=2, sticky=FILL_FRAME)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)

        self.active_player_list_frames = dict()
        for day in self.DAYS:
            active_player_list_frame = ActivePlayerListView(self.notebook)
            self.notebook.add(active_player_list_frame, text=day)
            self.active_player_list_frames[day] = active_player_list_frame

        self.notebook.select(0)
        self.current_day = 'Day 1'

        self.calculate_btn = ttk.Button(self, text='Calculate Scores')
        self.calculate_btn.grid(row=4, column=0, sticky=FILL_FRAME)

        self.return_btn = ttk.Button(self, text="Return")
        self.return_btn.grid(row=4, column=1, sticky=FILL_FRAME)

    def on_tab_selected(self, event):
        self.current_day = self.notebook.tab(self.notebook.select(), "text")

    def set_courses(self, course_names):
        """Populate the course names in the combobox."""
        self.course_box['values'] = course_names

    def set_controller(self, controller):
        """Set the controller and configure button commands."""
        self.controller = controller
        self.calculate_btn.configure(command=self.controller.calculate_scores)
        self.return_btn.configure(command=self.controller.open_menu)
        self.course_box.bind("<<ComboboxSelected>>", self.controller.load_course)

    def request_cut_line(self, player_list):
        """This function generates a window for requesting a cut line from the user."""
        split_request = SplitRequest(player_list)
        self.controller.application.wait_window(split_request)

        return split_request.cutline.get()
    
    def request_double_player(self, player_list):
        double_partner = DoublePartnerRequest(player_list)
        self.controller.application.wait_window(double_partner)
        
        return double_partner.double_player.get()
    
class DoublePartnerRequest(tk.Toplevel):
    """This class holds the window for a Double Partner request in the event that there are an odd number
    of participants, and one player needs to be given two teams in the Calcutta."""
    def __init__(self, players):

        super().__init__()

        self.title('Partner Request')
        container = ttk.LabelFrame(master=self, text='Choose the player with two partners')
        container.pack()
        self.players = players
        self.double_player = tk.StringVar(self)

        for i, player in enumerate(self.players):
            button = ttk.Radiobutton(
                container,
                text=player.player_info.name,
                value=player.player_info.name,
                variable=self.double_player
            )
            button.grid(column=0, row=i, sticky='nsew')

    
class SplitRequest(tk.Toplevel):
    """This class holds the window for a Tournament Split request after the second day. The user will select
    the player that marks the cut line, and all players with worse scores will be locked into the Twisted Creek
    while players with better or equivalent scores will be locked into the Mosley Open."""

    def __init__(self, player_list):

        super().__init__()

        self.title('Tournament Split')
        self.player_list = player_list
        container = ttk.LabelFrame(master=self, text='Choose the last person to make the cut')
        container.pack()
        self.cutline = tk.IntVar(self)
        self.cutline.set(-999)

        for i, player in enumerate(self.player_list):
            net_score = player.net_mosley_open_points
            button = ttk.Radiobutton(
                container,
                text=f'{player.player_info.name:<15s} {str(net_score):<3s}',
                value=net_score,
                variable=self.cutline
            )
            button.grid(column=0, row=i, sticky='nsew')