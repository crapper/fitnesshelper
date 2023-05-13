import cv2
import time
import threading

class VideoGet:
    def __init__(self, src, fps = 30):
        self.fps = fps
        self.src = src
        self.stopped = True
        self.stream = cv2.VideoCapture(self.src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        (grabbed, frame) = self.stream.read()
        self.grabbed = []
        self.frame = []
        self.grabbed.append(grabbed)
        self.frame.append(frame)
        self.currentframe = 0
        self.finished = False
        if self.src != 0:
            self.totalframe = int(self.stream.get(cv2.CAP_PROP_FRAME_COUNT)) 
            self.fpsvideo = self.stream.get(cv2.CAP_PROP_FPS)

    def start(self):    
        self.stopped = False
        # print(self.src)
        self.thread = threading.Thread(target=self.get, daemon = True)
        self.thread.start()
        # self.thread.join()
        return self

    def get(self):
        while not self.stopped and not self.finished:
            starttime = time.time()
            if (self.src != 0 and self.currentframe == self.totalframe):
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
            time.sleep(float(1/self.fps - (time.time() - starttime)))

    def stop(self):
        self.stopped = True

    def __del__(self):
        # stop thread
        if self.stopped == False:
            self.stopped = True
            self.thread.join()
        # relase stream
        if self.stream.isOpened():
            self.stream.release()