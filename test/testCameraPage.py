import unittest
from unittest.mock import MagicMock

from CameraPage import CameraPage

class TestCameraPage(unittest.TestCase):

    def setUp(self):
        self.app = MagicMock()
        self.controller = MagicMock()
        self.controller.width = 800
        self.controller.height = 600
        self.controller.weight = 70
        self.camera_page = CameraPage(self.app, self.controller)

    def test_disableswitch(self):
        # Test that active is set to False and counters are reset when disableswitch is called while active is True
        self.camera_page.active = True
        self.camera_page.counterlist[0].update_count(10, 100) # Add some counts to the PushupCounter
        self.camera_page.disableswitch()
        self.assertFalse(self.camera_page.active)
        self.assertEqual(self.camera_page.counterlist[0].get_count(), 0)

        # Test that active is set to True when disableswitch is called while active is False
        self.camera_page.disableswitch()
        self.assertTrue(self.camera_page.active)

    def test_most_frequent(self):
        # Test that most_frequent returns the correct value for a list with one most frequent value
        lst = [1, 2, 3, 3, 3, 4, 5]
        result = self.camera_page.most_frequent(lst)
        self.assertEqual(result, 3)

        # Test that most_frequent returns the correct value for a list with multiple most frequent values
        lst = [1, 2, 3, 3, 3, 4, 4, 5]
        result = self.camera_page.most_frequent(lst)
        self.assertIn(result, [3, 4])

    def tearDown(self):
        self.camera_page.stopvid() # Stop the video thread

if __name__ == '__main__':
    unittest.main()