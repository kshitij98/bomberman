import config
import random


class Person:
    def __init__(self, x, y):
        self.X = x
        self.Y = y
        self.alive = True

    def getXY(self):
        return (self.X, self.Y)

    def getX(self):
        return self.X

    def getY(self):
        return self.Y

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
        self.immortal = False
        self.timeLeft = -1
        self.sleepTime = config.sleepTime

    # def makeImmortal(self, x=1, y=1, time=10):
        # if (self.timeLeft != -1): return False
        # self.timeLeft = int(time / self.sleepTime)
        # self.immortal = True

    # def isImmortal(self):
        # return self.immortal

    def move(self, direction, isPossible):
        if (isPossible == 1):
            super().move(direction)


class Enemy(Person):
    def __init__(self, x, y, enemy_type):
        Person.__init__(self, x, y)
        self.type = enemy_type
        self.time_constant = config.time_constant(enemy_type)
        self.lastMove = 0

    def get_type(self):
        return self.type

    def kill(self):
        self.alive = False

    def isAlive(self):
        return self.alive

    def move_randomly(self, probabilities, current_time):
        if (current_time % self.time_constant > 0):
            return False

        if probabilities[self.lastMove] != 0:
            probabilities[(self.lastMove + 2) % 4] = 0
            probabilities[self.lastMove] *= 6
        else:
            probabilities[(self.lastMove + 2) % 4] *= 6

        total_probability = sum(probabilities)
        if (total_probability == 0):
            return False

        current_probablity = random.random() * total_probability
        total_sum = 0
        for i in range(4):
            total_sum += probabilities[i]
            if current_probablity <= total_sum:
                self.lastMove = i
                self.move(i)
                return True
