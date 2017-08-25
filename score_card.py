import config
import math
from getch import getch


class ScoreCard:
    def __init__(self, timeLeft=120, score=0, lives=3):
        self.timeLeft = int(timeLeft / config.sleep)
        self.score = score
        self.lives = lives
        self.sleep = config.sleep

    def __str__(self):
        string = "TIME LEFT: "
        string += str(math.floor((self.timeLeft - 1) * self.sleep) + 1) + "\n"
        string += "SCORE: " + str(self.score) + "\n"
        string += "LIVES: " + str(self.lives) + "\n"
        return string

    def update(self, score=0, lives=0, time=0):
        self.timeLeft += time
        self.score += score
        self.lives += lives
        if lives:
            getch()
        return self.timeLeft > 0 and self.lives > 0
