import unittest
from unittest.mock import MagicMock, create_autospec
from controllers.menu_controller import MenuController
from views.menu_view import MenuView
from views.course_list_view import CourseListView

class TestMenuController(unittest.TestCase):

    def setUp(self):
        # Create a mock application object
        self.mock_application = MagicMock()

        # Create a mock view, making sure it's an instance of MenuView
        self.mock_view = create_autospec(MenuView, instance=True)

        # Create an instance of the Menu Controller with the mock objects
        self.controller = MenuController(self.mock_application, self.mock_view)

    def test_show_course_list(self):
        # Call method to be tested
        self.controller.show_course_list()

        # Verify that the application.show_frame method was called with the
        # correct arguments
        self.mock_application.show_frame.assert_called_once_with(CourseListView)

    def test_set_controller(self):
        # Verify that the view's set_controller method was called with the controller
        # instance.
        self.mock_view.set_controller.assert_called_once_with(self.controller)

if __name__=='__main__':
    unittest.main()