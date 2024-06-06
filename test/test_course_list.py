import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import yaml

from models.course_list import CourseList
from models.course import Course

class TestCourseList(unittest.TestCase):

    def setUp(self):
        # Mock data
        self.course_data_1 = {
            'course_name': 'Sample Course1',
            'course_par': [4, 4, 3, 4, 4, 5, 3, 4, 5, 4, 4, 3, 4, 4, 5, 3, 4, 5],
            'course_handicap': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        }
        self.course_data_2 = {
            'course_name': 'Sample Course2',
            'course_par': [4, 4, 3, 4, 4, 5, 3, 4, 5, 4, 4, 3, 4, 4, 5, 3, 4, 5],
            'course_handicap': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        }
        self.mock_course1 = Course(**self.course_data_1)
        self.mock_course2 = Course(**self.course_data_2)
        self.yaml_data1 = yaml.dump(self.mock_course1)
        self.yaml_data2 = yaml.dump(self.mock_course2)

        self.course_lib_path = '\\Users\\sammo\\Mosley_Open_v4\\courselib'

    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open, read_data='')
    @patch('yaml.load')
    def test_load_course_library(self, mock_yaml_load, mock_open, mock_listdir):
        mock_listdir.return_value = ['course1.yaml', 'course2.yaml']
        mock_yaml_load.side_effect = [self.mock_course1, self.mock_course2]
        
        course_list = CourseList()

        self.assertEqual(len(course_list.course_list), 2)
        self.assertIn('Sample Course1', course_list.course_list)
        self.assertIn('Sample Course2', course_list.course_list)

    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open, read_data='')
    @patch('yaml.load')
    def test_load_course_library_invalid_course(self, mock_yaml_load, mock_open, mock_listdir):
        mock_listdir.return_value = ['invalid_course.yaml']
        mock_yaml_load.return_value = {}

        with self.assertRaises(TypeError):
            CourseList()

    @patch('os.listdir')
    @patch('builtins.open', new_callable=mock_open, read_data='')
    @patch('yaml.load')
    def test_refresh_course_list(self, mock_yaml_load, mock_open, mock_listdir):
        mock_listdir.return_value = ['course1.yaml']
        mock_yaml_load.return_value = self.mock_course1
        
        course_list = CourseList()

        # Initially, one course should be loaded
        self.assertEqual(len(course_list.course_list), 1)
        
        # Update the mock to simulate a new course file
        mock_listdir.return_value = ['course1.yaml', 'course2.yaml']
        mock_yaml_load.side_effect = [self.mock_course1, self.mock_course2]
        course_list.refresh_course_list()
        
        # After refreshing, two courses should be loaded
        self.assertEqual(len(course_list.course_list), 2)

if __name__ == '__main__':
    unittest.main()