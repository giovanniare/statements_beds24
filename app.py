import tkinter as tk
from handler.app_handler import AppHandler

# Build tkinter
root = tk.Tk()

# Call main handler
app = AppHandler(root)

# Authentication and data base creation
app.initialize()

# Build tkinter main window
app.lauch()

# Tkinter loop
root.mainloop()