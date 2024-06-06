import unittest
import sys
from unittest.mock import patch, mock_open, MagicMock

sys.path.append("/Users/sammo/Mosley_Open_v4")
from models.course import Course


class TestCourseModel(unittest.TestCase):

    def setUp(self):
        self.course_name = "Test Course"
        self.par_order = [4, 4, 3, 4, 4, 5, 3, 4, 5, 4, 4, 3, 4, 4, 5, 3, 4, 5]
        self.handicap_order = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        self.course = Course(self.course_name, self.par_order, self.handicap_order)

    def test_course_initialization(self):

        # Attempt to create a course object with an invalid handicap order length
        with self.assertRaises(ValueError):
            course = Course(self.course_name, self.par_order, [1, 2, 3])

        self.assertEqual(self.course.name, self.course_name)
        self.assertEqual(self.course.par_order, self.par_order)
        self.assertEqual(self.course.handicap_order, self.handicap_order)
        self.assertTrue(self.course.save_path.endswith(f'{self.course_name}.yaml'))

    def test_invalid_course_name(self):
        with self.assertRaises(ValueError) as context:
            Course(123, self.par_order, self.handicap_order)
        self.assertEqual(str(context.exception), "Course name must be a string.")

    def test_no_course_name(self):
        with self.assertRaises(ValueError) as context:
            Course('', self.par_order, self.handicap_order)
        self.assertEqual(str(context.exception), "Course name cannot be empty.")

    def test_invalid_course_par_length(self):
        with self.assertRaises(ValueError) as context:
            Course(self.course_name, [4]*17, self.handicap_order)
        self.assertEqual(str(context.exception), "Course par length must be 18, got 17.")

    def test_invalid_course_handicap_length(self):
        with self.assertRaises(ValueError) as context:
            Course(self.course_name, self.par_order, list(range(1, 18)))
        self.assertEqual(str(context.exception), "Course handicap length must be 18, got 17.")

    @patch("builtins.open", new_callable=mock_open)
    @patch("yaml.dump")
    def test_save_course(self, mock_yaml_dump, mock_open):
        self.course.save()
        mock_open.assert_called_once_with(self.course.save_path, 'w')
        mock_yaml_dump.assert_called_once_with(self.course, mock_open())

    @patch('models.course.path.exists')
    @patch('models.course.remove')
    def test_delete_success(self, mock_remove, mock_path_exists):
        # Simulate that the file exists
        mock_path_exists.return_value = True

        # Mock the trigger_event method
        self.course.trigger_event = MagicMock()

        # Call the delete method
        self.course.delete()

        filepath = 'c:\\Users\\sammo\\Mosley_Open_v4\\courselib\\Test Course.yaml'
        # Check if path.exists was called with the correct path
        mock_path_exists.assert_called_once_with(filepath)

        # Check if remove was called with the correct path
        mock_remove.assert_called_once_with(filepath)

        # Check if the trigger_event method was called with 'delete'
        self.course.trigger_event.assert_called_once_with('delete')
    

    def test_event_notification(self):
        # Test event notification on save and delete
        events_triggered = []

        def on_save(model):
            events_triggered.append('save')

        def on_delete(model):
            events_triggered.append('delete')

        self.course.add_event_listener('save', on_save)
        self.course.add_event_listener('delete', on_delete)

        self.course.save()
        self.course.delete()

        self.assertIn('save', events_triggered)
        self.assertIn('delete', events_triggered)


if __name__ == '__main__':
    unittest.main()
