from config import look, color, time_constant
import os
import time
import random
from person import Player, Enemy
from keyboard import Keyboard

class Board:
	def __init__(self, board_height=21, board_width=21, enemies={'a': 10, 'b': 5, 'c': 2, 'd': 1}, number_of_bricks=40): # Add board settings
		self.board_height = board_height
		self.board_width = board_width
		self.map = [[' ' for i in range(board_width)] for j in range(board_height)]
		self.enemies = []

		self.available_blocks = []
		for i in range(board_height):
			for j in range(board_width):
				if (i == 0 or j == 0 or i == (board_height - 1) or j == (board_width - 1) or (i%2 == 0 and j%2 == 0)):
					self.map[i][j] = 'W'
				elif (i>2 or j>2):
					self.available_blocks.append([i, j]);

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
				design = look(self.map[i][j])
				str += color(self.map[i][j]) + design[:4] + '\033[0m'
			str += '\n'
			for j in range(self.board_width):
				design = look(self.map[i][j])
				str += color(self.map[i][j]) + design[4:8] + '\033[0m'
			str += '\n'
		return str

	def update_positions(self):
		for i in range(self.board_height):
			for j in range(self.board_width):
				if ('a' <= self.map[i][j] and self.map[i][j] <= 'z'):
					self.map[i][j] = ' '

		for i in range(self.number_of_enemies):
			x, y = self.enemies[i].getXY()
			self.map[x][y] = self.enemies[i].get_type()

	def start_game(self):
		current_time = 0
		MOD = time_constant('main')

		while True:
			print(self)

			key = self.keyboard.get_key()
			print(key)
			# print(self.enemies)

			for i in range(self.number_of_enemies):
				x, y = self.enemies[i].getXY()
				self.enemies[i].move_randomly([(self.map[x][y+1] != 'B' and self.map[x][y+1] != 'W' and self.map[x][y+1] != 'X') * 0.25, (self.map[x+1][y] != 'B' and self.map[x+1][y] != 'W' and self.map[x+1][y] != 'X') * 0.25, (self.map[x][y-1] != 'B' and self.map[x][y-1] != 'W' and self.map[x][y-1] != 'X') * 0.25, (self.map[x-1][y] != 'B' and self.map[x-1][y] != 'W' and self.map[x-1][y] != 'X') * 0.25], current_time)

			self.update_positions()
			self.keyboard.flush_istream()
			current_time = (current_time + 1) % MOD
			time.sleep(0.05)
			os.system('clear')