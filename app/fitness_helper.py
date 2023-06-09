import tkinter as tk
import tkcalendar as tkc
import tkinter.messagebox as messagebox
import tkinter.filedialog as fd
from PIL import Image, ImageTk
import datetime
import math
import time
import numpy as np
import cv2

from .page import *
from .camera_page import *
from .config_page import *
from .statistic_page import *
from .video_page import *
from .tips_window import *

class FitnessHelper(App):
    def __init__(self, *args, **kwargs):
        App.__init__(self, *args, **kwargs)
        
        self.c = tk.Canvas(self, width=self.width, height=self.height, bg = 'black')
        self.c.pack()

        # Create a dictionary of frames
        self.statistic_page = StatisticPage(self.c, self)
        self.camera_page = CameraPage(self.c, self)
        self.video_page = VideoPage(self.c, self)
        self.config_page = ConfigPage(self.c, self)

        # create the bar with buttons
        self.start_x = int(self.width * 0.9)
        w = int(self.width * 0.1)
        h = self.height
        blank = np.full((h, w,3), 80, np.uint8)
        self.img = Image.fromarray(blank)
        self.img_tk = ImageTk.PhotoImage(image=self.img) 
        self.bar = self.c.create_image(self.start_x,0, image=self.img_tk, anchor=tk.NW)
        button_len = 64
        self.pixel = tk.PhotoImage(width=1, height=1)
        self.btn1 = tk.Button(self, image=self.pixel, width=64, height=64, command=lambda: self.switchCameraPage(), state=tk.NORMAL)
        self.btn1.place(x= self.start_x+button_len/2, y=button_len)
        self.btn2 = tk.Button(self, image=self.pixel, width=64, height=64, command=lambda: self.switchVideoPage(), state=tk.NORMAL)
        self.btn2.place(x= self.start_x+button_len/2, y=button_len*3)
        self.btn3 = tk.Button(self, image=self.pixel, width=64, height=64, command=lambda: self.switchConfigPage(), state=tk.NORMAL)
        self.btn3.place(x= self.start_x+button_len/2, y=button_len*5)
        self.btn4 = tk.Button(self, image=self.pixel, width=64, height=64, command=lambda: self.switchStatisticPage(), state=tk.NORMAL)
        self.btn4.place(x= self.start_x+button_len/2, y=button_len*7)
        self.create_hover_tip(self.btn1, text = "Camera Page Switch\n" "Cannot be used when:\n" "Weight is not initialize in config.")
        self.create_hover_tip(self.btn2, text = "Video Page Switch\n" "Cannot be used when:\n" "Weight is not initialize in config.")
        self.create_hover_tip(self.btn3, text = "Config Page Switch\n" "Cannot be used when:\n" "Camera/Video page is active.")
        self.create_hover_tip(self.btn4, text = "Statistic Page Switch\n" "Cannot be used when:\n" "Video page is active.")
        self.update_frame()
        self.protocol("WM_DELETE_WINDOW", self.before_destroy)

    def enter(self, widget, text):
        self.leave()
        self.tips = TipWindow(widget)
        self.tips.showtip(text)

    def leave(self):
        if self.tips != None:
            self.tips.hidetip()
            self.tips = None

    def create_hover_tip(self, widget, text):
        widget.bind('<Enter>',lambda event, widget=widget, text=text: self.enter(widget, text))
        widget.bind('<Leave>',lambda event: self.leave())

    def update_date(self, date_win: tk.Toplevel, cal: tkc.Calendar):
        self.temp_date = cal.get_date()
        date_win.destroy()

    def pick_date(self, title="Pick Date") -> str:
        self.temp_date = ""
        date_win = tk.Toplevel(self)
        date_win.resizable(0,0)
        date_win.grab_set()
        date_win.title(title)
        year = int(datetime.datetime.today().strftime('%Y'))
        month = int(datetime.datetime.today().strftime('%m'))
        day = int(datetime.datetime.today().strftime('%d'))
        cal = tkc.Calendar(date_win, selectmode="day", year=year, month=month, day=day, date_pattern='yyyy-mm-dd')
        cal.pack(pady=20)
        ok_button = tk.Button(date_win, text="OK", command=lambda: self.update_date(date_win, cal))
        ok_button.pack(pady=20)
        date_win.wait_window()

    def switchCameraPage(self):
        if self.weight == -1:
            messagebox.showinfo('Warning', 'Please enter your weight in the config page')
            return

        cap = cv2.VideoCapture(0)
        if cap.isOpened() == True:
            cap.release()
            self.statistic_page.request_close_page()
            self.config_page.request_close_page()
            self.camera_page.toggle_visible()

    def switchVideoPage(self):
        if self.weight == -1:
            messagebox.showinfo('Warning', 'Please enter your weight in the config page')
            return

        if self.video_page.active == False:
            self.statistic_page.request_close_page()
            self.config_page.request_close_page()
            
            filetypes = (
                ('mp4 files', '*.mp4'),
                ('avi files', '*.avi')
            )
            filename = fd.askopenfilename(title='Open a file',filetypes=filetypes)
            if filename == '':
                return
            
            self.pick_date("Pick Date for Video")
            self.video_page.date = self.temp_date
            if self.video_page.date == '':
                return
            if datetime.datetime.strptime(self.video_page.date, '%Y-%m-%d') > datetime.datetime.today():
                messagebox.showinfo('Warning', 'Please enter a date before today')
                return
            self.video_page.request_open_page()
            self.video_page.start_vid(filename)
        else:
            self.video_page.request_close_page()

    def switchStatisticPage(self):
        if self.video_page.active:
            return

        self.camera_page.request_close_page()

        if not self.statistic_page.active:
            self.pick_date("Pick Start Date for Statistic")
            self.statistic_page.start_date = self.temp_date
            self.pick_date("Pick End Date for Statistic")
            self.statistic_page.end_date = self.temp_date
        if self.statistic_page.start_date != '' and self.statistic_page.end_date != '':
            self.statistic_page.toggle_visible()

    def switchConfigPage(self):
        if self.video_page.active or self.camera_page.active:
            return
        self.config_page.toggle_visible()

    def update_frame(self):
        start_time = time.time()
        
        self.video_page.update_frame()
        self.camera_page.update_frame()

        wait_time = max(1, math.ceil(1000/self.expect_frame - (time.time()- start_time)/1000))
        self.after_keeper = self.after(wait_time, self.update_frame)
    
    def before_destroy(self):
        if self.after_keeper != None:
            self.after_cancel(self.after_keeper)
        self.quit()
