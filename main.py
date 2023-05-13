import tkinter as tk
import tkcalendar as tkc
import tkinter.messagebox as messagebox
import tkinter.filedialog as fd
from PIL import Image, ImageTk
import datetime
import numpy as np

from app import *


class FitnessHelper(tk.Tk):
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
        self.weight = -1 # weight for calories calculation
        self.c = tk.Canvas(self, width=self.width, height=self.height, bg = 'blue')
        self.c.pack()
        self.expect_frame = 20
        self.temp_date = ""
        self.after_keeper = None

        # Create a dictionary of frames
        # self.bar = BarPage(self.c, self)
        self.frames = []
        self.frames.append(StatisticPage(self.c, self))
        self.frames.append(CameraPage(self.c, self))
        self.frames.append(VideoPage(self.c, self))
        self.frames.append(ConfigPage(self.c, self))

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

        self.update_frame()
        self.protocol("WM_DELETE_WINDOW", self.when_dead)

    def disabler(self, list_disable_index):
        for i in list_disable_index:
            if self.frames[i].active == True:
                self.frames[i].disable_switch()

    def update_video_date(self, date_win, cal):
        self.temp_date = cal.get_date()
        date_win.destroy()

    def pick_date(self, title="Pick Date"):
        date_win = tk.Toplevel(self)
        date_win.grab_set()
        date_win.title(title)
        year = int(datetime.datetime.today().strftime('%Y'))
        month = int(datetime.datetime.today().strftime('%m'))
        day = int(datetime.datetime.today().strftime('%d'))
        cal = tkc.Calendar(date_win, selectmode="day", year=year, month=month, day=day, date_pattern='dd-MM-yyyy')
        cal.pack(pady=20)
        ok_button = tk.Button(date_win, text="OK", command=lambda: self.update_video_date(date_win, cal))
        ok_button.pack(pady=20)
        date_win.wait_window()

    def switchCameraPage(self):
        if self.weight != -1:
            self.frames[1].disable_switch()
            list_disable = [0, 3]
            self.disabler(list_disable)
            if self.frames[2].active == True:
                self.frames[2].move_top()
        else:
            messagebox.showinfo('Warning', 'Please enter your weight in the config page')

    def switchVideoPage(self):
        if self.weight != -1:
            filetypes = (
                ('mp4 files', '*.mp4'),
                ('avi files', '*.avi')
            )
            if self.frames[2].active == False:
                list_disable = [0, 3]
                self.disabler(list_disable)
                filename = fd.askopenfilename(title='Open a file',filetypes=filetypes)
                if filename != '':
                    self.pick_date("Pick Date for Video")
                    self.frames[2].date = self.temp_date
                    self.frames[2].disable_switch()
                    if self.frames[2].video_stopped() == True:
                        self.frames[2].start_vid(filename)
            else:
                self.frames[2].disable_switch()
        else:
            messagebox.showinfo('Warning', 'Please enter your weight in the config page')

    def switchStatisticPage(self):
        any_other_active = False
        for i in range(len(self.frames)):
            if i != 0 and i != 3:
                if self.frames[i].active == True:
                    any_other_active = True
        if any_other_active == False:
            self.pick_date("Pick Start Date for Statistic")
            self.frames[0].start_date = self.temp_date
            self.pick_date("Pick End Date for Statistic")
            self.frames[0].end_date = self.temp_date
            self.frames[0].disable_switch()
            if self.frames[3].active == True:
                self.frames[3].move_top()

    def switchConfigPage(self):
        any_other_active = False
        for i in range(len(self.frames)):
            if i != 3 and i != 0:
                if self.frames[i].active == True:
                    any_other_active = True
        if any_other_active == False:
            self.frames[3].disable_switch()

    def update_frame(self):
        start_time = time.time()
        if self.frames[1].active:
            self.frames[1].update_frame()
        if self.frames[2].active:
            self.frames[2].update_frame()
        wait_time = max(1, math.ceil(1000/self.expect_frame - (time.time()- start_time)/1000))
        self.after_keeper = self.after(wait_time, self.update_frame)
    
    def when_dead(self):
        if self.after_keeper != None:
            self.after_cancel(self.after_keeper)
        self.quit()

if __name__ == "__main__":
    main_window = FitnessHelper()
    main_window.mainloop()