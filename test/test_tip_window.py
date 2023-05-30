import sys
import os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

import unittest
from app import *

class TestTipWindow(unittest.TestCase):
    def setUp(self):
        self.tip_window = TipWindow(tk.Button())

    def tearDown(self):
        pass

    def test_tip_window(self):
        self.tip_window.showtip("test")
        self.assertEqual(self.tip_window.text, "test")
        self.assertIsNotNone(self.tip_window.tipwindow)
        self.tip_window.showtip("") # dummy for just return, for coverage
        self.tip_window.hidetip()
        self.assertIsNone(self.tip_window.tipwindow)

if __name__ == '__main__':
    unittest.main()