"""This file contains the Course View Class and the associated functions needed for creating,
saving, and loading a course."""

import tkinter as tk
from tkinter import ttk

PAGE_NAME_STR = 'Edit Courses'
MAJOR_LABEL_FONT = ('Times New Roman', 14, 'bold')
MINOR_LABEL_FONT = ('Times New Roman', 12, 'bold')
ENTRY_FONT = ('Times New Roman', 11)
FILL_HORIZONTAL = 'ew'
FILL_VERTICAL = 'ns'
FILL_FRAME = 'nsew'
LABEL_PADDING = (15, 17)
ENTRY_PADDING = (1, 1)
COURSE_LENGTH = 18

class CourseView(tk.Toplevel):
    """View for displaying and interacting with a single Course model."""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        # Create a label at the top of window with the page name.
        page_name_label = ttk.Label(self, text=PAGE_NAME_STR, font=MAJOR_LABEL_FONT, anchor=tk.CENTER)
        page_name_label.grid(row=0, column=0, columnspan=3, sticky=FILL_HORIZONTAL)

        # Divide Page Name Label from entry boxes.
        divider = ttk.Separator(master=self, orient='horizontal')
        divider.grid(row=1, column=0, columnspan=3, sticky=FILL_HORIZONTAL)

        self.course_entry_frame = CourseEntryFrame(self, self.controller)
        self.course_entry_frame.grid(row=2, column=0, columnspan=3, sticky=FILL_HORIZONTAL)
        
        self.save_course_btn = ttk.Button(self, text='Save Course', command=self.controller.save_course)
        self.save_course_btn.grid(row=3, column=0, columnspan=1, sticky=FILL_HORIZONTAL)

        self.delete_course_btn = ttk.Button(self, text='Delete Course', command=self.controller.delete_course)
        self.delete_course_btn.grid(row=3, column=1, columnspan=1, sticky=FILL_HORIZONTAL)

        # Create a dropdown menu to select a course to load.
        self.course_box = ttk.Combobox(self, state='readonly')
        self.course_box.grid(row=3, column=2, columnspan=1, sticky=FILL_HORIZONTAL)
        self.course_box.bind("<<ComboboxSelected>>", self.controller.load_course)

    def set_courses(self, course_names):
        """Populate the combobox with course names."""
        self.course_box['values'] = course_names

    def get_course_name(self):
        """Get the entered course name."""
        course_name = self.course_entry_frame.entry_course_name.get()
        if not course_name:
            return None
        
        return course_name
    
    def get_par_order(self):
        """Get the par order from entries"""
        par_entry_dict = self.course_entry_frame.par_entry_dict
        try:
            par_order = [int(par_entry_dict[f'Hole {i+1}'].get()) for i in range(COURSE_LENGTH)]
        except ValueError:
            return None
        
        return par_order
    
    def get_handicap_order(self):
        """Get the handicap order from entries"""
        hc_entry_dict = self.course_entry_frame.hc_entry_dict
        try:
            hc_order = [int(hc_entry_dict[f'Hole {i+1}'].get()) for i in range(COURSE_LENGTH)]
        except ValueError:
            return None
        
        return hc_order
    
    def set_course_data(self, course):
        """Set the course data into the entry fields."""
        self.course_entry_frame.entry_course_name.delete(0, tk.END)
        
        for i in range(COURSE_LENGTH):
            self.course_entry_frame.par_entry_dict[f'Hole {i+1}'].delete(0, tk.END)
            self.course_entry_frame.hc_entry_dict[f'Hole {i+1}'].delete(0, tk.END)

        if course:
            self.course_entry_frame.entry_course_name.insert(0, course.name)
        
            for i in range(COURSE_LENGTH):
                self.course_entry_frame.par_entry_dict[f'Hole {i+1}'].insert(0, course.par_order[i])
                self.course_entry_frame.hc_entry_dict[f'Hole {i+1}'].insert(0, course.handicap_order[i])


class CourseEntryFrame(ttk.Frame):
    """Frame containing all of the course data entry fields."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Construct Course Name entry box
        self.entry_course_name = ttk.Entry(self, font=ENTRY_FONT)
        self.entry_course_name.grid(row=0, column=0, rowspan=3, sticky=FILL_FRAME)

        # Construct Par/HC label boxes
        par_label = ttk.Label(self, text='Par', font=MINOR_LABEL_FONT, anchor=tk.CENTER)
        par_label.grid(row=0, column=1, padx=LABEL_PADDING)
        handicap_label = ttk.Label(self, text='HC', font=MINOR_LABEL_FONT, anchor=tk.CENTER)
        handicap_label.grid(row=2, column=1, padx=LABEL_PADDING)
        
        # Construct dictionary of Par/HC entries
        self.par_entry_dict = dict()
        self.hc_entry_dict = dict()
        for i in range(COURSE_LENGTH):
            entry_par = ttk.Entry(self, width=2)
            entry_par.grid(row=0, column=i+2, sticky=FILL_FRAME, padx=ENTRY_PADDING)
            entry_hc = ttk.Entry(self, width=2)
            entry_hc.grid(row=2, column=i+2, sticky=FILL_FRAME, padx=ENTRY_PADDING)

            dict_key = f"Hole {i+1}"
            self.par_entry_dict[dict_key] = entry_par
            self.hc_entry_dict[dict_key] = entry_hc
