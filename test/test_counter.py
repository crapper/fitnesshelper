import sys
import os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

import unittest
from app import *


class TestCounter(unittest.TestCase):
    def test_pushup_counter(self):
        pc = PushupCounter()
        self.assertEqual(pc.classname, "pushup")
        self.assertTrue(pc.isDown(100))
        self.assertFalse(pc.isDown(140))
        self.assertTrue(pc.isUp(140))
        self.assertFalse(pc.isUp(100))
        pc.update_count(90, 0)
        pc.update_count(140, 1)
        pc.update_count(90, 2)
        pc.update_count(140, 3)
        self.assertEqual(pc.get_count(), 1)

    def test_situp_counter(self):
        sc = SitupCounter()
        self.assertEqual(sc.classname, "situp")
        self.assertTrue(sc.isDown(90))
        self.assertFalse(sc.isDown(60))
        self.assertTrue(sc.isUp(60))
        self.assertFalse(sc.isUp(90))
        sc.update_count(100, 0)
        sc.update_count(60, 1)
        sc.update_count(100, 2)
        sc.update_count(60, 3)
        self.assertEqual(sc.get_count(), 1)

    def test_squat_counter(self):
        sqc = SquatCounter()
        self.assertEqual(sqc.classname, "squat")
        self.assertTrue(sqc.isDown(70))
        self.assertFalse(sqc.isDown(40))
        self.assertTrue(sqc.isUp(40))
        self.assertFalse(sqc.isUp(70))
        sqc.update_count(70, 0)
        sqc.update_count(40, 1)
        sqc.update_count(70, 2)
        sqc.update_count(40, 3)
        self.assertEqual(sqc.get_count(), 1)

if __name__ == '__main__':
    unittest.main()
