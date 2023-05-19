import cv2
import mediapipe as md
import numpy as np
import math

from .types import *


class ModelController:
    def __init__(self):
        self.draw = md.solutions.drawing_utils
        self.draw_style = md.solutions.drawing_styles
        self.pose = md.solutions.pose
        self.model = self.pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5, model_complexity = 1)
        self.result = []
        self.angle_for_count = -1
        self.prediction = Activity.non
        self.point_side = PointView.front

    def init_frame(self):
        self.result = []
        self.angle_for_count = -1
        self.prediction = Activity.non
        self.point_side = PointView.front

    def angle_cal(self, a,b,c):
        a = np.array(a, int) # First
        b = np.array(b, int) # Mid
        c = np.array(c, int) # End

        angle = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
        if angle < 0:
            angle += 360
        if angle > 180:
            angle = 360 - angle
        return angle

    def side(self, Nose, L_shoulder, R_shoulder):
        front = self.angle_cal(L_shoulder, Nose, R_shoulder)
        if front >= 60:
            return PointView.front
        if L_shoulder[2] <= R_shoulder[2]:
            return PointView.left
        else:
            return PointView.right

    def predict(self, pushup1, pushup2, situp1, situp2, squat1, squat2):
        prediction = Activity.non
        if pushup1 >=160 and squat1 >75 and pushup2 == PointView.down:
            prediction = Activity.pushup
        elif situp1 < 80 and situp2 > 120:
            prediction = Activity.situp
        elif squat1 <= 45 and squat2 <= 45:
            prediction = Activity.squat
        return prediction

    def isOneSideFull(self, vis):
        b = True
        for i in vis:
            if i < 0.5:
                b = False
        return b

    def face_direction(self, p1, p2):
        if p1[1] > p2[1]:
            return PointView.up
        else:
            return PointView.down

    def detect(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.model.process(frame)
        h, w, c = frame.shape
        key_points = []
        if results.pose_landmarks:
            for data_point in results.pose_landmarks.landmark:
                key_points.append([int(data_point.x*w), int(data_point.y*h), int(data_point.z*w), data_point.visibility])
            self.result = key_points
            self.point_side = self.side(key_points[0], key_points[11], key_points[12]) # detect side
            L_full = [key_points[0][3], key_points[2][3], key_points[11][3], key_points[23][3], key_points[25][3], key_points[27][3]]
            R_full = [key_points[0][3], key_points[5][3], key_points[12][3], key_points[24][3], key_points[26][3], key_points[28][3]]
            if self.point_side != PointView.front and (self.isOneSideFull(L_full) == True or self.isOneSideFull(R_full) == True):
                if self.point_side == PointView.left:
                    angle_classify_pushup = self.angle_cal(key_points[11], key_points[23], key_points[25])
                    face_classify_pushup2 = self.face_direction(key_points[2], key_points[0])
                    angle_classify_situp = self.angle_cal(key_points[23], key_points[25], key_points[27])
                    angle_classify_situp2 = self.angle_cal(key_points[23], key_points[25], [key_points[25][0], 0])
                    angle_classify_squat = self.angle_cal(key_points[11], key_points[23], [key_points[23][0], 0])
                    mid1 = [int((key_points[11][0]+key_points[23][0])/2), int((key_points[11][1]+key_points[23][1])/2)]
                    mid2 = [int((key_points[25][0]+key_points[27][0])/2), int((key_points[25][1]+key_points[27][1])/2)]
                    mid3 = [mid2[0], 0]
                    angle_classify_squat2 = self.angle_cal(mid1, mid2, mid3)
                else:
                    angle_classify_pushup = self.angle_cal(key_points[12], key_points[24], key_points[26])
                    face_classify_pushup2 = self.face_direction(key_points[5], key_points[0])
                    angle_classify_situp = self.angle_cal(key_points[24], key_points[26], key_points[28])
                    angle_classify_situp2 = self.angle_cal(key_points[24], key_points[26], [key_points[26][0], 0])
                    angle_classify_squat = self.angle_cal(key_points[12], key_points[24], [key_points[24][0], 0])
                    mid1 = [int((key_points[12][0]+key_points[24][0])/2), int((key_points[12][1]+key_points[24][1])/2)]
                    mid2 = [int((key_points[26][0]+key_points[28][0])/2), int((key_points[26][1]+key_points[28][1])/2)]
                    mid3 = [mid2[0], 0]
                    angle_classify_squat2 = self.angle_cal(mid1, mid2, mid3)
                self.prediction = self.predict(angle_classify_pushup, face_classify_pushup2, angle_classify_situp, angle_classify_situp2, angle_classify_squat, angle_classify_squat2)               
                if self.prediction == Activity.pushup:
                    self.angle_for_count = self.angle_cal(key_points[12], key_points[14], key_points[16])
                elif self.prediction == Activity.situp:
                    self.angle_for_count = self.angle_cal(key_points[12], key_points[24], key_points[26])
                elif self.prediction == Activity.squat:
                    self.angle_for_count = self.angle_cal(key_points[24], key_points[26], [key_points[26][0], 0])
                else:
                    self.angle_for_count = -1
            else:
                self.init_frame()
            self.draw.draw_landmarks(
                    frame, 
                    results.pose_landmarks, 
                    self.pose.POSE_CONNECTIONS, 
                    self.draw_style.DrawingSpec(color=(0,255,0), thickness=4, circle_radius= 4),
                    self.draw_style.DrawingSpec(color=(255,0,0), thickness=4, circle_radius= 4)
            )
        else:
            self.init_frame()
        return frame
