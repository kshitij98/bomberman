import config
import os
import time
import random
from score_card import ScoreCard
from person import Player, Enemy
from keyboard import Keyboard
from bomb import Bomb


class Board:
    def __init__(self, board_height=21, board_width=21, enemies={'a': 1, 'b': 1, 'c': 1, 'd': 1}, number_of_bricks=40, time=120):
        self.gameNotOver = self.gameNotPaused = True
        self.board_height = board_height
        self.board_width = board_width
        self.map = [[' ' for i in range(board_width)] for j in range(board_height)]
        self.enemies = []
        self.bomb = Bomb()
        self.timeLeft = int(time / config.sleepTime)
        self.scoreCard = ScoreCard()

        self.available_blocks = []
        for i in range(board_height):
            for j in range(board_width):
                if (i == 0 or j == 0 or i == (board_height - 1) or j == (board_width - 1) or (i % 2 == 0 and j % 2 == 0)):
                    self.map[i][j] = 'W'
                elif (i > 2 or j > 2):
                    self.available_blocks.append([i, j])

        random.shuffle(self.available_blocks)

        temp = self.types_of_enemies = len(enemies)

        for i in range(number_of_bricks):
            self.map[self.available_blocks[i][0]][self.available_blocks[i][1]] = 'B'

        curr = number_of_bricks
        keys = list(enemies)
        for i in range(self.types_of_enemies):
            for j in range(enemies[keys[i]]):
                self.map[self.available_blocks[curr][0]][self.available_blocks[curr][1]] = keys[i]
                self.enemies.append(Enemy(self.available_blocks[curr][0], self.available_blocks[curr][1], keys[i]))
                curr += 1
        self.number_of_enemies = curr - number_of_bricks

        self.player = Player(1, 1)
        self.map[1][1] = 'P'
        self.keyboard = Keyboard()

    def __str__(self):
        str = ""
        for i in range(self.board_height):
            for j in range(self.board_width):
                design = config.look(self.map[i][j])
                str += config.color(self.map[i][j]) + design[:4] + '\033[0m'
            str += '\n'
            for j in range(self.board_width):
                design = config.look(self.map[i][j])
                str += config.color(self.map[i][j]) + design[4:8] + '\033[0m'
            str += '\n'
        return str

    def update_positions(self):
        player_x = -1
        for i in range(self.board_height):
            for j in range(self.board_width):
                if ('a' <= self.map[i][j] and self.map[i][j] <= 'z' or self.map[i][j] == 'X'):
                    self.map[i][j] = ' '
                elif (self.map[i][j] == 'P'):
                    player_x, player_y = i, j

        for i in range(self.number_of_enemies):
            if (self.enemies[i].isAlive()):
                x, y = self.enemies[i].getXY()
                if (self.map[x][y] == 'P'):
                    self.scoreCard.update(lives=-1)
                self.map[x][y] = self.enemies[i].get_type()

        if (player_x != -1):
            self.map[player_x][player_y] = ' '
        x, y = self.player.getXY()
        self.map[x][y] = 'P'

        bomb = self.bomb.getPosition()
        if (bomb):
            x, y = bomb['x'], bomb['y']
            self.map[x][y] = bomb['timer']
            if (bomb['explode']):
                direction = [[0, 1], [1, 0], [0, -1], [-1, 0]]
                if self.player.getX() == x and self.player.getY() == y:
                    self.scoreCard.update(lives=-1)
                intensity = bomb['intensity']
                for i in range(4):
                    for k in range(1, intensity+1):
                        x2, y2 = x + k*direction[i][0], y + k*direction[i][1]
                        if (x2 == self.player.getX() and y2 == self.player.getY()):
                            self.scoreCard.update(lives=-1)
                        if (self.map[x2][y2] == 'B'):
                            self.map[x2][y2] = 'X'
                            self.scoreCard.update(score=config.score('B'))
                            break
                        elif (self.map[x2][y2] == 'W'):
                            break
                        self.map[x2][y2] = 'X'
        else:
            x, y = self.bomb.getXY()
            if self.map[x][y] == '0':
                self.map[x][y] = ' '

        for i in range(self.number_of_enemies):
            x, y = self.enemies[i].getXY()
            if (self.map[x][y] == 'X'):
                self.scoreCard.update(score=config.score(self.enemies[i].get_type()))
                self.enemies[i].kill()

        return 1

    def isNotObstacle(self, x, y):
        if (self.map[x][y] == ' '):
            return 1
        if (self.map[x][y] == 'W'):
            return 0
        if (self.map[x][y] == 'B'):
            return 0
        if (self.map[x][y] == '5'):
            return 0
        if (self.map[x][y] == '4'):
            return 0
        if (self.map[x][y] == '3'):
            return 0
        if (self.map[x][y] == '2'):
            return 0
        if (self.map[x][y] == '1'):
            return 0
        if (self.map[x][y] == '0'):
            return 0
        return 1

    def key_bindings(self, key):
        if self.gameNotPaused:
            if (key == 'd'):
                self.player.move(0, self.isNotObstacle(self.player.getX(), self.player.getY()+1))
            elif (key == 's'):
                self.player.move(1, self.isNotObstacle(self.player.getX()+1, self.player.getY()))
            elif (key == 'a'):
                self.player.move(2, self.isNotObstacle(self.player.getX(), self.player.getY()-1))
            elif (key == 'w'):
                self.player.move(3, self.isNotObstacle(self.player.getX()-1, self.player.getY()))
            elif (key == 'b'):
                self.bomb.plantBomb(self.player.getX(), self.player.getY(), 3)
        if (key == ' '):
            self.gameNotPaused = not self.gameNotPaused

    def start_game(self):
        current_time = 0
        MOD = config.time_constant('main')
        sleepTime = config.sleepTime

        while self.gameNotOver and self.timeLeft >= 0:
            print(self)
            print(self.scoreCard)

            key = self.keyboard.get_key()
            self.keyboard.flush_istream()
            self.key_bindings(key)
            if self.gameNotPaused is False:
                time.sleep(sleepTime)
                os.system('clear')
                continue

            if (not self.scoreCard.update(time=-1)):
                return False

            for i in range(self.number_of_enemies):
                x, y = self.enemies[i].getXY()
                self.enemies[i].move_randomly([self.isNotObstacle(x, y+1), self.isNotObstacle(x+1, y), self.isNotObstacle(x, y-1), self.isNotObstacle(x-1, y)], current_time)

            self.bomb.updateBomb()

            self.update_positions()
            current_time = (current_time + 1) % MOD
            self.timeLeft -= 1
            time.sleep(sleepTime)
            os.system('clear')
