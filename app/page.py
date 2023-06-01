import tkinter as tk
from .tips_window import *

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Adding a title to the window
        self.wm_title("FitnessHelper")
        self.geometry("1280x720")
        self.minsize(width=1280, height=720)
        self.maxsize(width=1280, height=720)
        self.resizable(0,0)

        self.width = 1280
        self.height = 720
        self.initialize_attribute()
    
    def initialize_attribute(self):
        self.weight = -1 # weight for calories calculation
        self.model_complexity = 1
        self.model_conf = 0.5
        self.track_conf = 0.5
        self.statistic_unit = 0
        self.temp_date = ""
        self.expect_frame = 20
        self.after_keeper = None
        self.tips: TipWindow = None

class Page(tk.Frame):
    def __init__(self, parent: tk.Canvas, controller: App) -> None:
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.active = False

    def show_page(self):
        pass

    def hide_page(self):
        pass

    def request_open_page(self) -> bool:
        return False

    def request_close_page(self) -> bool:
        return False

    def toggle_visible(self) -> bool:
        if self.active == False:
            self.request_open_page()
        else:
            self.request_close_page()
        return self.active
    
    def update_frame(self):
        pass
