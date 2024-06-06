"""This file contains the CourseListController class and the associated functions needed for
interfacing with the CourseList View and CourseList Model as well as child controllers."""

from .course_controller import CourseController
from views.menu_view import MenuView

COURSE_LENGTH = 18

class CourseListController:
    """Controller for interfacing with the CourseList view and CourseList Model, as
    well as creating, interfacing with, and destroying CourseControllers for editing
    courses."""

    def __init__(self, application, model, view):
        self.application = application
        self.model = model
        self.view = view
        self.view.set_controller(self)
        self.view.generate_course_frames(self.get_course_names())
        self.populate_course_data()

    def open_course_editor(self):
        """Open the course editor."""
        self.course_controller = CourseController(self)

    def delete_course_editor(self, event):
        """Delete the course editor."""
        self.course_controller = None

    def open_menu(self):
        """Return to the menu page."""
        self.application.show_frame(MenuView)

    def populate_course_data(self):
        """Populate the course data into the CourseInfoFrames."""
        for course_name in self.view.course_frames:
            course_model = self.get_course(course_name)
            course_frame = self.view.course_frames[course_name]

            course_frame.course_name_label.config(text=course_name)
            for i in range(COURSE_LENGTH):
                par = course_model.par_order[i]
                hc = course_model.handicap_order[i]

                course_frame.par_dict[f'Hole {i+1}'].config(text=str(par))
                course_frame.hc_dict[f'Hole {i+1}'].config(text=str(hc))

    def get_course(self, course_name):
        """Get the course model by course name."""
        return self.model.course_list[course_name]
    
    def get_course_names(self):
        """Get a list of all course names."""
        return list(self.model.course_list.keys())
    
    def update_course_list(self):
        """Update the course list view with the latest data."""
        self.model.refresh_course_list()
        self.view.destroy_course_frames()
        self.view.generate_course_frames(self.get_course_names())
        self.populate_course_data()
