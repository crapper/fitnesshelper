import cv2
import time
import threading
import numpy as np
import os

from typing import List
from .types import *
from .counter import *

def most_frequent(activities: List[Activity]):
    return max(set(activities), key = activities.count)

def filter_activities_by_frequency(counters: List[Counter], activities: List[Activity]):
    if len(activities) < 200:
        return
    max_appear = most_frequent(activities)
    setlist = list(set(activities))
    setlist.remove(max_appear)
    for i in setlist:
        if i != Activity.non:
            counters[i].state = ActivityType.NA
            if counters[i].peak_valley_count % 2 == 1:
                counters[i].peak_valley_count -= 1
            counters[i].temp_count_time = 0
    activities.clear()

class VideoGet:
    def __init__(self, src, fps = 30):
        self.fps = fps
        self.src = src
        self.stream = cv2.VideoCapture()
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.grabbed = [True]
        self.frame = [np.full((640, 480,3), 0, np.uint8)]
        self.currentframe = 0
        self.finished = False
        self.total_frame = -1
        self.thread = None

    def start(self):
        self.thread = threading.Thread(target=self.get, daemon = True)
        self.thread.start()
        return self

    def get(self):
        if self.stream.isOpened() == False:
            if self.src != 0:
                self.stream.open(self.src)
                self.stream.set(cv2.CAP_PROP_POS_FRAMES, self.currentframe)
                self.total_frame = int(self.stream.get(cv2.CAP_PROP_FRAME_COUNT)) 
                self.fps_video = self.stream.get(cv2.CAP_PROP_FPS)
            else:
                self.stream.open(0, cv2.CAP_DSHOW)
        while self.stream.isOpened() and not self.finished:
            start_time = time.time()
            if (self.src != 0 and self.currentframe == self.total_frame):
                self.finished = True
            elif len(self.grabbed) < 30 and self.src != 0:
                (grabbed, frame) = self.stream.read()
                self.grabbed.append(grabbed)
                self.frame.append(frame)
                self.currentframe += 1
            elif self.src == 0:
                (grabbed, frame) = self.stream.read()
                self.grabbed[0] = grabbed
                self.frame[0] = frame
                self.currentframe += 1
            time_taken = time.time() - start_time
            sleep_time = float(1/self.fps - time_taken)
            if sleep_time > 0:
                time.sleep(sleep_time)

    def stop(self):
        self.stream.release()
        self.stream = cv2.VideoCapture()
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        #if the os is Windows 
        if os.name == 'nt' and self.thread != None:
            self.thread.join()
