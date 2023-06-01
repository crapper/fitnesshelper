import cv2
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
from typing import List

from .counter import *
from .video_get import *
from .model_controller import *
from .sql_connector import *
from .page import *

class CameraPage(Page):
    def __init__(self, parent: tk.Canvas, controller: App):
        Page.__init__(self, parent, controller)
        self.model : ModelController = ModelController()
        w = int(self.controller.width * 0.9)
        h = self.controller.height
        blank = np.full((h, w,3), 0, np.uint8)
        self.img :Image = Image.fromarray(blank)
        self.img_tk: ImageTk.PhotoImage = ImageTk.PhotoImage(image=self.img) 
        self.cam: int = parent.create_image(0,0, image=self.img_tk, anchor=tk.NW)
        self.video_thread: VideoGet = VideoGet(0, 20)
        self.counter_list: List[Counter] = [PushupCounter(), SitupCounter(), SquatCounter()]
        self.db_connector: SQLconnector = SQLconnector()
        self.METlist: List[float] = [3.8, 5.5, 8.0]
        self.offset_non_frame: List[Activity] = []

        self.hide_page()

    def save(self):
        for p in range(len(self.counter_list)):
            if self.counter_list[p].get_count() > 0:
                MET = self.METlist[p] * 3.5 * self.controller.weight / 200 * self.counter_list[p].total_time / 60
                self.db_connector.save(self.counter_list[p].classname, self.counter_list[p].get_count(), self.controller.weight, self.counter_list[p].total_time, MET)

    def show_page(self):
        self.model.set_model(self.controller.model_complexity, self.controller.model_conf, self.controller.track_conf)
        self.active = True
        self.parent.itemconfig(self.cam, state='normal')
        self.start_vid()

    def hide_page(self):
        self.active = False

        self.parent.itemconfig(self.cam, state='hidden')
        self.stop_vid()

    def request_open_page(self):
        if self.active:
            return True

        self.show_page()
        return True

    def request_close_page(self):
        if self.active == False:
            return True

        self.stop_vid()
        msg_box = tk.messagebox.askquestion('Warning', 'Are you save the counting to the database?(all progress will lost if no is selected)',icon='warning')
        if msg_box == 'yes':
            self.save()
        
        self.counter_list = [PushupCounter(), SitupCounter(), SquatCounter()]
        self.offset_non_frame = []
        self.model.reset()

        self.hide_page()
        return True

    def setCamImg(self, img_np: cv2.Mat):
        w = int(self.controller.width * 0.9)
        h = self.controller.height
        img_np = cv2.resize(img_np, (w, h))
        self.img = Image.fromarray(img_np)
        self.img_tk = ImageTk.PhotoImage(image=self.img)  #must use same ImageTk object
        self.parent.itemconfig(self.cam, image=self.img_tk, anchor=tk.NW)


    def start_vid(self):
        self.video_thread.start()

    def stop_vid(self):
        self.video_thread.stop()
        w = int(self.controller.width * 0.9)
        h = self.controller.height
        blank = np.full((h, w,3), 0, np.uint8)
        self.setCamImg(blank)

    def update_frame(self):
        if self.active == False or self.video_thread == None:
            return
        if self.video_thread.stream.isOpened() and len(self.video_thread.grabbed) > 0:
            ret, frame = self.video_thread.grabbed[0], self.video_thread.frame[0]
            
            if not ret:
                return
            
            img = self.model.detect(frame)
            if self.model.prediction != Activity.non:
                self.counter_list[self.model.prediction].update_count(self.model.angle_for_count, time.time())
                self.offset_non_frame.append(self.model.prediction)
            filter_activities_by_frequency(self.counter_list, self.offset_non_frame)

            text = "Pushup: " + str(self.counter_list[0].get_count()) + " Situp: " + str(self.counter_list[1].get_count()) + " Squat: " + str(self.counter_list[2].get_count())
            cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
            self.setCamImg(img)
        else:
            w = int(self.controller.width * 0.9)
            h = self.controller.height
            blank = np.full((h, w,3), 0, np.uint8)
            self.setCamImg(blank)
