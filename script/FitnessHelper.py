import tkinter as tk
from tkinter import *
from datetime import datetime
from SQLconnector import *
from BarPage import *
from StatisticPage import *
from CameraPage import *
from VideoPage import *
from ConfigPage import *
import tkcalendar as tkc
from tkinter import filedialog as fd


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
        self.c = Canvas(self, width=self.width, height=self.height, bg = 'blue')
        self.c.pack()
        self.expectframe = 20
        self.tempdate = ""
        self.updatefun = None

        # Create a dictionary of frames
        self.bar = BarPage(self.c, self)
        self.frames = []
        self.frames.append(StatisticPage(self.c, self))
        self.frames.append(CameraPage(self.c, self))
        self.frames.append(VideoPage(self.c, self))
        self.frames.append(ConfigPage(self.c, self))
        self.update_frame()
        self.protocol("WM_DELETE_WINDOW", self.whendead)

    def disabler(self, listdisableindex):
        for i in listdisableindex:
            if self.frames[i].active == True:
                self.frames[i].disableswitch()

    def updatevideodate(self, date_win, cal):
        self.tempdate = cal.get_date()
        date_win.destroy()

    def pick_date(self, title="Pick Date"):
        date_win = Toplevel(self)
        date_win.grab_set()
        date_win.title(title)
        year = int(datetime.today().strftime('%Y'))
        month = int(datetime.today().strftime('%m'))
        day = int(datetime.today().strftime('%d'))
        cal = tkc.Calendar(date_win, selectmode="day", year=year, month=month, day=day, date_pattern='dd-MM-yyyy')
        cal.pack(pady=20)
        ok_button = Button(date_win, text="OK", command=lambda: self.updatevideodate(date_win, cal))
        ok_button.pack(pady=20)
        date_win.wait_window()

    def switchCameraPage(self):
        if self.weight != -1:
            self.frames[1].disableswitch()
            list_disable = [0, 3]
            self.disabler(list_disable)
            if self.frames[2].active == True:
                self.frames[2].movetop()
        else:
            tk.messagebox.showinfo('Warning', 'Please enter your weight in the config page')

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
                    self.frames[2].date = self.tempdate
                    self.frames[2].disableswitch()
                    if self.frames[2].videostopped() == True:
                        self.frames[2].startvid(filename)
            else:
                self.frames[2].disableswitch()
        else:
            tk.messagebox.showinfo('Warning', 'Please enter your weight in the config page')

    def switchStatisticPage(self):
        anyotheractive = False
        for i in range(len(self.frames)):
            if i != 0 and i != 3:
                if self.frames[i].active == True:
                    anyotheractive = True
        if anyotheractive == False:
            self.pick_date("Pick Start Date for Statistic")
            self.frames[0].startdate = self.tempdate
            self.pick_date("Pick End Date for Statistic")
            self.frames[0].enddate = self.tempdate
            self.frames[0].disableswitch()
            if self.frames[3].active == True:
                self.frames[3].movetop()

    def switchConfigPage(self):
        anyotheractive = False
        for i in range(len(self.frames)):
            if i != 3 and i != 0:
                if self.frames[i].active == True:
                    anyotheractive = True
        if anyotheractive == False:
            self.frames[3].disableswitch()

    def update_frame(self):
        starttime = time.time()
        if self.frames[1].active:
            self.frames[1].update_frame()
        if self.frames[2].active:
            self.frames[2].update_frame()
        wait_time = max(1, math.ceil(1000/self.expectframe - (time.time()- starttime)/1000))
        self.updatefun = self.after(wait_time, self.update_frame)
    
    def whendead(self):
        if self.updatefun != None:
            self.after_cancel(self.updatefun)
        self.quit()