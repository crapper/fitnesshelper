import sys
import os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

import unittest
import cv2
from app import *

class TestModelController(unittest.TestCase):
    def setUp(self):
        self.mc = ModelController()

    def test_init(self):
        self.assertIsInstance(self.mc.draw, object)
        self.assertIsInstance(self.mc.draw_style, object)
        self.assertIsInstance(self.mc.pose, object)
        self.assertIsInstance(self.mc.model, object)
        self.assertEqual(self.mc.result, [])
        self.assertEqual(self.mc.angle_for_count, -1)
        self.assertEqual(self.mc.prediction, Activity.non)
        self.assertEqual(self.mc.point_side, PointView.front)

    # def test_set_model(self):
    #     self.mc.set_model(2, 0.75, 0.75)
    #     self.assertEqual(self.mc.model.model_complexity, 2)

    def test_angle_cal(self):
        a = [0, 0]
        b = [0, 1]
        c = [1, 0]
        angle = self.mc.angle_cal(a, b, c)
        self.assertAlmostEqual(angle, 45.0)

    def test_side(self):
        Nose = [0, 0, 0, 1]
        L_shoulder = [1, 0, 0, 1]
        R_shoulder = [-1, 0, 0, 1]
        side = self.mc.side(Nose, L_shoulder, R_shoulder)
        self.assertEqual(side, PointView.front)

    def test_predict(self):
        #(TTT), (), ()
        pushup1 = 160
        pushup2 = PointView.down
        situp1 = 79
        situp2 = 121
        squat1 = 76
        squat2 = 44
        prediction = self.mc.predict(pushup1, pushup2, situp1, situp2, squat1, squat2)
        self.assertEqual(prediction, Activity.pushup)

        #(FTF), (TT), ()
        pushup1 = 140
        pushup2 = PointView.up
        situp1 = 79
        situp2 = 121
        squat1 = 76
        squat2 = 44
        prediction = self.mc.predict(pushup1, pushup2, situp1, situp2, squat1, squat2)
        self.assertEqual(prediction, Activity.situp)

        #(FFT), (FF), (TT)
        pushup1 = 140
        pushup2 = PointView.down
        situp1 = 80
        situp2 = 120
        squat1 = 44
        squat2 = 44
        prediction = self.mc.predict(pushup1, pushup2, situp1, situp2, squat1, squat2)
        self.assertEqual(prediction, Activity.squat)

        #(FFF), (FF), (FF)
        pushup1 = 140
        pushup2 = PointView.up
        situp1 = 80
        situp2 = 120
        squat1 = 50
        squat2 = 44
        prediction = self.mc.predict(pushup1, pushup2, situp1, situp2, squat1, squat2)
        self.assertEqual(prediction, Activity.non)

    def test_isOneSideFull(self):
        vis = [1, 1, 1, 1, 1, 1]
        b = self.mc.isOneSideFull(vis)
        self.assertTrue(b)

    def test_face_direction(self):
        p1 = [0, 0]
        p2 = [0, 1]
        direction = self.mc.face_direction(p1, p2)
        self.assertEqual(direction, PointView.down)

    def test_detect(self):
        path1 = os.path.abspath(os.path.join(os.path.dirname(__file__), '../testimg/pushup.jpg'))
        path2 = os.path.abspath(os.path.join(os.path.dirname(__file__), '../testimg/situp.jpg'))
        path3 = os.path.abspath(os.path.join(os.path.dirname(__file__), '../testimg/squat.jpg'))
        frame = cv2.imread(path1)
        self.mc.detect(frame)
        self.assertEqual(self.mc.prediction, Activity.pushup)

        self.mc = ModelController()
        frame = cv2.imread(path2)
        self.mc.detect(frame)
        self.assertEqual(self.mc.prediction, Activity.situp)

        self.mc = ModelController()
        frame = cv2.imread(path3)
        self.mc.detect(frame)
        self.assertEqual(self.mc.prediction, Activity.squat)


    def test_reset(self):
        self.mc.reset()
        self.assertEqual(self.mc.result, [])
        self.assertEqual(self.mc.angle_for_count, -1)
        self.assertEqual(self.mc.prediction, Activity.non)
        self.assertEqual(self.mc.point_side, PointView.front)

if __name__ == '__main__':
    unittest.main()