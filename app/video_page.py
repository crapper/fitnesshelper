import cv2
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
from typing import Optional

from .model_controller import *
from .video_get import *
from .sql_connector import *
from .counter import *
from .page import *

class VideoPage(Page):
    def __init__(self, parent: tk.Canvas, controller: App):
        Page.__init__(self, parent, controller)
        self.model = ModelController()
        self.panel = []
        self.BgTop_x = 688
        self.BgTop_y = 188
        self.BgDown_x = 1088
        self.BgDown_y = 488
        self.shape_tri_pointer={'bounds': [1152, 224, self.BgDown_x, 192, self.BgDown_x, 256], 'kind': 'tri', 'fill': True}
        self.panel.append(self.parent.create_polygon(list(self.shape_tri_pointer.values())[0],fill='white',outline='green', width = 5))#[0] : widget background panel triangle
        self.panel.append(self.parent.create_rectangle(self.BgTop_x, self.BgTop_y,self.BgDown_x,self.BgDown_y,fill='white',outline='green', width = 5)) #[1] : widget background panel rectangle
        self.db_connector = SQLconnector()
        self.METlist = [3.8, 5.5, 8.0]
        blank = np.full((int((self.BgDown_y-self.BgTop_y)*0.8/2), int((self.BgDown_x-self.BgTop_x)*0.8),3), 0, np.uint8)
        self.img = Image.fromarray(blank)
        self.img_tk = ImageTk.PhotoImage(image=self.img) 
        self.cam = self.parent.create_image(self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1),self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1), image=self.img_tk, anchor=tk.NW)
        self.panel.append(self.cam) #[2] : widget camera image
        self.panel.append(self.parent.create_rectangle(self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1),
        ( self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1) + int((self.BgDown_y-self.BgTop_y)*0.8/2) ),
        self.BgDown_x-int((self.BgDown_x-self.BgTop_x)*0.1),
        ( self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1) + int((self.BgDown_y-self.BgTop_y)*0.8/2) +int((self.BgDown_y-self.BgTop_y)*0.05) ),
        fill='gray',outline='black')) #[3] : widget progress bar border

        self.bar_fill = self.parent.create_rectangle( self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1)+1,
         ( self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1) + int((self.BgDown_y-self.BgTop_y)*0.8/2) ) +1,
          self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1)-1,
          ( self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1) + int((self.BgDown_y-self.BgTop_y)*0.8/2) +int((self.BgDown_y-self.BgTop_y)*0.05)),
          fill='green') #final x = self.BgDown_x-11

        self.total = int((self.BgDown_x-self.BgTop_x)*0.8)-2
        self.initial_x = self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1)+1
        self.panel.append(self.bar_fill) #[4] : widget progress bar fill, total 378 pixels

        self.counter_list = [PushupCounter(), SquatCounter(), SitupCounter()]
        self.panel.append(self.parent.create_text(self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1), ( self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1) + int((self.BgDown_y-self.BgTop_y)*0.8/2) +int((self.BgDown_y-self.BgTop_y)*0.05) ), text="Pushup: "+str(self.counter_list[Activity.pushup].get_count()), font=("Helvetica", 16), fill="black", anchor=tk.NW)) #[5] : widget text pushup counter
        self.panel.append(self.parent.create_text(self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1) , ( self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1) + int((self.BgDown_y-self.BgTop_y)*0.8/2) +int((self.BgDown_y-self.BgTop_y)*0.05) )+16+16, text="Situp: "+str(self.counter_list[Activity.pushup].get_count()), font=("Helvetica", 16), fill="black", anchor=tk.NW)) #[6] : widget text situp counter
        self.panel.append(self.parent.create_text(self.BgTop_x+int((self.BgDown_x-self.BgTop_x)*0.1) , ( self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1) + int((self.BgDown_y-self.BgTop_y)*0.8/2) +int((self.BgDown_y-self.BgTop_y)*0.05) )+16+16+16+16, text="Squat: "+str(self.counter_list[Activity.pushup].get_count()), font=("Helvetica", 16), fill="black", anchor=tk.NW)) #[7] : widget text squat counter
        self.pixel = tk.PhotoImage(width=1, height=1)
        self.save_btn = tk.Button(self.controller, image=self.pixel, text="Save", state='disable', width=int((self.BgDown_x-self.BgTop_x)*0.2), height =int((self.BgDown_y-self.BgTop_y)*0.1), compound='c', command=lambda: self.save())
        self.save_btn.place(x= self.BgDown_x - int((self.BgDown_x-self.BgTop_x)*0.3), y = ( self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1) + int((self.BgDown_y-self.BgTop_y)*0.8/2) +int((self.BgDown_y-self.BgTop_y)*0.1) )+16+16)
        self.save_btn.place_forget()
        self.date = ""
        self.video_thread = None
        self.frame_read = 0
        self.offset_non_frame = []

        self.hide_page()

    def save(self):
        for p in range(len(self.counter_list)):
            if self.counter_list[p].get_count() > 0:
                MET = self.METlist[p] * 3.5 * self.controller.weight / 200 * (self.counter_list[p].total_time/self.video_thread.fps_video/ 60)
                self.db_connector.save(self.counter_list[p].classname, self.counter_list[p].get_count(), self.controller.weight, self.counter_list[p].total_time/self.video_thread.fps_video, MET)
        self.stop_vid()
        self.hide_page()

    def video_stopped(self):
        if self.video_thread != None:
            return self.video_thread.stopped
        else:
            return True

    def setCamImg(self, img_np: cv2.Mat):
        w = int((self.BgDown_x-self.BgTop_x)*0.8)
        h = int((self.BgDown_y-self.BgTop_y)*0.8/2)
        img_np = cv2.resize(img_np, (w, h))
        self.img = Image.fromarray(img_np)
        self.img_tk = ImageTk.PhotoImage(image=self.img)  #must use same ImageTk object
        self.parent.itemconfig(self.cam, image=self.img_tk, anchor=tk.NW)

    def update_count(self):
        self.parent.itemconfig(self.panel[5], text="Pushup: "+str(self.counter_list[Activity.pushup].get_count()))
        self.parent.itemconfig(self.panel[6], text="Situp: "+str(self.counter_list[Activity.situp].get_count()))
        self.parent.itemconfig(self.panel[7], text="Squat: "+str(self.counter_list[Activity.squat].get_count()))

    def start_vid(self, source: Optional[str] = None):
        if self.video_thread != None:
            self.video_thread.start()
        elif source != None:
            self.video_thread = VideoGet(source, 25)
            self.video_thread.start()

    def stop_vid(self):
        if self.video_thread != None:
            self.video_thread.stop()
        w = int((self.BgDown_x-self.BgTop_x)*0.8)
        h = int((self.BgDown_y-self.BgTop_y)*0.8/2)
        blank = np.full((h, w,3), 0, np.uint8)
        self.setCamImg(blank)
    
    def reset(self):
        self.stop_vid()
        self.date = ""
        self.save_btn["state"] = "disable"
        self.save_btn.place_forget()
        self.counter_list = [PushupCounter(), SitupCounter(), SquatCounter()]
        self.db_connector = SQLconnector()
        if self.video_thread != None:
            self.video_thread = None
        self.frame_read = 0
        x0, y0, x1, y1 = self.parent.coords(self.bar_fill)
        self.parent.coords(self.bar_fill, self.initial_x, y0, self.initial_x, y1)
        for item in self.panel:
            self.parent.itemconfig(item, state='hidden')
        self.model.reset()
        self.offset_non_frame = []

    def show_page(self):
        self.model.set_model(self.controller.model_complexity, self.controller.model_conf, self.controller.track_conf)
        self.active = True
        self.db_connector.date = self.date
        for item in self.panel:
            self.parent.itemconfig(item, state='normal')
            self.parent.tag_raise(item, 'all')
        self.save_btn.place(x= self.BgDown_x - int((self.BgDown_x-self.BgTop_x)*0.3), y = ( self.BgTop_y+int((self.BgDown_y-self.BgTop_y)*0.1) + int((self.BgDown_y-self.BgTop_y)*0.8/2) +int((self.BgDown_y-self.BgTop_y)*0.1) )+16+16)
        

    def hide_page(self):
        self.active = False

        self.reset()

    def request_open_page(self):
        if self.active:
            return True

        self.show_page()
        return True

    def request_close_page(self):
        if self.active == False:
            return True

        self.stop_vid()
        msg_box = tk.messagebox.askquestion('Warning', 'Are you sure you want to terminate the process?(all progress will lost)',icon='warning')
        if msg_box == 'yes':
            self.hide_page()
            return True
        else:
            self.start_vid()
            self.update_frame()
            return False

    def most_frequent(self, List):
        return max(set(List), key = List.count)

    def update_frame(self):
        if self.active == False or self.video_thread == None:
            return
        if self.video_thread.stream.isOpened() and self.frame_read != self.video_thread.total_frame+1:
            if len(self.video_thread.frame) != 0:
                ret, frame = self.video_thread.grabbed.pop(0), self.video_thread.frame.pop(0)
                self.frame_read += 1
                if ret:
                    img = self.model.detect(frame)
                    print(self.model.prediction)
                    if self.model.prediction != Activity.non:
                        self.counter_list[self.model.prediction].update_count(self.model.angle_for_count, self.frame_read)
                        self.update_count()
                    self.offset_non_frame.append(self.model.prediction)
                    if len(self.offset_non_frame) >= 100:
                        max_appear = self.most_frequent(self.offset_non_frame)
                        setlist = list(set(self.offset_non_frame))
                        setlist.remove(max_appear)
                        for i in setlist:
                            if i != Activity.non:
                                self.counter_list[i].state = ActivityType.NA
                                if self.counter_list[i].peak_valley_count % 2 == 1:
                                    self.counter_list[i].peak_valley_count -= 1
                                self.counter_list[i].temp_count_time = 0
                        self.offset_non_frame = []
                    self.setCamImg(img)
                    x0, y0, x1, y1 = self.parent.coords(self.bar_fill)
                    x1 = self.initial_x + int(self.total * self.frame_read/self.video_thread.total_frame)
                    self.parent.coords(self.bar_fill, x0, y0, x1, y1)
        else:
            w = int((self.BgDown_x-self.BgTop_x)*0.8)
            h = int((self.BgDown_y-self.BgTop_y)*0.8/2)
            blank = np.full((h, w,3), 0, np.uint8)
            self.setCamImg(blank)
            if self.video_thread.finished:
                self.save_btn["state"] = "normal"
