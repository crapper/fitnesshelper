import cv2
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

from .sql_connector import *
from .page import *


class StatisticPage(Page):
    def __init__(self, parent: tk.Canvas, controller):
        Page.__init__(self, parent)
        self.controller = controller
        self.active = False
        w = int(self.controller.width * 0.9)
        h = self.controller.height
        blank = np.full((h, w,3), 255, np.uint8)
        self.img = Image.fromarray(blank)
        self.img_tk = ImageTk.PhotoImage(image=self.img) 
        self.cam = parent.create_image(0,0, image=self.img_tk, anchor=tk.NW)
        self.db_connector = SQLconnector()
        self.start_date = ""
        self.end_date = ""
        self.plot_graph_list = []
        self.state = 0
        self.left_btn = tk.Button(self.controller, text="<", command=lambda: self.change_state(-1))
        self.left_btn.place(x=0, y=h/2)
        self.right_btn = tk.Button(self.controller, text=">", command=lambda: self.change_state(1))
        self.right_btn.place(x=0, y=h/2+100)
        self.left_btn.place_forget()
        self.right_btn.place_forget()
        
    def change_state(self, state):
        self.state = (self.state + state) % 4
        self.setCamImg(self.plot_graph_list[self.state])

    def disable_switch(self):
        if self.active == True:
            self.active = False
            self.start_date = ""
            self.end_date = ""
            self.state = 0
            self.plot_graph_list = []
            self.left_btn.place_forget()
            self.right_btn.place_forget()
            w = int(self.controller.width * 0.9)
            h = self.controller.height
            blank = np.full((h, w,3), 255, np.uint8)
            self.setCamImg(blank)
        else:
            dt = datetime.datetime.strptime(self.start_date, '%d-%m-%Y').date()
            dt2 = datetime.datetime.strptime(self.end_date, '%d-%m-%Y').date()
            if dt > dt2:
                tk.messagebox.showinfo('Warning', 'End date must be later than start date')
                self.start_date = ""
                self.end_date = ""
            else:
                self.left_btn.place(x=0, y=self.controller.height/2)
                self.right_btn.place(x=0, y=self.controller.height/2+100)
                self.active = True
                self.parent.tag_raise(self.cam, 'all')
                self.plot_graph_list.append(self.list_to_img(self.db_connector.extract_calories_list(self.start_date, self.end_date), "Calories Trend for all activities"))
                self.plot_graph_list.append(self.list_to_img(self.db_connector.extract_calories_list(self.start_date, self.end_date, "pushup"), "Calories Trend for pushup"))
                self.plot_graph_list.append(self.list_to_img(self.db_connector.extract_calories_list(self.start_date, self.end_date, "situp"), "Calories Trend for situp"))
                self.plot_graph_list.append(self.list_to_img(self.db_connector.extract_calories_list(self.start_date, self.end_date, "squat"), "Calories Trend for squat"))
                self.setCamImg(self.plot_graph_list[self.state])
                
    def list_to_img(self, lst, title="Calories Trend"):
        dateMETlist = []
        for k in lst:
            date_string = k[1]
            dt = datetime.datetime.strptime(date_string, '%d-%m-%Y')
            temp_found = False
            for i in range(len(dateMETlist)):
                if dt == dateMETlist[i][0]:
                    dateMETlist[i][1] += k[5]
                    temp_found = True
                    break
            if temp_found == False:
                dateMETlist.append([dt, k[5]])

        dateMETlist.sort(key=lambda x: x[0])
        date_list = []
        METlist = []

        for i in dateMETlist:
            date_list.append(i[0])
            METlist.append(i[1])
        fig, ax = plt.subplots()
        ax.plot(date_list,METlist, marker="o",markersize=10, markeredgecolor="red", markerfacecolor="green")
        plt.grid()
        plt.ylabel("Calories spent")
        plt.xlabel("Date")
        plt.title(title)
        myFmt = DateFormatter("%Y-%m-%d")
        ax.xaxis.set_major_formatter(myFmt)
        plt.xticks(date_list)
        fig.autofmt_xdate()
        fig.canvas.draw()
        plt.clf()
        img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        img  = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        img = cv2.resize(img,(1280, 840))

        # img is rgb, convert to opencv's default bgr
        img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        return img

    def setCamImg(self, img_np):
        w = int(self.controller.width * 0.9)
        h = self.controller.height
        img_np = cv2.resize(img_np, (w, h))
        self.img = Image.fromarray(img_np)
        self.img_tk = ImageTk.PhotoImage(image=self.img)  #must use same ImageTk object
        self.parent.itemconfig(self.cam, image=self.img_tk, anchor=tk.NW)