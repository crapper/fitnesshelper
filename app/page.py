import tkinter as tk

class Page(tk.Frame):
    def __init__(self, parent: tk.Canvas) -> None:
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.active = False

    def disable_switch(self):
        pass

    def move_top(self):
        pass