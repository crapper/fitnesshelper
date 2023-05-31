import sys
import os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

import unittest
from app import *

class TestVideoGet(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_real_camera(self):
        # Test that the VideoGet instance is able to get frames
        self.video = VideoGet(0, fps=30)
        self.video.start()
        while self.video.stream.isOpened() == False:
            time.sleep(0.01)
        self.assertTrue(self.video.stream.isOpened())
        self.assertTrue(self.video.grabbed[0])
        self.assertIsNotNone(self.video.frame[0])
    
    def test_get_video_file(self):
        # Test that the VideoGet instance is able to keep reading frame after pop the top frame for video source
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../testvideo/pushup5.mp4'))
        self.video = VideoGet(path, fps=30)
        self.video.start()
        while len(self.video.frame) < 30:
            time.sleep(0.01)
        self.video.frame.pop(0)
        self.video.grabbed.pop(0)
        while len(self.video.frame) < 30:
            time.sleep(0.01)
        self.assertEqual(len(self.video.frame), 30)

    def test_get_video_file2(self):
        # Test that the VideoGet instance is able to keep reading frame until the end of the video
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../testvideo/testvideo.avi'))
        self.video = VideoGet(path, fps=30)
        self.video.start()
        while self.video.stream.isOpened() == False:
            time.sleep(0.01)
        while not self.video.finished or len(self.video.frame) > 0:
            if len(self.video.frame) == 0:
                time.sleep(0.01)
            else:
                self.video.frame.pop(0)
                self.video.grabbed.pop(0)
        self.assertTrue(self.video.finished)

    def test_stop(self):
        # Test that the VideoGet instance is able to stop
        self.video = VideoGet(0, fps=30)
        self.video.start()
        while self.video.stream.isOpened() == False:
            time.sleep(0.01)
        self.video.stop()
        self.assertFalse(self.video.stream.isOpened())

    def tearDown(self):
        del self.video


if __name__ == '__main__':
    unittest.main()
