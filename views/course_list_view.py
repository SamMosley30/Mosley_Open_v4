"""This file contains the Course List View Class and the associated functions needed for
displaying the course list page."""

import tkinter as tk
from tkinter import ttk

PAGE_NAME_STR = 'Course Library'
MAJOR_LABEL_FONT = ('Times New Roman', 14, 'bold')
MINOR_LABEL_FONT = ('Times New Roman', 12, 'bold')
ENTRY_FONT = ('Times New Roman', 11)
FILL_HORIZONTAL = 'ew'
FILL_VERTICAL = 'ns'
FILL_FRAME = 'nsew'
LABEL_PADDING = (15, 17)
ENTRY_PADDING = (1, 1)
COURSE_LENGTH = 18

class CourseListView(ttk.Frame):
    """View for displaying and interacting with the Course Library."""

    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=0, sticky=FILL_FRAME)
        self.columnconfigure(0, weight=1)

        # Create and layout widgets
        self.create_widgets()
        self.course_frames = {}
    
    def create_widgets(self):
        """Create and layout the widgets"""

        # Create a label at the top of window with the page name.
        page_name_label = ttk.Label(self, text=PAGE_NAME_STR, font=MAJOR_LABEL_FONT, anchor=tk.CENTER)
        page_name_label.grid(row=0, column=0, columnspan=3, sticky=FILL_HORIZONTAL)

        # Divide Page Name Label from course list.
        divider = ttk.Separator(master=self, orient='horizontal')
        divider.grid(row=1, column=0, columnspan=3, sticky=FILL_HORIZONTAL)

        # Create canvas to hold list of courses.
        self.canvas = tk.Canvas(self, height=515)
        self.canvas.grid(row=2, column=0, columnspan=2, sticky=FILL_FRAME)
        self.canvas.grid_columnconfigure(0, weight=1)
        self.canvas.grid_rowconfigure(0, weight=1)

        # Create a scrollbar in case course list goes out of bounds
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.grid(row=2, column=2, rowspan=1, sticky=FILL_FRAME)
        scrollbar.grid_columnconfigure(0, weight=1)
        scrollbar.grid_rowconfigure(0, weight=1)

        self.course_list_frame = ttk.Frame(self.canvas)
        self.course_list_frame.grid_columnconfigure(0, weight=1)
        self.course_list_frame.grid_rowconfigure(0, weight=1)
        self.course_list_frame.configure(height=1000)
        self.canvas.create_window((0,0), window=self.course_list_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.course_list_frame.bind('<Configure>', self.on_frame_configure)

        self.edit_course_btn = ttk.Button(self, text='Edit Courses')
        self.edit_course_btn.grid(row=3, column=0, sticky=FILL_FRAME)

        self.return_btn = ttk.Button(self, text="Return")
        self.return_btn.grid(row=4, column=0, sticky=FILL_FRAME)

    def on_frame_configure(self, event):
        """Update the scroll region of the canvas."""
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def set_controller(self, controller):
        """Set the controller and configure button commands."""
        self.controller = controller
        self.edit_course_btn.configure(command=self.controller.open_course_editor)
        self.return_btn.configure(command=self.controller.open_menu)

    def generate_course_frames(self, course_names):
        """Generate the CourseInfoFrames for each course."""

        # Ensure that existing frames are destroyed before regenerating.
        self.destroy_course_frames()
        for i, course_name in enumerate(course_names):
            course_frame = CourseInfoFrame(self.course_list_frame)
            course_frame.grid(row=i, column=0, columnspan=3, sticky=FILL_HORIZONTAL)
            course_frame.columnconfigure(0, minsize=157)
            self.course_frames[course_name] = course_frame
        
    def destroy_course_frames(self):
        """Destroy existing course frames and reset course_frames dictionary."""
        
        if self.course_frames:
            for course_frame in self.course_frames.values():
                course_frame.destroy()

        self.course_frames = {}


class CourseInfoFrame(ttk.Frame):
    """A frame organizing all of the course data into a single card."""
    def __init__(self, parent):
        super().__init__(parent)

        self.course_name_label = ttk.Label(self, text='', font=MAJOR_LABEL_FONT, anchor=tk.CENTER)
        self.course_name_label.grid(row=0, column=0, rowspan=3, sticky=FILL_FRAME)

        course_vert_divider1 = ttk.Separator(self, orient='vertical')
        course_vert_divider1.grid(row=0, column=1, rowspan=3, sticky=FILL_VERTICAL)

        # Construct Par/HC label boxes
        par_label = ttk.Label(self, text='Par', font=MINOR_LABEL_FONT, anchor=tk.CENTER)
        par_label.grid(row=0, column=2, padx=LABEL_PADDING)
        handicap_label = ttk.Label(self, text='HC', font=MINOR_LABEL_FONT, anchor=tk.CENTER)
        handicap_label.grid(row=2, column=2, padx=LABEL_PADDING)

        course_vert_divider2 = ttk.Separator(self, orient='vertical')
        course_vert_divider2.grid(row=0, column=3, rowspan=3, sticky=FILL_VERTICAL)

        self.par_dict = dict()
        self.hc_dict = dict()
        for i in range(COURSE_LENGTH):
            self.columnconfigure(2*i+4, minsize=22)
            par_hole_label = ttk.Label(self, text='', anchor=tk.CENTER)
            par_hole_label.grid(row=0, column=2*i+4, sticky=FILL_FRAME)
            self.par_dict[f'Hole {i+1}'] = par_hole_label

            handicap_hole_label = ttk.Label(self, text='', anchor=tk.CENTER)
            handicap_hole_label.grid(row=2, column=2*i+4, sticky=FILL_FRAME)
            self.hc_dict[f'Hole {i+1}'] = handicap_hole_label

            hole_divider = ttk.Separator(self, orient='vertical')
            hole_divider.grid(row=0, column=2*i+5, rowspan=3, sticky=FILL_VERTICAL)

        course_column, _ = self.grid_size()
        course_vert_divider3 = ttk.Separator(self, orient='vertical')
        course_vert_divider3.grid(row=0, column=course_column-1, rowspan=3, sticky='ns')

        course_horiz_divider1 = ttk.Separator(self, orient='horizontal')
        course_horiz_divider1.grid(row=1, column=2, columnspan=course_column-2, sticky='ew')

        course_horiz_divider2 = ttk.Separator(self, orient='horizontal')
        course_horiz_divider2.grid(row=3, column=0, columnspan=course_column, sticky='ew')
