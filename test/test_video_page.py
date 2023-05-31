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

class TestVideoPage(unittest.TestCase):
    def setUp(self):
        global root
        self.c = tk.Canvas(root)
        self.video_page = VideoPage(self.c, root)

    def tearDown(self):
        self.video_page.hide_page()
        self.video_page.reset()
        del self.video_page
        pass

    def test_show_page(self):
        self.assertFalse(self.video_page.active)
        self.video_page.show_page()
        self.assertTrue(self.video_page.active)

    def test_hide_page(self):
        self.video_page.show_page()
        self.assertTrue(self.video_page.active)
        self.video_page.hide_page()
        self.assertFalse(self.video_page.active)

    def test_request_open_page(self):
        self.assertFalse(self.video_page.active)
        self.video_page.request_open_page()
        self.assertTrue(self.video_page.active)
        self.assertTrue(self.video_page.request_open_page())
    
    def test_request_close_page(self):
        def mock_askquestion(title, message, **options):
            return 'yes'
        self.video_page.show_page()
        self.assertTrue(self.video_page.active)
        with patch.object(mb, 'askquestion', side_effect=mock_askquestion):
            self.video_page.request_close_page()
        self.assertFalse(self.video_page.active)
        with patch.object(mb, 'askquestion', side_effect=mock_askquestion):
            self.assertTrue(self.video_page.request_close_page())

    def test_start_video(self):
        def mock_askquestion(title, message, **options):
            return 'no'
        self.video_page.show_page()
        self.assertIsNone(self.video_page.video_thread)
        path = Path(__file__).parent.parent / "testvideo"/ "pushup5.mp4"
        path = path.absolute().as_posix()
        self.video_page.start_vid(path)
        self.assertIsInstance(self.video_page.video_thread, VideoGet) # test on start video
        with patch.object(mb, 'askquestion', side_effect=mock_askquestion): # test on restart video
            self.assertFalse(self.video_page.request_close_page())

    def test_update_frame(self):
        self.video_page.update_frame() # test on no video and not active
        self.video_page.show_page()
        path = Path(__file__).parent.parent / "testvideo"/ "pushup5.mp4"
        path = path.absolute().as_posix()
        self.video_page.start_vid(path)
        while len(self.video_page.video_thread.frame) < 2: # wait until got frame come in
            time.sleep(0.1)
        while self.video_page.model.prediction == Activity.non: # wait until model predict pushup
            if len(self.video_page.video_thread.frame) == 0:
                time.sleep(0.1)
            else:
                self.video_page.update_frame()
        self.assertEqual(self.video_page.model.prediction, Activity.pushup)

        while len(self.video_page.video_thread.frame) < 2: # wait until got frame come in
            time.sleep(0.1)
        self.video_page.video_thread.grabbed[0] = False
        self.video_page.update_frame() # ret is False, should not update frame and return directly
        
        self.video_page.stop_vid()

    def test_trigger_save_btn(self):
        self.video_page.show_page()
        path = Path(__file__).parent.parent / "testvideo"/ "pushup5.mp4"
        path = path.absolute().as_posix()
        self.video_page.start_vid(path)
        self.video_page.stop_vid()
        self.video_page.video_thread.finished = True
        self.video_page.update_frame()
        self.assertEqual(self.video_page.save_btn['state'], 'normal')

    def test_save(self):
        if os.path.exists(self.video_page.db_connector.db_path):
            os.remove(self.video_page.db_connector.db_path)
        date = '2020-11-11'
        classname = 'pushup'
        time = 100
        fps = 10
        count = 10
        root.weight = 40
        MET = 3.8 * 3.5 * root.weight / 200 * time / fps / 60
        
        self.video_page.date = date
        self.video_page.show_page()
        self.video_page.counter_list[0].peak_valley_count = 10
        self.video_page.counter_list[0].total_time = time
        self.video_page.video_thread = VideoGet(0)
        self.video_page.video_thread.fps_video = 10
        self.video_page.save()
        self.assertEqual(self.video_page.counter_list[0].peak_valley_count, 0)
        self.assertEqual(self.video_page.counter_list[0].total_time, 0)


        con = sqlite3.connect(self.video_page.db_connector.db_path)
        cur = con.cursor()
        res = cur.execute("SELECT * FROM counting where class = ? and date = ?", (classname, date))
        list_return = res.fetchall()
        self.assertEqual(len(list_return), 1)
        row = list_return[0]
        self.assertEqual(row[0], classname)
        self.assertEqual(row[1], date)
        self.assertEqual(row[2], count/2)
        self.assertEqual(row[3], root.weight)
        self.assertEqual(row[4], time / fps)
        self.assertEqual(row[5], MET)
        
    

if __name__ == '__main__':
    unittest.main()
    