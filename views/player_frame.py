import tkinter as tk
from tkinter import ttk

LABEL_FONT = ('Times', 14, 'bold')
MINOR_FONT = ('Times', 11)

class PlayerFrame(ttk.Frame):

    def __init__(self, parent, controller=None, header=False, entry=False):
        super().__init__(master=parent)
        self.parent = parent
        self.controller = controller
        self.header = header
        self.entry = entry
        self.style = ttk.Style()
        self.style.configure('player.TFrame', background='black')
        self.configure(style='player.TFrame')

        self.create_widgets()
        
    def create_widgets(self):
        if self.header or self.entry:
            self.pixel = tk.PhotoImage(master=self.parent.master, width=1, height=1)
        else:
            self.pixel = tk.PhotoImage(master=self.parent.master.master.master, width=1, height=1)

        if self.header:
            self.player = tk.Label(self, text='Player', anchor=tk.CENTER, width=127,
                                   image=self.pixel, font=LABEL_FONT, compound='center')
            self.mosley_open_hc = tk.Label(self, text='Mosley Open Handicap', anchor=tk.CENTER,
                                           width=205, image=self.pixel, font=LABEL_FONT, compound='center')
            self.twisted_creek_hc = tk.Label(self, text='Twisted Creek Handicap', anchor=tk.CENTER,
                                             width=225, image=self.pixel, font=LABEL_FONT, compound='center')
            self.active = tk.Label(self, text='Active', anchor=tk.CENTER, width=60, image=self.pixel,
                                   font=LABEL_FONT, compound='center')
        elif self.entry:
            self.player = tk.Entry(self, width=21)
            self.mosley_open_hc = tk.Entry(self, width=35)
            self.twisted_creek_hc = tk.Entry(self, width=38)
            self.active = tk.Label(self, width=60, image=self.pixel)
        else:
            self.active_state = tk.BooleanVar(self)
            self.player = tk.Label(self, anchor=tk.CENTER, width=127, image=self.pixel,
                                   font=MINOR_FONT, compound='center')
            self.mosley_open_hc = tk.Label(self, anchor=tk.CENTER, width=205, image=self.pixel,
                                           font=MINOR_FONT, compound='center')
            self.twisted_creek_hc = tk.Label(self, anchor=tk.CENTER, width=225, image=self.pixel,
                                             font=MINOR_FONT, compound='center')
            self.active = ttk.Checkbutton(self, onvalue=True, offvalue=False, command=self.activate_player,
                                          variable=self.active_state, width=7)
            
        self.player.grid(row=0, column=0, sticky='nsew', padx=(1, 1), pady=(1, 1))
        self.mosley_open_hc.grid(row=0, column=1, sticky='nsew', padx=(1, 1), pady=(1, 1))
        self.twisted_creek_hc.grid(row=0, column=2, sticky='nsew', padx=(1, 1), pady=(1, 1))
        self.active.grid(row=0, column=3, sticky='nsew', padx=(1, 1), pady=(1, 1))
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def activate_player(self):
        player_name = self.player.cget("text")
        self.controller.activate_player(player_name, self.active_state.get())
            
        


