from tkinter import *
import tkinter as tk
from Counter import *
from VideoGet import *
from ModelController import *
from SQLconnector import *
from PIL import Image, ImageTk


class CameraPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.model = ModelController()
        w = int(self.controller.width * 0.9)
        h = self.controller.height
        blank = np.full((h, w,3), 0, np.uint8)
        self.img = Image.fromarray(blank)
        self.imgtk = ImageTk.PhotoImage(image=self.img) 
        self.cam = parent.create_image(0,0, image=self.imgtk, anchor=NW)
        self.videothread = VideoGet(0, 20)
        self.active = False
        self.counterlist = [PushupCounter(), SitupCounter(), SquatCounter()]
        self.dbconnector = SQLconnector()
        self.counterlist[0].peakvalleycount = 10
        self.counterlist[0].totaltime = 100
        self.offsetnonframe = []

    def disableswitch(self):
        if self.active == True:
            if self.videothread.stopped == False:
                self.stopvid()
            # self.parent.itemconfig(self.cam, state='hidden')
            msg_box = tk.messagebox.askquestion('Warning', 'Are you save the counting to the database?(all progress will lost if no is selected)',icon='warning')
            if msg_box == 'yes':
                for p in range(len(self.counterlist)):
                    if self.counterlist[p].get_count() > 0:
                        MET = 3.8 * 3.5 * self.controller.weight / 200 * self.counterlist[p].totaltime / 60
                        self.dbconnector.save(self.counterlist[p].classname, self.counterlist[p].get_count(), self.controller.weight, self.counterlist[p].totaltime, MET)
            self.active = False
            self.counterlist = [PushupCounter(), SitupCounter(), SquatCounter()]
            self.model.model.reset()
        else:
            if self.videothread.stopped == True:
                self.startvid()
            self.parent.tag_raise(self.cam, 'all')
            self.active = True

    def setCamImg(self, imgnp):
        w = int(self.controller.width * 0.9)
        h = self.controller.height
        imgnp = cv2.resize(imgnp, (w, h))
        self.img = Image.fromarray(imgnp)
        self.imgtk = ImageTk.PhotoImage(image=self.img)  #must use same ImageTk object
        self.parent.itemconfig(self.cam, image=self.imgtk, anchor=NW)

    def videostopped(self):
        return self.videothread.stopped

    def startvid(self):
        self.videothread.start()

    def stopvid(self):
        self.videothread.stop()
        w = int(self.controller.width * 0.9)
        h = self.controller.height
        blank = np.full((h, w,3), 0, np.uint8)
        self.setCamImg(blank)
    
    def most_frequent(self, List):
        return max(set(List), key = List.count)

    def update_frame(self):
        if self.videothread.stopped == False:
            if len(self.videothread.grabbed) > 0:
                ret, frame = self.videothread.grabbed[0], self.videothread.frame[0]
                if ret:
                    img = self.model.detect(frame)
                    if self.model.prediction != Activity.non:
                        self.counterlist[self.model.prediction].update_count(self.model.angleforcount, time.time())
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
                    text = "Pushup: " + str(self.counterlist[0].get_count()) + " Situp: " + str(self.counterlist[1].get_count()) + " Squat: " + str(self.counterlist[2].get_count())
                    cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
                    self.setCamImg(img)
        else:
            w = int(self.controller.width * 0.9)
            h = self.controller.height
            blank = np.full((h, w,3), 0, np.uint8)
            self.setCamImg(blank)