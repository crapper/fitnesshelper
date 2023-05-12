import tkinter as tk
from tkinter import *
import numpy as np
from PIL import Image, ImageTk


class BarPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.startx = int(self.controller.width * 0.9)
        w = int(self.controller.width * 0.1)
        h = self.controller.height
        blank = np.full((h, w,3), 80, np.uint8)
        self.img = Image.fromarray(blank)
        self.imgtk = ImageTk.PhotoImage(image=self.img) 
        self.bar = parent.create_image(self.startx,0, image=self.imgtk, anchor=NW)
        buttonlen = 64
        self.pixel = PhotoImage(width=1, height=1)
        self.btn1 = Button(self.controller, image=self.pixel, width=64, height=64, command=lambda: self.controller.switchCameraPage(), state=NORMAL)
        self.btn1.place(x= self.startx+buttonlen/2, y=buttonlen)
        self.btn2 = Button(self.controller, image=self.pixel, width=64, height=64, command=lambda: self.controller.switchVideoPage(), state=NORMAL)
        self.btn2.place(x= self.startx+buttonlen/2, y=buttonlen*3)
        self.btn3 = Button(self.controller, image=self.pixel, width=64, height=64, command=lambda: self.controller.switchConfigPage(), state=NORMAL)
        self.btn3.place(x= self.startx+buttonlen/2, y=buttonlen*5)
        self.btn4 = Button(self.controller, image=self.pixel, width=64, height=64, command=lambda: self.controller.switchStatisticPage(), state=NORMAL)
        self.btn4.place(x= self.startx+buttonlen/2, y=buttonlen*7)