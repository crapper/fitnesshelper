import enum

class ActivityType(enum.IntEnum):
    NA = 0
    UP = 1
    DOWN = 2

class Activity(enum.IntEnum):
    pushup = 0
    situp = 1
    squat = 2
    non = 3

class PointView(enum.IntEnum):
    left = 0
    right = 1
    front = 2
    down = 3
    up = 4
