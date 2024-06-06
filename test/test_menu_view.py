import unittest
from unittest.mock import MagicMock
import tkinter as tk
from views.menu_view import MenuView

class TestMenuView(unittest.TestCase):

    def setUp(self):
        # Set up the Tkinter root widget
        self.root = tk.Tk()

        # Create an instance of the MenuView
        self.view = MenuView(self.root)

    def tearDown(self):
        # Destroy the Tkinter root widget
        self.root.destroy()

    def test_widgets_creation(self):
        # Check that the main label is created with correct text and font
        self.assertEqual(self.view.grid_size(), (1, 4))
        self.assertEqual(self.view.winfo_children()[0].cget('text'), 'Welcome to the Mosley Open')

        # Check that the Course List button is created with correct text
        self.assertEqual(self.view.course_list_btn.cget('text'), 'Course List')

    def test_set_controller(self):
        # Create a mock controller
        mock_controller = MagicMock()

        # Set the controller on the view
        self.view.set_controller(mock_controller)

        # Check that the controller is set correctly
        self.assertEqual(self.view.controller, mock_controller)

        # Simulate a button click
        self.view.course_list_btn.invoke()

        # Check that the Course List button is configured with the correct command
        mock_controller.show_course_list.assert_called_once()

if __name__=='__main__':
    unittest.main()
