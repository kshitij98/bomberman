import config
import os
import time
import random
from score_card import ScoreCard
from person import Player, Enemy
from keyboard import Keyboard
from bomb import Bomb


class Board:
    def __init__(self,
                 enemies={'a': 2, 'b': 1},
                 brd_height=21,
                 brd_width=21,
                 bricks=40,
                 time=120):
        self.__gameNotOver = self.__gameNotPaused = True
        self.__brd_height = brd_height
        self.__brd_width = brd_width
        self.__M = [[' ' for i in range(brd_width)] for j in range(brd_height)]
        self.__enemies = []
        self.__bomb = Bomb()
        self.__timeLeft = int(time / config.sleepTime)
        self.__scoreCard = ScoreCard()

        self.__free = []
        for i in range(brd_height):
            for j in range(brd_width):
                if i == 0 or j == 0 or i == (brd_height - 1):
                    self.__M[i][j] = 'W'
                elif j == (brd_width - 1) or (i % 2 == 0 and j % 2 == 0):
                    self.__M[i][j] = 'W'
                elif (i > 2 or j > 2):
                    self.__free.append([i, j])

        random.shuffle(self.__free)

        temp = self.__types_of_enemies = len(enemies)

        for i in range(bricks):
            self.__M[self.__free[i][0]][self.__free[i][1]] = 'B'

        curr = bricks
        keys = list(enemies)
        for i in range(self.__types_of_enemies):
            for j in range(enemies[keys[i]]):
                x, y = self.__free[curr][0], self.__free[curr][1]
                self.__M[x][y] = keys[i]
                self.__enemies.append(Enemy(x, y, keys[i]))
                curr += 1
        self.__number_of_enemies = curr - bricks

        self.__player = Player(1, 1)
        self.__M[1][1] = 'P'
        self.__keyboard = Keyboard()

    def __str__(self):
        str = ""
        for i in range(self.__brd_height):
            for j in range(self.__brd_width):
                design = config.look(self.__M[i][j])
                str += config.color(self.__M[i][j]) + design[:4] + '\033[0m'
            str += '\n'
            for j in range(self.__brd_width):
                design = config.look(self.__M[i][j])
                str += config.color(self.__M[i][j]) + design[4:8] + '\033[0m'
            str += '\n'
        return str

    def __update_positions(self):
        player_x = -1
        for i in range(self.__brd_height):
            for j in range(self.__brd_width):
                if 'a' <= self.__M[i][j] and self.__M[i][j] <= 'z':
                    self.__M[i][j] = ' '
                elif self.__M[i][j] == 'X':
                    self.__M[i][j] = ' '
                elif (self.__M[i][j] == 'P'):
                    player_x, player_y = i, j

        for i in range(self.__number_of_enemies):
            if (self.__enemies[i].isAlive()):
                x, y = self.__enemies[i].getXY()
                if (self.__M[x][y] == 'P'):
                    self.__scoreCard.update(lives=-1)
                self.__M[x][y] = self.__enemies[i].get_type()

        if (player_x != -1):
            self.__M[player_x][player_y] = ' '
        x, y = self.__player.getXY()
        self.__M[x][y] = 'P'

        bomb = self.__bomb.getPosition()
        if (bomb):
            x, y = bomb['x'], bomb['y']
            self.__M[x][y] = bomb['timer']
            if (bomb['explode']):
                direction = [[0, 1], [1, 0], [0, -1], [-1, 0]]
                if self.__player.getX() == x and self.__player.getY() == y:
                    self.__scoreCard.update(lives=-1)
                intensity = bomb['intensity']
                for i in range(4):
                    for k in range(1, intensity+1):
                        x2, y2 = x + k*direction[i][0], y + k*direction[i][1]
                        player_x = self.__player.getX()
                        player_y = self.__player.getY()
                        if x2 == player_x and y2 == player_y:
                            self.__scoreCard.update(lives=-1)
                        if (self.__M[x2][y2] == 'B'):
                            self.__M[x2][y2] = 'X'
                            self.__scoreCard.update(score=config.score('B'))
                            break
                        elif (self.__M[x2][y2] == 'W'):
                            break
                        self.__M[x2][y2] = 'X'
        else:
            x, y = self.__bomb.getXY()
            if self.__M[x][y] == '0':
                self.__M[x][y] = ' '

        for i in range(self.__number_of_enemies):
            x, y = self.__enemies[i].getXY()
            if (self.__M[x][y] == 'X'):
                enemy_type = self.__enemies[i].get_type()
                self.__scoreCard.update(score=config.score(enemy_type))
                self.__enemies[i].kill()

        return 1

    def __isNotObstacle(self, x, y):
        if (self.__M[x][y] == ' '):
            return 1
        if (self.__M[x][y] == 'W'):
            return 0
        if (self.__M[x][y] == 'B'):
            return 0
        if (self.__M[x][y] == '5'):
            return 0
        if (self.__M[x][y] == '4'):
            return 0
        if (self.__M[x][y] == '3'):
            return 0
        if (self.__M[x][y] == '2'):
            return 0
        if (self.__M[x][y] == '1'):
            return 0
        if (self.__M[x][y] == '0'):
            return 0
        return 1

    def __key_bindings(self, key):
        x, y = self.__player.getX(), self.__player.getY()
        if self.__gameNotPaused:
            if (key == 'd'):
                self.__player.move(self.__isNotObstacle(x, y+1)*10 + 0)
            elif (key == 's'):
                self.__player.move(self.__isNotObstacle(x+1, y)*10 + 1)
            elif (key == 'a'):
                self.__player.move(self.__isNotObstacle(x, y-1)*10 + 2)
            elif (key == 'w'):
                self.__player.move(self.__isNotObstacle(x-1, y)*10 + 3)
            elif (key == 'b'):
                self.__bomb.plantBomb(x, y, 3)
        if (key == ' '):
            self.__gameNotPaused = not self.__gameNotPaused

    def start_game(self):
        current_time = 0
        MOD = config.time_constant('main')
        sleepTime = config.sleepTime

        while self.__gameNotOver and self.__timeLeft >= 0:
            print(self)
            print(self.__scoreCard)

            key = self.__keyboard.get_key()
            self.__keyboard.flush_istream()
            self.__key_bindings(key)
            if self.__gameNotPaused is False:
                time.sleep(sleepTime)
                os.system('clear')
                continue

            if (not self.__scoreCard.update(time=-1)):
                return False

            for i in range(self.__number_of_enemies):
                x, y = self.__enemies[i].getXY()
                self.__enemies[i].move_randomly([self.__isNotObstacle(x, y+1),
                                                self.__isNotObstacle(x+1, y),
                                                self.__isNotObstacle(x, y-1),
                                                self.__isNotObstacle(x-1, y)],
                                                current_time)

            self.__bomb.updateBomb()

            self.__update_positions()
            current_time = (current_time + 1) % MOD
            self.__timeLeft -= 1
            time.sleep(sleepTime)
            os.system('clear')
