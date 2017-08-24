import config
import math

class ScoreCard:
	def __init__(self, timeLeft=120, score=0, lives=3):
		self.timeLeft = int(timeLeft / config.sleepTime)
		self.score = score
		self.lives = lives
		self.sleepTime = config.sleepTime

	def __str__(self):
		string = ""
		string += "TIME LEFT: " + str(math.floor((self.timeLeft - 1) * self.sleepTime) + 1) + "\n"
		string += "SCORE: " + str(self.score) + "\n"
		string += "LIVES: " + str(self.lives) + "\n"
		self.timeLeft -= 1
		return string

	def update(self, score=0, lives=0, time=-1):
		self.timeLeft += time
		self.score += score
		self.lives += lives
		return self.timeLeft > 0 and self.lives > 0