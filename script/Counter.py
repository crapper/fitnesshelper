from enum_activity import ActivityType

class Counter:
    def __init__(self):
        self.peakvalleycount = 0
        self.state = ActivityType.NA
        self.tempcount_time = 0
        self.totaltime = 0

    def update_count(self, angle, temp):
        if angle >=0:
            if self.isDown(angle) and self.state == ActivityType.NA:
                self.state = ActivityType.DOWN
                self.tempcount_time = temp
            elif self.isUp(angle) and self.state == ActivityType.NA:
                self.state = ActivityType.UP
                self.tempcount_time = temp
            elif self.state == ActivityType.DOWN and self.isUp(angle):
                # self.play_sound()
                self.peakvalleycount += 1
                self.totaltime += temp - self.tempcount_time
                self.tempcount_time = temp
                self.state = ActivityType.UP
            elif self.state == ActivityType.UP and self.isDown(angle):
                # self.play_sound()
                self.peakvalleycount += 1
                self.totaltime += temp - self.tempcount_time
                self.tempcount_time = temp
                self.state = ActivityType.DOWN

    def isDown(self, angle):
        pass

    def isUp(self, angle):
        pass

    def get_count(self):
        return int(self.peakvalleycount/2)

class PushupCounter(Counter):
    def __init__(self):
        super().__init__()
        self.classname = "pushup"

    def isUp(self, angle):
        if angle >= 140:
            return True
        else:
            return False

    def isDown(self, angle):
        if angle <= 100:
            return True
        else:
            return False

class SitupCounter(Counter):
    def __init__(self):
        super().__init__()
        self.classname = "situp"

    def isUp(self, angle):
        if angle <= 60:
            return True
        else:
            return False

    def isDown(self, angle):
        if angle >= 90:
            return True
        else:
            return False

class SquatCounter(Counter):
    def __init__(self):
        super().__init__()
        self.classname = "squat"

    def isUp(self, angle):
        if angle <= 40:
            return True
        else:
            return False

    def isDown(self, angle):
        if angle >= 70:
            return True
        else:
            return False