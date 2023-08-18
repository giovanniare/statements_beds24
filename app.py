import tkinter as tk
from window.window_maker import Window

root = tk.Tk()

# Initalize window maker
window = Window(root)

# Create window
window.create_window()

root.mainloop()