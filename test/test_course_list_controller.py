import unittest
from unittest.mock import MagicMock, patch
from controllers.course_list_controller import CourseListController
from views.menu_view import MenuView

class TestCourseListController(unittest.TestCase):
    
    def setUp(self):
        # Mock application, model, and view
        self.application = MagicMock()
        self.model = MagicMock()
        self.view = MagicMock()

        # Mock course model
        self.course_model = MagicMock()
        self.course_model.par_order = [3] * 18
        self.course_model.handicap_order = [1] * 18

        # Simulate a course list in the model
        self.model.course_list = {
            'Course1': self.course_model,
            'Course2': self.course_model
        }

        # Initialize the CourseListController with mocks
        self.controller = CourseListController(self.application, self.model, self.view)
    
    def test_init(self):
        # Ensure the controller initializes correctly
        self.view.set_controller.assert_called_once_with(self.controller)
        self.view.generate_course_frames.assert_called_once_with(['Course1', 'Course2'])
        self.assertEqual(self.controller.view, self.view)
        self.assertEqual(self.controller.model, self.model)
        self.assertEqual(self.controller.application, self.application)

    def test_open_course_editor(self):
        with patch('controllers.course_list_controller.CourseController') as mock_course_controller:
            self.controller.open_course_editor()
            mock_course_controller.assert_called_once_with(self.controller)

    def test_delete_course_editor(self):
        self.controller.delete_course_editor(None)
        self.assertIsNone(self.controller.course_controller)

    def test_open_menu(self):
        self.controller.open_menu()
        self.application.show_frame.assert_called_once_with(MenuView)

    def test_populate_course_data(self):
        # Mock course frames in the view
        course_frame_mock = MagicMock()
        self.view.course_frames = {
            'Course1': course_frame_mock,
            'Course2': course_frame_mock
        }

        self.controller.populate_course_data()

        # Check if the course data is populated correctly
        for course_frame in self.view.course_frames.values():
            course_frame.course_name_label.config.assert_called_with(text='Course2')
            for i in range(18):
                course_frame.par_dict[f'Hole {i+1}'].config.assert_called_with(text='3')
                course_frame.hc_dict[f'Hole {i+1}'].config.assert_called_with(text='1')

    def test_get_course(self):
        course = self.controller.get_course('Course1')
        self.assertEqual(course, self.course_model)

    def test_get_course_names(self):
        course_names = self.controller.get_course_names()
        self.assertEqual(course_names, ['Course1', 'Course2'])

    def test_update_course_list(self):
        # Reset mock calls
        self.view.generate_course_frames.reset_mock()

        self.controller.update_course_list()
        self.model.refresh_course_list.assert_called_once()
        self.view.destroy_course_frames.assert_called_once()
        self.view.generate_course_frames.assert_called_once_with(['Course1', 'Course2'])
        
if __name__ == '__main__':
    unittest.main()