"""This file contains the MenuController class and its associated functions."""

from views.menu_view import MenuView
from views.course_list_view import CourseListView

class MenuController:
    """Controller for menu used to navigate scorekeeping application."""

    def __init__(self, application, view: MenuView):
        self.application = application
        self.view = view
        self.view.set_controller(self)

    def show_course_list(self):
        """Display the CourseListView frame of the application."""
        self.application.show_frame(CourseListView)