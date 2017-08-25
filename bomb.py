import config
import math


class Bomb:
    def __init__(self, time=-1):
        self.timeLeft = time
        self.sleep = config.sleepTime
        self.x = 0
        self.y = 0

    def plantBomb(self, x=1, y=1, time=3, intensity=5):
        if (self.timeLeft != -1):
            return False
        self.intensity = intensity
        self.timeLeft = int(time / self.sleep)
        self.x = x
        self.y = y

    def getXY(self):
        return (self.x, self.y)

    def updateBomb(self):
        if (self.timeLeft >= 0):
            self.timeLeft -= 1

    def getPosition(self):
        if self.timeLeft >= 0:
            return {
                'explode': self.timeLeft == 0,
                'timer': str(math.floor((self.timeLeft - 1) * self.sleep) + 1),
                'x': self.x,
                'y': self.y,
                'intensity': self.intensity
            }
        return False
