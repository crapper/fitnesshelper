import sys
import os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

import unittest
from app import *
from pathlib import Path

class TestVideoGet(unittest.TestCase):
    def setUp(self):
        self.video = None
        pass

    def test_get_real_camera(self):
        # check if the environment is github action
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            raise unittest.SkipTest()
        self.video = VideoGet(0, fps=30)
        self.video.start()
        while self.video.stream.isOpened() == False:
            time.sleep(0.1)
        self.assertTrue(self.video.stream.isOpened())
        self.assertTrue(self.video.grabbed[0])
        self.assertIsNotNone(self.video.frame[0])
    
    def test_get_video_file(self):
        # Test that the VideoGet instance is able to keep reading frame after pop the top frame for video source
        path = Path(__file__).parent.parent / "testvideo"/ "testvideo.avi"
        path = path.absolute().as_posix()
        self.video = VideoGet(path, fps=30)
        self.video.start()
        while len(self.video.frame) <= 2:
            time.sleep(0.1)
        self.video.frame.pop(0)
        self.video.grabbed.pop(0)
        while len(self.video.frame) <= 2:
            time.sleep(0.1)
        self.assertGreater(len(self.video.frame), 1)

    def test_get_video_file_til_end(self):
        # Test that the VideoGet instance is able to keep reading frame until the end of the video
        path = Path(__file__).parent.parent / "testvideo" / "testvideo.avi"
        path = path.absolute().as_posix()
        self.video = VideoGet(path, fps=30)
        self.video.start()
        while self.video.stream.isOpened() == False:
            time.sleep(0.1)
        while not self.video.finished or len(self.video.frame) > 0:
            if len(self.video.frame) == 0:
                time.sleep(0.1)
            else:
                self.video.frame.pop(0)
                self.video.grabbed.pop(0)
        self.assertTrue(self.video.finished)

    def test_stop(self):
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            raise unittest.SkipTest()
        # Test that the VideoGet instance is able to stop
        self.video = VideoGet(0, fps=30)
        self.video.start()
        while self.video.stream.isOpened() == False:
            time.sleep(0.1)
        self.video.stop()
        self.assertFalse(self.video.stream.isOpened())

    def test_most_frequent(self):
        Listtest = [Activity.pushup, Activity.pushup, Activity.squat, Activity.situp]
        self.assertEqual(most_frequent(Listtest), Activity.pushup)

    def test_filter_activities_by_frequency(self):
        Counterlist = [PushupCounter(), SitupCounter(), SquatCounter()]
        Listtest = []
        filter_activities_by_frequency(Listtest, Counterlist) # dummy return when len < 200
        for i in range(0, 200):
            Listtest.append(Activity.pushup)
        for i in range(0, 100):
            Listtest.append(Activity.situp)
        for i in range(0, 50):
            Listtest.append(Activity.squat)
        Counterlist[0].temp_count_time = 100
        Counterlist[0].peak_valley_count = 3
        Counterlist[1].temp_count_time = 100
        Counterlist[1].peak_valley_count = 3
        Counterlist[2].temp_count_time = 100
        Counterlist[2].peak_valley_count = 3
        filter_activities_by_frequency(Counterlist, Listtest)
        self.assertEqual(len(Listtest), 0)
        self.assertEqual(Counterlist[0].temp_count_time, 100)
        self.assertEqual(Counterlist[0].peak_valley_count, 3)
        self.assertEqual(Counterlist[1].temp_count_time, 0)
        self.assertEqual(Counterlist[1].peak_valley_count, 2)
        self.assertEqual(Counterlist[2].temp_count_time, 0)
        self.assertEqual(Counterlist[2].peak_valley_count, 2)

    def tearDown(self):
        if self.video is not None:
            del self.video

if __name__ == '__main__':
    unittest.main()
