import unittest
from ...script.VideoGet import VideoGet

class TestVideoGet(unittest.TestCase):
    def setUp(self):
        self.video_get = VideoGet(0, 30)
        self.video_get.start()
        print("setup")

    def test_video_stream(self):
        # Test that video stream is running and frames are being captured
        self.assertTrue(self.video_get.stream.isOpened())
        self.assertTrue(len(self.video_get.grabbed) > 0)
        self.assertTrue(len(self.video_get.frame) > 0)
        

    def test_stop_video_stream(self):
        # Test that video stream can be stopped
        self.video_get.stop()
        self.assertTrue(self.video_get.stopped)
        

    def test_video_frame_size(self):
        # Test that video frames have correct width and height
        self.assertEqual(self.video_get.frame[0].shape[:2], (480, 640))

    def tearDown(self):
        self.video_get.stop()
        self.video_get.stream.release()
        del self.video_get


if __name__ == '__main__':
    unittest.main()
