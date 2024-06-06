"""This file contains the Course class and the associated functions needed for creating,
saving, and loading a course."""

import yaml
from os import path, remove

from .observable_model import ObservableModel

COURSE_LENGTH = 18
COURSE_DIR = 'courselib'

class Course(ObservableModel):
    """This class contains all of the information specific to a course, and the functions
    needed for saving the course to the course library."""

    def __init__(self, course_name: str, course_par: list, course_handicap: list):
        super().__init__()
        
        self._validate_course_name(course_name)
        self._validate_course_length(course_par, 'par')
        self._validate_course_length(course_handicap, 'handicap')
        
        self.name = course_name
        self.par_order = course_par
        self.handicap_order = course_handicap
        self.save_path = path.abspath(f'courselib/{self.name}.yaml')

    def _validate_course_name(self, course_name):
        if not isinstance(course_name, str):
            raise ValueError("Course name must be a string.")
        if not course_name:
            raise ValueError("Course name cannot be empty.")
        
    def _validate_course_length(self, course_data, data_type):
        if not course_data:
            raise ValueError(f"Course {data_type} must be defined.")
        if len(course_data) != COURSE_LENGTH:
            msg = f"Course {data_type} length must be {COURSE_LENGTH}, got {len(course_data)}."
            raise ValueError(msg)
        if not all([isinstance(hole, int) for hole in course_data]):
            msg = f"Course {data_type} must contain only int type values."

    def save(self):
        """Save the Course object to the course library as a YAML file."""

        try:
            with open(self.save_path, 'w') as course_file:
                yaml.dump(self, course_file)
            self.trigger_event('save')
        except Exception as e:
            raise IOError(f"Failed to save course: {e}")


    def delete(self):
        """Delete the course file from the course library"""
        try:
            if path.exists(self.save_path):
                remove(self.save_path)
                self.trigger_event('delete')
            else:
                raise FileNotFoundError(f"Course file {self.save_path} does not exist.")
        except Exception as e:
            raise IOError(f"Failed to delete course: {e}")
        
