"""This file contains the CourseList model class and the associated functions needed
for handling it."""

import os
import yaml

from .observable_model import ObservableModel
from .course import Course

COURSE_LIB_PATH = '\\Users\\sammo\Mosley_Open_v4\\courselib'

class CourseList(ObservableModel):
    """Model for maintaining and processing a list of all courses within the course library."""

    def __init__(self):
        self.course_list = self._load_course_library()

    def _load_course_library(self):
        course_dict = dict()
        for filename in os.listdir(COURSE_LIB_PATH):

            if not filename.endswith('.yaml'):
                continue

            filepath = os.path.join(COURSE_LIB_PATH, filename)
            with open(filepath, 'r') as file:
                course_model = yaml.load(file, Loader=yaml.Loader)

            if not isinstance(course_model, Course):
                raise TypeError(f"Invalid Course File at {filepath}.")
            
            course_dict[course_model.name] = course_model

        return course_dict
    
    def refresh_course_list(self):
        """Refresh the course list model to get updated/new data then trigger an event."""
        self.course_list = self._load_course_library()

