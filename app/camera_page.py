import cv2
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk

from .counter import *
from .video_get import *
from .model_controller import *
from .sql_connector import *
from .page import *

class CameraPage(Page):
    def __init__(self, parent: tk.Canvas, controller: App):
        Page.__init__(self, parent, controller)
        self.model = ModelController()
        w = int(self.controller.width * 0.9)
        h = self.controller.height
        blank = np.full((h, w,3), 0, np.uint8)
        self.img = Image.fromarray(blank)
        self.img_tk = ImageTk.PhotoImage(image=self.img) 
        self.cam = parent.create_image(0,0, image=self.img_tk, anchor=tk.NW)
        self.video_thread = VideoGet(0, 20)
        self.counter_list = [PushupCounter(), SitupCounter(), SquatCounter()]
        self.db_connector = SQLconnector()
        self.counter_list[0].peak_valley_count = 10
        self.counter_list[0].total_time = 100
        self.offset_non_frame = []

        self.hide_page()

    def show_page(self):
        self.active = True
        self.model.model_complexity = self.controller.model_complexity
        self.parent.itemconfig(self.cam, state='normal')
        self.start_vid()

    def hide_page(self):
        self.active = False

        self.parent.itemconfig(self.cam, state='hidden')

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
            for p in range(len(self.counter_list)):
                if self.counter_list[p].get_count() > 0:
                    MET = 3.8 * 3.5 * self.controller.weight / 200 * self.counter_list[p].total_time / 60
                    self.db_connector.save(self.counter_list[p].classname, self.counter_list[p].get_count(), self.controller.weight, self.counter_list[p].total_time, MET)
        
        self.counter_list = [PushupCounter(), SitupCounter(), SquatCounter()]
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

    def video_stopped(self):
        return self.video_thread.stopped

    def start_vid(self):
        self.video_thread.start()

    def stop_vid(self):
        self.video_thread.stop()
        w = int(self.controller.width * 0.9)
        h = self.controller.height
        blank = np.full((h, w,3), 0, np.uint8)
        self.setCamImg(blank)
    
    def most_frequent(self, List):
        return max(set(List), key = List.count)

    def update_frame(self):
        if self.active == False or self.video_thread == None:
            return
        if self.video_thread.stream.isOpened() and len(self.video_thread.grabbed) > 0:
            ret, frame = self.video_thread.grabbed[0], self.video_thread.frame[0]
            if ret:
                img = self.model.detect(frame)
                if self.model.prediction != Activity.non:
                    self.counter_list[self.model.prediction].update_count(self.model.angle_for_count, time.time())
                self.offset_non_frame.append(self.model.prediction)
                if len(self.offset_non_frame) >= 10:
                    max_appear = self.most_frequent(self.offset_non_frame)
                    setlist = list(set(self.offset_non_frame))
                    setlist.remove(max_appear)
                    for i in setlist:
                        if i != Activity.non:
                            self.counter_list[i].state = ActivityType.NA
                            if self.counter_list[i].peak_valley_count % 2 == 1:
                                self.counter_list[i].peak_valley_count -= 1
                            self.counter_list[i].temp_count_time = 0
                text = "Pushup: " + str(self.counter_list[0].get_count()) + " Situp: " + str(self.counter_list[1].get_count()) + " Squat: " + str(self.counter_list[2].get_count())
                cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)
                self.setCamImg(img)
        else:
            w = int(self.controller.width * 0.9)
            h = self.controller.height
            blank = np.full((h, w,3), 0, np.uint8)
            self.setCamImg(blank)
