
import sys
import tkinter as tk
import tkinter.ttk as ttk

sys.path.append("/Users/sammo/Mosley_Open_v4")

from models.course_list import CourseList
from views.course_list_view import CourseListView
from views.menu_view import MenuView
from controllers.course_list_controller import CourseListController
from controllers.menu_controller import MenuController

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.title('Mosley Open')
        self.geometry('675x600')

        self.frames = dict()

        container = ttk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        # Initialize the menu view and controller.
        menu_view = MenuView(container)
        menu_controller = MenuController(self, menu_view)
        self.frames[MenuView] = menu_view

        course_list_model = CourseList()
        course_list_view = CourseListView(container)
        course_list_controller = CourseListController(self, course_list_model, course_list_view)
        self.frames[CourseListView] = course_list_view

        # Show the initial frame
        self.show_frame(MenuView)

    def show_frame(self, view_class):
        """Raises the input view to the front of the application."""
        frame = self.frames[view_class]
        frame.tkraise()

if __name__ == '__main__':
    app = App()
    app.mainloop()
