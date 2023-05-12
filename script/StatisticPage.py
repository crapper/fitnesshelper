import tkinter as tk
import numpy as np
from tkinter import *
from PIL import Image, ImageTk
import cv2
from datetime import datetime
from SQLconnector import *
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter


class StatisticPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.active = False
        w = int(self.controller.width * 0.9)
        h = self.controller.height
        blank = np.full((h, w,3), 255, np.uint8)
        self.img = Image.fromarray(blank)
        self.imgtk = ImageTk.PhotoImage(image=self.img) 
        self.cam = parent.create_image(0,0, image=self.imgtk, anchor=NW)
        self.dbconnector = SQLconnector()
        self.startdate = ""
        self.enddate = ""
        self.statisticpage = []
        self.state = 0
        self.leftbtn = Button(self.controller, text="<", command=lambda: self.changestate(-1))
        self.leftbtn.place(x=0, y=h/2)
        self.rightbtn = Button(self.controller, text=">", command=lambda: self.changestate(1))
        self.rightbtn.place(x=0, y=h/2+100)
        self.leftbtn.place_forget()
        self.rightbtn.place_forget()
        
    def changestate(self, state):
        self.state = (self.state + state) % 4
        self.setCamImg(self.statisticpage[self.state])

    def disableswitch(self):
        if self.active == True:
            self.active = False
            self.startdate = ""
            self.enddate = ""
            self.state = 0
            self.statisticpage = []
            self.leftbtn.place_forget()
            self.rightbtn.place_forget()
            w = int(self.controller.width * 0.9)
            h = self.controller.height
            blank = np.full((h, w,3), 255, np.uint8)
            self.setCamImg(blank)
        else:
            dt = datetime.strptime(self.startdate, '%d-%m-%Y').date()
            dt2 = datetime.strptime(self.enddate, '%d-%m-%Y').date()
            if dt > dt2:
                tk.messagebox.showinfo('Warning', 'End date must be later than start date')
                self.startdate = ""
                self.enddate = ""
            else:
                self.leftbtn.place(x=0, y=self.controller.height/2)
                self.rightbtn.place(x=0, y=self.controller.height/2+100)
                self.active = True
                self.parent.tag_raise(self.cam, 'all')
                self.statisticpage.append(self.listtoimg(self.dbconnector.extractcalorieslist(self.startdate, self.enddate), "Calories Trend for all activities"))
                self.statisticpage.append(self.listtoimg(self.dbconnector.extractcalorieslist(self.startdate, self.enddate, "pushup"), "Calories Trend for pushup"))
                self.statisticpage.append(self.listtoimg(self.dbconnector.extractcalorieslist(self.startdate, self.enddate, "situp"), "Calories Trend for situp"))
                self.statisticpage.append(self.listtoimg(self.dbconnector.extractcalorieslist(self.startdate, self.enddate, "squat"), "Calories Trend for squat"))
                self.setCamImg(self.statisticpage[self.state])
                
    def listtoimg(self, lst, title="Calories Trend"):
        dateMETlist = []
        for k in lst:
            datestring = k[1]
            dt = datetime.strptime(datestring, '%d-%m-%Y')
            tempfound = False
            for i in range(len(dateMETlist)):
                if dt == dateMETlist[i][0]:
                    dateMETlist[i][1] += k[5]
                    tempfound = True
                    break
            if tempfound == False:
                dateMETlist.append([dt, k[5]])

        dateMETlist.sort(key=lambda x: x[0])
        datelist = []
        METlist = []

        for i in dateMETlist:
            datelist.append(i[0])
            METlist.append(i[1])
        fig, ax = plt.subplots()
        ax.plot(datelist,METlist, marker="o",markersize=10, markeredgecolor="red", markerfacecolor="green")
        plt.grid()
        plt.ylabel("Calories spent")
        plt.xlabel("Date")
        plt.title(title)
        myFmt = DateFormatter("%Y-%m-%d")
        ax.xaxis.set_major_formatter(myFmt)
        plt.xticks(datelist)
        fig.autofmt_xdate()
        # plt.savefig(r"C:\Users\DanielFung\Desktop\fyp\py\fyp\test.jpg")
        fig.canvas.draw()
        plt.clf()
        img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        img  = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        img = cv2.resize(img,(1280, 840))

        # img is rgb, convert to opencv's default bgr
        img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        return img

    def setCamImg(self, imgnp):
        w = int(self.controller.width * 0.9)
        h = self.controller.height
        imgnp = cv2.resize(imgnp, (w, h))
        self.img = Image.fromarray(imgnp)
        self.imgtk = ImageTk.PhotoImage(image=self.img)  #must use same ImageTk object
        self.parent.itemconfig(self.cam, image=self.imgtk, anchor=NW)