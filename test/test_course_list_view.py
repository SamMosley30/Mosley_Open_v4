import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
import tkinter.ttk as ttk
from views.course_list_view import CourseListView, CourseInfoFrame

COURSE_LENGTH = 18

class TestCourseListView(unittest.TestCase):
    
    def setUp(self):
        # Create the Tkinter root widget
        self.root = tk.Tk()

        # Create the CourseListView instance
        self.view = CourseListView(self.root)
    
    def tearDown(self):
        # Destroy the Tkinter root widget
        self.root.destroy()
    
    def test_create_widgets(self):
        # Check if main widgets are created
        self.assertIsInstance(self.view.canvas, tk.Canvas)
        self.assertIsInstance(self.view.edit_course_btn, ttk.Button)
        self.assertIsInstance(self.view.return_btn, ttk.Button)
    
    def test_set_controller(self):
        controller = MagicMock()
        self.view.set_controller(controller)
        self.assertEqual(self.view.controller, controller)
        self.view.edit_course_btn.invoke()
        controller.open_course_editor.assert_called_once()
        self.view.return_btn.invoke()
        controller.open_menu.assert_called_once()
    
    def test_generate_course_frames(self):
        course_names = ['Course1', 'Course2']
        self.view.generate_course_frames(course_names)
        self.assertEqual(len(self.view.course_frames), 2)
        self.assertIn('Course1', self.view.course_frames)
        self.assertIn('Course2', self.view.course_frames)
        for course_frame in self.view.course_frames.values():
            self.assertIsInstance(course_frame, CourseInfoFrame)
    
    def test_destroy_course_frames(self):
        course_names = ['Course1', 'Course2']
        self.view.generate_course_frames(course_names)
        self.view.destroy_course_frames()
        self.assertEqual(len(self.view.course_frames), 0)
    
    def test_on_frame_configure(self):
        self.view.canvas.configure = MagicMock()
        event = MagicMock()
        self.view.on_frame_configure(event)
        self.view.canvas.configure.assert_called_once_with(scrollregion=self.view.canvas.bbox('all'))

class TestCourseInfoFrame(unittest.TestCase):

    def setUp(self):
        # Create the Tkinter root widget
        self.root = tk.Tk()

        # Create the CourseInfoFrame instance
        self.course_frame = CourseInfoFrame(self.root)
    
    def tearDown(self):
        # Destroy the Tkinter root widget
        self.root.destroy()
    
    def test_course_info_frame_creation(self):
        self.assertIsInstance(self.course_frame.course_name_label, ttk.Label)
        self.assertEqual(len(self.course_frame.par_dict), COURSE_LENGTH)
        self.assertEqual(len(self.course_frame.hc_dict), COURSE_LENGTH)
        for par_label in self.course_frame.par_dict.values():
            self.assertIsInstance(par_label, ttk.Label)
        for hc_label in self.course_frame.hc_dict.values():
            self.assertIsInstance(hc_label, ttk.Label)

if __name__ == '__main__':
    unittest.main()