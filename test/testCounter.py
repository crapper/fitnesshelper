import unittest
from enum_activity import ActivityType
from Counter import Counter, PushupCounter, SitupCounter, SquatCounter

class CounterTest(unittest.TestCase):
    def test_pushup_counter(self):
        pc = PushupCounter()
        self.assertEqual(pc.classname, "pushup")
        pc.update_count(90, 0)
        pc.update_count(140, 1)
        pc.update_count(90, 2)
        pc.update_count(140, 3)
        self.assertEqual(pc.get_count(), 1)

    def test_situp_counter(self):
        sc = SitupCounter()
        self.assertEqual(sc.classname, "situp")
        sc.update_count(100, 0)
        sc.update_count(60, 1)
        sc.update_count(100, 2)
        sc.update_count(60, 3)
        self.assertEqual(sc.get_count(), 1)

    def test_squat_counter(self):
        sqc = SquatCounter()
        self.assertEqual(sqc.classname, "squat")
        sqc.update_count(70, 0)
        sqc.update_count(40, 1)
        sqc.update_count(70, 2)
        sqc.update_count(40, 3)
        self.assertEqual(sqc.get_count(), 1)

if __name__ == '__main__':
    unittest.main()
