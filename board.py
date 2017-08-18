from config import look, color
import os
import time
import random

class Board:
	def __init__(self, board_height=20, board_width=20, enemies=[], number_of_bricks=40): # Add board settings
		self.board_height = board_height
		self.board_width = board_width
		self.map = [[' ' for i in range(board_height)] for j in range(board_width)]
		
		self.available_blocks = []
		for i in range(board_height):
			for j in range(board_width):
				if (i == 0 or j == 0 or i == (board_height - 1) or j == (board_width - 1) or (i%2 == 0 and j%2 == 0)):
					self.map[i][j] = 'W'
				elif (i>2 or j>2):
					self.available_blocks.append([i, j]);

		random.shuffle(self.available_blocks)
		
		temp = self.number_of_enemies = len(enemies)
		
		# for i in range(self.number_of_enemies):


		for i in range(number_of_bricks):
			self.map[self.available_blocks[i][0]][self.available_blocks[i][1]] = 'B'

		# print(self.available_blocks)

		self.map[1][1] = 'P'

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

	def start_game(self):
		while True:
			print(self)



			time.sleep(0.03)
			os.system('clear')