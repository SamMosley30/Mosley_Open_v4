"""This file contains the ActivePlayerView class and its associated functions."""

import tkinter as tk
from tkinter import ttk

LABEL_FONT = ('Times', 12, 'bold')
LABEL_PADDING = (1, 1)
ENTRY_PADDING = (2, 2)
FILL_FRAME = 'nsew'
COURSE_LENGTH = 18

class ActivePlayerView(ttk.Frame):
    """This class defines the ActivePlayerView frame which holds all of the elements needed to
    set the hole by hole scores for a player."""

    def __init__(self, parent):
        super().__init__(parent)
        self.style = ttk.Style()
        self.style.configure('player.TLabel', background='black')
        self.create_widgets()

    def create_widgets(self):
        self.name_label = ttk.Label(self, font=LABEL_FONT, width=15, borderwidth=1,
                                    relief='solid')
        self.name_label.grid(row = 0, column = 0, sticky=FILL_FRAME, padx=LABEL_PADDING)

        self.hc_label = ttk.Label(self, font=LABEL_FONT, width=6, borderwidth=1, relief='solid')
        self.hc_label.grid(row=0, column=1, sticky=FILL_FRAME, padx=LABEL_PADDING)

        self.score_entry_dict = dict()
        for i in range(COURSE_LENGTH):
            score_entry = ttk.Entry(self, width=2)
            score_entry.grid(row=0, column=i+2, sticky=FILL_FRAME, padx=ENTRY_PADDING)
            self.score_entry_dict[f"Hole {i+1}"] = score_entry

        self.total_score_label = ttk.Label(self, font=LABEL_FONT)
        self.total_score_label.grid(row=0, column=20, padx=LABEL_PADDING, sticky=FILL_FRAME)

    def set_score_data(self, raw_scores: list, total_score: int):
        """Populate the entries."""

        for i in range(COURSE_LENGTH):
            self.score_entry_dict[f'Hole {i+1}'].delete(0, tk.END)

        if len(raw_scores) == COURSE_LENGTH:
            for i in range(COURSE_LENGTH):
                self.score_entry_dict[f'Hole {i+1}'].insert(0, raw_scores[i])
        
        if total_score:
            self.total_score_label.config(text=total_score)
