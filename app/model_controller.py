import cv2
import mediapipe as md
import numpy as np
import math

from .types import *


class ModelController:
    def __init__(self):
        self.draw = md.solutions.drawing_utils
        self.drawstyle = md.solutions.drawing_styles
        self.pose = md.solutions.pose
        self.model = self.pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5, model_complexity = 1)
        self.result = []
        self.angleforcount = -1
        self.prediction = Activity.non
        self.pointside = PointView.front

    def initframe(self):
        self.result = []
        self.angleforcount = -1
        self.prediction = Activity.non
        self.pointside = PointView.front

    def angle_cal(self, a,b,c):
        a = np.array(a, int) # First
        b = np.array(b, int) # Mid
        c = np.array(c, int) # End

        angle = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
        if angle < 0:
            angle += 360
            if angle > 180:
                angle = 360 - angle
        elif angle > 180:
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

    def facedirection(self, p1, p2):
        if p1[1] > p2[1]:
            return PointView.up
        else:
            return PointView.down

    def detect(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.model.process(frame)
        h, w, c = frame.shape
        keypoints = []
        if results.pose_landmarks:
            for data_point in results.pose_landmarks.landmark:
                keypoints.append([int(data_point.x*w), int(data_point.y*h), int(data_point.z*w), data_point.visibility])
            self.result = keypoints
            self.pointside = self.side(keypoints[0], keypoints[11], keypoints[12]) # detect side
            L_full = [keypoints[0][3], keypoints[2][3], keypoints[11][3], keypoints[23][3], keypoints[25][3], keypoints[27][3]]
            R_full = [keypoints[0][3], keypoints[5][3], keypoints[12][3], keypoints[24][3], keypoints[26][3], keypoints[28][3]]
            if self.pointside != PointView.front and (self.isOneSideFull(L_full) == True or self.isOneSideFull(R_full) == True):
                if self.pointside == PointView.left:
                    angle_classify_pushup = self.angle_cal(keypoints[11], keypoints[23], keypoints[25])
                    face_classify_pushup2 = self.facedirection(keypoints[2], keypoints[0])
                    angle_classify_situp = self.angle_cal(keypoints[23], keypoints[25], keypoints[27])
                    angle_classify_situp2 = self.angle_cal(keypoints[23], keypoints[25], [keypoints[25][0], 0])
                    angle_classify_squat = self.angle_cal(keypoints[11], keypoints[23], [keypoints[23][0], 0])
                    mid1 = [int((keypoints[11][0]+keypoints[23][0])/2), int((keypoints[11][1]+keypoints[23][1])/2)]
                    mid2 = [int((keypoints[25][0]+keypoints[27][0])/2), int((keypoints[25][1]+keypoints[27][1])/2)]
                    mid3 = [mid2[0], 0]
                    angle_classify_squat2 = self.angle_cal(mid1, mid2, mid3)
                else:
                    angle_classify_pushup = self.angle_cal(keypoints[12], keypoints[24], keypoints[26])
                    face_classify_pushup2 = self.facedirection(keypoints[5], keypoints[0])
                    angle_classify_situp = self.angle_cal(keypoints[24], keypoints[26], keypoints[28])
                    angle_classify_situp2 = self.angle_cal(keypoints[24], keypoints[26], [keypoints[26][0], 0])
                    angle_classify_squat = self.angle_cal(keypoints[12], keypoints[24], [keypoints[24][0], 0])
                    mid1 = [int((keypoints[12][0]+keypoints[24][0])/2), int((keypoints[12][1]+keypoints[24][1])/2)]
                    mid2 = [int((keypoints[26][0]+keypoints[28][0])/2), int((keypoints[26][1]+keypoints[28][1])/2)]
                    mid3 = [mid2[0], 0]
                    angle_classify_squat2 = self.angle_cal(mid1, mid2, mid3)
                self.prediction = self.predict(angle_classify_pushup, face_classify_pushup2, angle_classify_situp, angle_classify_situp2, angle_classify_squat, angle_classify_squat2)               
                if self.prediction == Activity.pushup:
                    self.angleforcount = self.angle_cal(keypoints[12], keypoints[14], keypoints[16])
                elif self.prediction == Activity.situp:
                    self.angleforcount = self.angle_cal(keypoints[12], keypoints[24], keypoints[26])
                elif self.prediction == Activity.squat:
                    self.angleforcount = self.angle_cal(keypoints[24], keypoints[26], [keypoints[26][0], 0])
                else:
                    self.angleforcount = -1
            else:
                self.initframe()
            self.draw.draw_landmarks(
                    frame, 
                    results.pose_landmarks, 
                    self.pose.POSE_CONNECTIONS, 
                    self.drawstyle.DrawingSpec(color=(0,255,0), thickness=4, circle_radius= 4),
                    self.drawstyle.DrawingSpec(color=(255,0,0), thickness=4, circle_radius= 4)
            )
        else:
            self.initframe()
        return frame