import cv2
import time
import threading
import numpy as np

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

    def start(self):
        self.thread = threading.Thread(target=self.get, daemon = True)
        self.thread.start()
        return self

    def get(self):
        if self.stream.isOpened() == False:
            if self.src != 0:
                self.stream.open(self.src)
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

    def __del__(self):
        # stop thread
        if self.stream.isOpened() == False:
            self.thread.join()
        # release stream
        if self.stream.isOpened():
            self.stream.release()