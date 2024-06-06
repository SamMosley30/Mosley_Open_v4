"""This file contains the Course Controller class and the associated functions needed for interacting
with the Course model and Course View, as well as interfacing with the parent controller."""

import sys

from views.course_view import CourseView
from models.course import Course

class CourseController:
    """Controller for Course operations."""

    def __init__(self, course_list_controller):
        self.course_list_controller = course_list_controller
        self.model = None
        self.view = CourseView(self)
        self.view.bind('<Destroy>', self.course_list_controller.delete_course_editor)
        self.update_course_list()

    def save_course(self):

        if not self.model:
            course_name = self.view.get_course_name()
            par_order = self.view.get_par_order()
            handicap_order = self.view.get_handicap_order()
            if not course_name:
                return
            if not par_order:
                return
            if not handicap_order:
                return
            self.model = Course(course_name, par_order, handicap_order)
        else:
            self.model.name = self.view.get_course_name()
            self.model.par_order = self.view.get_par_order()
            self.model.handicap_order = self.view.get_handicap_order()

        self.model.save()
        self.course_list_controller.update_course_list()
        self.model = None
        self.view.set_course_data(self.model)

    def delete_course(self):
        
        if not self.model:
            return
        
        self.model.delete()
        self.course_list_controller.update_course_list()
        self.model = None

    def load_course(self, event):
        course_name = self.view.course_box.get()
        self.model = self.course_list_controller.get_course(course_name)
        self.view.set_course_data(self.model)

    def update_course_list(self):
        course_names = self.course_list_controller.get_course_names()
        self.view.set_courses(course_names)

