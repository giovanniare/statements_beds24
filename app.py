import tkinter as tk
from handler.app_handler import AppHandler


class App:
    def __init__(self) -> None:
        self.root = None
        self.app = None

    def build(self):
        # Build tkinter
        self.root = tk.Tk()
        # Call main handler
        self.app = AppHandler(self.root)
        # Authentication and data base creation
        self.app.initialize()

    def run(self):
        # Build project
        self.build()

        # Build tkinter main window
        self.app.lauch()

        # Tkinter loop
        self.root.mainloop()