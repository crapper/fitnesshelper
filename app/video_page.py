import cv2
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk

from .model_controller import *
from .video_get import *
from .sql_connector import *
from .counter import *


class VideoPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.model = ModelController()
        self.panel = []
        self.BgTopx = 688
        self.BgTopy = 188
        self.BgDownx = 1088
        self.BgDowny = 488
        self.shapetripointer={'bounds': [1152, 224, self.BgDownx, 192, self.BgDownx, 256], 'kind': 'tri', 'fill': True}
        self.panel.append(self.parent.create_polygon(list(self.shapetripointer.values())[0],fill='white',outline='green', width = 5))#[0] : widget background panel triangle
        self.panel.append(self.parent.create_rectangle(self.BgTopx, self.BgTopy,self.BgDownx,self.BgDowny,fill='white',outline='green', width = 5)) #[1] : widget background panel rectangle
        self.dbconnector = SQLconnector()
        blank = np.full((int((self.BgDowny-self.BgTopy)*0.8/2), int((self.BgDownx-self.BgTopx)*0.8),3), 0, np.uint8)
        self.img = Image.fromarray(blank)
        self.imgtk = ImageTk.PhotoImage(image=self.img) 
        self.cam = self.parent.create_image(self.BgTopx+int((self.BgDownx-self.BgTopx)*0.1),self.BgTopy+int((self.BgDowny-self.BgTopy)*0.1), image=self.imgtk, anchor=tk.NW)
        self.panel.append(self.cam) #[2] : widget camera image
        self.panel.append(self.parent.create_rectangle(self.BgTopx+int((self.BgDownx-self.BgTopx)*0.1),
        ( self.BgTopy+int((self.BgDowny-self.BgTopy)*0.1) + int((self.BgDowny-self.BgTopy)*0.8/2) ),
        self.BgDownx-int((self.BgDownx-self.BgTopx)*0.1),
        ( self.BgTopy+int((self.BgDowny-self.BgTopy)*0.1) + int((self.BgDowny-self.BgTopy)*0.8/2) +int((self.BgDowny-self.BgTopy)*0.05) ),
        fill='gray',outline='black')) #[3] : widget progress bar border

        self.barfill = self.parent.create_rectangle( self.BgTopx+int((self.BgDownx-self.BgTopx)*0.1)+1,
         ( self.BgTopy+int((self.BgDowny-self.BgTopy)*0.1) + int((self.BgDowny-self.BgTopy)*0.8/2) ) +1,
          self.BgTopx+int((self.BgDownx-self.BgTopx)*0.1)-1,
          ( self.BgTopy+int((self.BgDowny-self.BgTopy)*0.1) + int((self.BgDowny-self.BgTopy)*0.8/2) +int((self.BgDowny-self.BgTopy)*0.05)),
          fill='green') #final x = self.BgDownx-11

        self.total = int((self.BgDownx-self.BgTopx)*0.8)-2
        self.initialx = self.BgTopx+int((self.BgDownx-self.BgTopx)*0.1)+1
        self.panel.append(self.barfill) #[4] : widget progress bar fill, total 378 pixels

        self.counterlist = [PushupCounter(), SquatCounter(), SitupCounter()]
        self.panel.append(self.parent.create_text(self.BgTopx+int((self.BgDownx-self.BgTopx)*0.1), ( self.BgTopy+int((self.BgDowny-self.BgTopy)*0.1) + int((self.BgDowny-self.BgTopy)*0.8/2) +int((self.BgDowny-self.BgTopy)*0.05) ), text="Pushup: "+str(self.counterlist[Activity.pushup].get_count()), font=("Helvetica", 16), fill="black", anchor=tk.NW)) #[5] : widget text pushup counter
        self.panel.append(self.parent.create_text(self.BgTopx+int((self.BgDownx-self.BgTopx)*0.1) , ( self.BgTopy+int((self.BgDowny-self.BgTopy)*0.1) + int((self.BgDowny-self.BgTopy)*0.8/2) +int((self.BgDowny-self.BgTopy)*0.05) )+16+16, text="Situp: "+str(self.counterlist[Activity.pushup].get_count()), font=("Helvetica", 16), fill="black", anchor=tk.NW)) #[6] : widget text situp counter
        self.panel.append(self.parent.create_text(self.BgTopx+int((self.BgDownx-self.BgTopx)*0.1) , ( self.BgTopy+int((self.BgDowny-self.BgTopy)*0.1) + int((self.BgDowny-self.BgTopy)*0.8/2) +int((self.BgDowny-self.BgTopy)*0.05) )+16+16+16+16, text="Squat: "+str(self.counterlist[Activity.pushup].get_count()), font=("Helvetica", 16), fill="black", anchor=tk.NW)) #[7] : widget text squat counter
        self.pixel = tk.PhotoImage(width=1, height=1)
        self.savebtn = tk.Button(self.controller, image=self.pixel, text="Save", state='disable', width=int((self.BgDownx-self.BgTopx)*0.2), height =int((self.BgDowny-self.BgTopy)*0.1), compound='c', command=lambda: self.save())
        self.savebtn.place(x= self.BgDownx - int((self.BgDownx-self.BgTopx)*0.3), y = ( self.BgTopy+int((self.BgDowny-self.BgTopy)*0.1) + int((self.BgDowny-self.BgTopy)*0.8/2) +int((self.BgDowny-self.BgTopy)*0.1) )+16+16)
        self.savebtn.place_forget()
        self.date = ""
        self.active = False
        self.videothread = None
        self.frameread = 0
        self.offsetnonframe = []
        for item in self.panel:
            self.parent.itemconfig(item, state='hidden')
    def save(self):
        for p in range(len(self.counterlist)):
            if self.counterlist[p].get_count() > 0:
                MET = 3.8 * 3.5 * self.controller.weight / 200 * (self.counterlist[p].totaltime/self.videothread.fpsvideo/ 60)
                self.dbconnector.save(self.counterlist[p].classname, self.counterlist[p].get_count(), self.controller.weight, self.counterlist[p].totaltime/self.videothread.fpsvideo, MET)
        self.stopvid()
        self.initialize()

    def videostopped(self):
        if self.videothread != None:
            return self.videothread.stopped
        else:
            return True
    def setCamImg(self, imgnp):
        w = int((self.BgDownx-self.BgTopx)*0.8)
        h = int((self.BgDowny-self.BgTopy)*0.8/2)
        imgnp = cv2.resize(imgnp, (w, h))
        self.img = Image.fromarray(imgnp)
        self.imgtk = ImageTk.PhotoImage(image=self.img)  #must use same ImageTk object
        self.parent.itemconfig(self.cam, image=self.imgtk, anchor=tk.NW)

    def updatecount(self):
        self.parent.itemconfig(self.panel[5], text="Pushup: "+str(self.counterlist[Activity.pushup].get_count()))
        self.parent.itemconfig(self.panel[6], text="Situp: "+str(self.counterlist[Activity.situp].get_count()))
        self.parent.itemconfig(self.panel[7], text="Squat: "+str(self.counterlist[Activity.squat].get_count()))

    def startvid(self, source):
        if self.videothread != None:
            self.videothread.start()
        else:
            self.videothread = VideoGet(source, 15)
            self.videothread.start()

    def stopvid(self):
        if self.videothread != None:
            self.videothread.stop()
        w = int((self.BgDownx-self.BgTopx)*0.8)
        h = int((self.BgDowny-self.BgTopy)*0.8/2)
        blank = np.full((h, w,3), 0, np.uint8)
        self.setCamImg(blank)
    
    def initialize(self):
        self.date = ""
        self.savebtn["state"] = "disable"
        self.savebtn.place_forget()
        self.counterlist = [PushupCounter(), SitupCounter(), SquatCounter()]
        self.dbconnector = SQLconnector()
        if self.videothread!= None:
            self.videothread = None
        self.frameread = 0
        x0, y0, x1, y1 = self.parent.coords(self.barfill)
        self.parent.coords(self.barfill, self.initialx, y0, self.initialx, y1)
        for item in self.panel:
            self.parent.itemconfig(item, state='hidden')
        self.active = False
        self.model.model.reset()

    def disableswitch(self):
        if self.active == True:
            self.stopvid()
            msg_box = tk.messagebox.askquestion('Warning', 'Are you sure you want to terminate the process?(all progress will lost)',icon='warning')
            if msg_box == 'yes':
                self.initialize()
            else:
                self.videothread.start()
                self.update_frame()
        else:
            self.dbconnector.date = self.date
            for item in self.panel:
                self.parent.itemconfig(item, state='normal')
                self.parent.tag_raise(item, 'all')
            self.savebtn.place(x= self.BgDownx - int((self.BgDownx-self.BgTopx)*0.3), y = ( self.BgTopy+int((self.BgDowny-self.BgTopy)*0.1) + int((self.BgDowny-self.BgTopy)*0.8/2) +int((self.BgDowny-self.BgTopy)*0.1) )+16+16)
            self.active = True

    def most_frequent(self, List):
        return max(set(List), key = List.count)

    def update_frame(self):
        if self.videothread.stopped == False and self.frameread != self.videothread.totalframe+1:
            if len(self.videothread.frame) != 0: #self.frameread <= self.videothread.currentframe
                ret, frame = self.videothread.grabbed.pop(0), self.videothread.frame.pop(0)
                self.frameread += 1
                if ret:
                    img = self.model.detect(frame)
                    if self.model.prediction != Activity.non:
                        self.counterlist[self.model.prediction].update_count(self.model.angleforcount, self.frameread)
                        self.updatecount()
                    self.offsetnonframe.append(self.model.prediction)
                    if len(self.offsetnonframe) >= 10:
                        maxappear = self.most_frequent(self.offsetnonframe)
                        setlist = list(set(self.offsetnonframe))
                        setlist.remove(maxappear)
                        for i in setlist:
                            if i != Activity.non:
                                self.counterlist[i].state = ActivityType.NA
                                if self.counterlist[i].peakvalleycount % 2 == 1:
                                    self.counterlist[i].peakvalleycount -= 1
                                self.counterlist[i].tempcount_time = 0
                    self.setCamImg(img)
                    x0, y0, x1, y1 = self.parent.coords(self.barfill)
                    x1 = self.initialx + int(self.total * self.frameread/self.videothread.totalframe)
                    self.parent.coords(self.barfill, x0, y0, x1, y1)
        else:
            w = int((self.BgDownx-self.BgTopx)*0.8)
            h = int((self.BgDowny-self.BgTopy)*0.8/2)
            blank = np.full((h, w,3), 0, np.uint8)
            self.setCamImg(blank)
            if self.videothread.finished:
                self.savebtn["state"] = "normal"
    def movetop(self):
        for item in self.panel:
            self.parent.tag_raise(item, 'all')