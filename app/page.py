import tkinter as tk

class Page(tk.Frame):
    def __init__(self, parent: tk.Canvas) -> None:
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.active = False

    def show_page(self):
        pass

    def hide_page(self):
        pass

    def toggle_visible(self):
        if self.active == False:
            self.show_page()
        else:
            self.hide_page()
