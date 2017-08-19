from config import time_constant
import random

class Person:
	def __init__(self, x, y):
		self.X = x
		self.Y = y
	
	def getXY(self):
		return (self.X, self.Y)

	def setXY(self, x, y):
		self.X = x
		self.Y = y

	def move(self, direction):
		directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
		x, y = self.getXY()
		x += directions[direction][0]
		y += directions[direction][1]
		self.setXY(x, y)

class Player(Person):
	def __init__(self, x, y):
		Person.__init__(self, x, y)

class Enemy(Person):
	def __init__(self, x, y, enemy_type):
		Person.__init__(self, x, y)
		self.type = enemy_type
		self.time_constant = time_constant(enemy_type)

	def get_type(self):
		return self.type

	def move_randomly(self, probabilities, current_time):
		if (current_time % self.time_constant > 0):
			return False
		total_probability = sum(probabilities)
		current_probablity = random.random() * total_probability
		total_sum = 0
		for i in range(4):
			total_sum += probabilities[i]
			if current_probablity <= total_sum:
				self.move(i)
				return True
		