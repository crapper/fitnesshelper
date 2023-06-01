import sys
import os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

import unittest
from unittest.mock import patch
import tkinter as tk
from app import *
import tkinter.messagebox as mb
import sqlite3
from test_setup import root

class TestCameraPage(unittest.TestCase):
    def setUp(self):
        global root
        self.c = tk.Canvas(root)
        self.camera_page = CameraPage(self.c, root)

    def tearDown(self):
        self.camera_page.hide_page()
        del self.camera_page
        pass

    def test_show_page(self):
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            raise unittest.SkipTest()
        self.assertFalse(self.camera_page.active)
        self.camera_page.show_page()
        self.assertTrue(self.camera_page.active)

    def test_hide_page(self):
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            raise unittest.SkipTest()
        self.camera_page.show_page()
        self.assertTrue(self.camera_page.active)
        self.camera_page.hide_page()
        self.assertFalse(self.camera_page.active)

    def test_request_open_page(self):
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            raise unittest.SkipTest()
        self.assertFalse(self.camera_page.active)
        self.camera_page.request_open_page()
        self.assertTrue(self.camera_page.active)
        self.assertTrue(self.camera_page.request_open_page())
    
    def test_request_close_page(self):
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            raise unittest.SkipTest()
        def mock_askquestion(title, message, **options):
            return 'yes'
        self.camera_page.show_page()
        self.assertTrue(self.camera_page.active)
        with patch.object(mb, 'askquestion', side_effect=mock_askquestion):
            self.camera_page.request_close_page()
        self.assertFalse(self.camera_page.active)
        with patch.object(mb, 'askquestion', side_effect=mock_askquestion):
            self.assertTrue(self.camera_page.request_close_page())

    def test_save(self):
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            raise unittest.SkipTest()
        if os.path.exists(self.camera_page.db_connector.db_path):
            os.remove(self.camera_page.db_connector.db_path)
        date = datetime.datetime.now().date().strftime('%Y-%m-%d')
        classname = 'pushup'
        time = 100
        count = 10
        root.weight = 40
        MET = 3.8 * 3.5 * root.weight / 200 * time / 60

        self.camera_page.show_page()
        self.camera_page.counter_list[0].peak_valley_count = 10
        self.camera_page.counter_list[0].total_time = time
        self.camera_page.save()

        con = sqlite3.connect(self.camera_page.db_connector.db_path)
        cur = con.cursor()
        res = cur.execute("SELECT * FROM counting where class = ? and date = ?", (classname, date))
        list_return = res.fetchall()
        self.assertEqual(len(list_return), 1)
        row = list_return[0]
        self.assertEqual(row[0], classname)
        self.assertEqual(row[1], date)
        self.assertEqual(row[2], count/2)
        self.assertEqual(row[3], root.weight)
        self.assertEqual(row[4], time)
        self.assertEqual(row[5], MET)
    
    def test_update_frame(self):
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            raise unittest.SkipTest()
        class MockVideoGet(VideoGet):
            def __init__(self, src=0, fps=30):
                super().__init__(src, fps)

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
                    if (self.currentframe == self.total_frame):
                        self.finished = True
                    else:
                        (grabbed, frame) = self.stream.read()
                        self.grabbed[0] = grabbed
                        self.frame[0] = frame
                        self.currentframe += 1
                    time_taken = time.time() - start_time
                    sleep_time = float(1/self.fps - time_taken)
                    if sleep_time > 0:
                        time.sleep(sleep_time)

        self.camera_page.update_frame() # not active, return directly
        path = Path(__file__).parent.parent / "testvideo"/ "pushup5.mp4"
        path = path.absolute().as_posix()
        self.camera_page.video_thread = MockVideoGet(path, 20) #mock as real camera
        self.camera_page.show_page()
        self.camera_page.stop_vid()
        while self.camera_page.video_thread.stream.isOpened():
            time.sleep(0.1)
        self.camera_page.update_frame() # blank the screen area
        self.assertEqual(len(self.camera_page.offset_non_frame), 0)
        self.camera_page.video_thread.grabbed[0] = False
        self.camera_page.start_vid()
        while not self.camera_page.video_thread.stream.isOpened():
            time.sleep(0.1)
        self.camera_page.update_frame() # not ret return directly
        self.camera_page.video_thread.grabbed[0] = True
        frame = 0
        while frame < 10:
            self.camera_page.update_frame()
            frame += 1
        self.assertGreater(len(self.camera_page.offset_non_frame), 0)

if __name__ == '__main__':
    unittest.main()
    