import unittest
from unittest.mock import MagicMock, patch
from controllers.course_controller import CourseController
from models.course import Course

class TestCourseController(unittest.TestCase):

    def setUp(self):
        self.mock_course_list_controller = MagicMock()
        self.mock_view = MagicMock()
        self.sample_par_order = [4, 4, 3, 4, 4, 5, 3, 4, 5, 4, 4, 3, 4, 4, 5, 3, 4, 5]
        self.sample_handicap_order = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        
        # Patch the CourseView to return the mock view
        patcher = patch('controllers.course_controller.CourseView', return_value=self.mock_view)
        self.addCleanup(patcher.stop)
        self.mock_course_view_class = patcher.start()
        
        # Initialize the CourseController with the mocked course list controller
        self.controller = CourseController(self.mock_course_list_controller)

    def test_initialization(self):
        self.mock_course_view_class.assert_called_once_with(self.controller)
        self.assertIsNone(self.controller.model)
        self.mock_view.bind.assert_called_once_with('<Destroy>', self.mock_course_list_controller.delete_course_editor)
        self.mock_course_list_controller.get_course_names.assert_called_once()

    @patch('controllers.course_controller.Course')
    def test_save_course(self, MockCourse):
        # Test saving a new course
        self.mock_view.get_course_name.return_value = "Test Course"
        self.mock_view.get_par_order.return_value = self.sample_par_order
        self.mock_view.get_handicap_order.return_value = self.sample_handicap_order

        self.controller.save_course()

        MockCourse.assert_called_once_with("Test Course", self.sample_par_order, self.sample_handicap_order)
        MockCourse().save.assert_called_once()
        self.mock_course_list_controller.update_course_list.assert_called_once()
        self.assertIsNone(self.controller.model)
        self.mock_view.set_course_data.assert_called_once_with(None)

    def test_delete_course(self):
        # Test deleting an existing course
        mock_model = MagicMock()
        self.controller.model = mock_model
        self.controller.delete_course()

        mock_model.delete.assert_called_once()
        self.mock_course_list_controller.update_course_list.assert_called_once()
        self.assertIsNone(self.controller.model)

    def test_load_course(self):
        # Test loading a course
        mock_course = MagicMock()
        self.mock_course_list_controller.get_course.return_value = mock_course
        self.mock_view.course_box.get.return_value = "Test Course"

        self.controller.load_course(None)

        self.mock_course_list_controller.get_course.assert_called_once_with("Test Course")
        self.mock_view.set_course_data.assert_called_once_with(mock_course)
        self.assertEqual(self.controller.model, mock_course)

    def test_update_course_list(self):
        # Reset the call count for get_course_names and the view after initialization
        self.mock_course_list_controller.get_course_names.reset_mock()
        self.mock_view.set_courses.reset_mock()

        # Test updating the course list
        self.mock_course_list_controller.get_course_names.return_value = ["Course1", "Course2"]

        self.controller.update_course_list()

        self.mock_course_list_controller.get_course_names.assert_called_once()
        self.mock_view.set_courses.assert_called_once_with(["Course1", "Course2"])

if __name__ == '__main__':
    unittest.main()