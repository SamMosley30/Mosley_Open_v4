import unittest
from unittest.mock import MagicMock
import tkinter as tk
import tkinter.ttk as ttk
from views.course_view import CourseView, CourseEntryFrame

COURSE_LENGTH = 18

class TestCourseView(unittest.TestCase):

    def setUp(self):
        # Create the Tkinter root widget
        self.root = tk.Tk()

        # Mock the controller
        self.controller = MagicMock()

        # Create the CourseView instance
        self.view = CourseView(self.controller)
    
    def tearDown(self):
        # Destroy the Tkinter root widget
        self.root.destroy()

    def test_widgets_creation(self):
        # Check if main widgets are created
        self.assertIsInstance(self.view.course_entry_frame, CourseEntryFrame)
        self.assertIsInstance(self.view.save_course_btn, ttk.Button)
        self.assertIsInstance(self.view.delete_course_btn, ttk.Button)
        self.assertIsInstance(self.view.course_box, ttk.Combobox)

    def test_set_courses(self):
        # Test setting courses in combobox
        course_names = ['Course1', 'Course2']
        self.view.set_courses(course_names)
        self.assertEqual(self.view.course_box['values'], tuple(course_names))

    def test_get_course_name(self):
        # Test getting course name
        self.view.course_entry_frame.entry_course_name.insert(0, 'TestCourse')
        self.assertEqual(self.view.get_course_name(), 'TestCourse')

        # Test getting course name when entry is empty
        self.view.course_entry_frame.entry_course_name.delete(0, tk.END)
        self.assertIsNone(self.view.get_course_name())

    def test_get_par_order(self):
        # Test getting par order
        for i in range(COURSE_LENGTH):
            self.view.course_entry_frame.par_entry_dict[f'Hole {i+1}'].insert(0, str(i + 3))
        self.assertEqual(self.view.get_par_order(), [i + 3 for i in range(COURSE_LENGTH)])

        # Test getting par order with invalid input
        self.view.course_entry_frame.par_entry_dict['Hole 1'].delete(0, tk.END)
        self.view.course_entry_frame.par_entry_dict['Hole 1'].insert(0, 'invalid')
        self.assertIsNone(self.view.get_par_order())

    def test_get_handicap_order(self):
        # Test getting handicap order
        for i in range(COURSE_LENGTH):
            self.view.course_entry_frame.hc_entry_dict[f'Hole {i+1}'].insert(0, str(i + 1))
        self.assertEqual(self.view.get_handicap_order(), [i + 1 for i in range(COURSE_LENGTH)])

        # Test getting handicap order with invalid input
        self.view.course_entry_frame.hc_entry_dict['Hole 1'].delete(0, tk.END)
        self.view.course_entry_frame.hc_entry_dict['Hole 1'].insert(0, 'invalid')
        self.assertIsNone(self.view.get_handicap_order())

    def test_set_course_data(self):
        # Test setting course data
        course = MagicMock()
        course.name = 'TestCourse'
        course.par_order = [i + 3 for i in range(COURSE_LENGTH)]
        course.handicap_order = [i + 1 for i in range(COURSE_LENGTH)]

        self.view.set_course_data(course)
        self.assertEqual(self.view.course_entry_frame.entry_course_name.get(), 'TestCourse')
        for i in range(COURSE_LENGTH):
            self.assertEqual(self.view.course_entry_frame.par_entry_dict[f'Hole {i+1}'].get(), str(i + 3))
            self.assertEqual(self.view.course_entry_frame.hc_entry_dict[f'Hole {i+1}'].get(), str(i + 1))

        # Test setting course data to None
        self.view.set_course_data(None)
        self.assertEqual(self.view.course_entry_frame.entry_course_name.get(), '')
        for i in range(COURSE_LENGTH):
            self.assertEqual(self.view.course_entry_frame.par_entry_dict[f'Hole {i+1}'].get(), '')
            self.assertEqual(self.view.course_entry_frame.hc_entry_dict[f'Hole {i+1}'].get(), '')

class TestCourseEntryFrame(unittest.TestCase):

    def setUp(self):
        # Create the Tkinter root widget
        self.root = tk.Tk()

        # Mock the controller
        self.controller = MagicMock()

        # Create the CourseEntryFrame instance
        self.course_entry_frame = CourseEntryFrame(self.root, self.controller)
    
    def tearDown(self):
        # Destroy the Tkinter root widget
        self.root.destroy()
    
    def test_course_entry_frame_creation(self):
        self.assertIsInstance(self.course_entry_frame.entry_course_name, ttk.Entry)
        self.assertEqual(len(self.course_entry_frame.par_entry_dict), COURSE_LENGTH)
        self.assertEqual(len(self.course_entry_frame.hc_entry_dict), COURSE_LENGTH)
        for par_entry in self.course_entry_frame.par_entry_dict.values():
            self.assertIsInstance(par_entry, ttk.Entry)
        for hc_entry in self.course_entry_frame.hc_entry_dict.values():
            self.assertIsInstance(hc_entry, ttk.Entry)

if __name__ == '__main__':
    unittest.main()