import sys
import termios
from select import select

class Keyboard:
	def __init__(self):
		self.fileDescriptor = sys.stdin.fileno()
		self.newTerm = termios.tcgetattr(self.fileDescriptor)
		self.oldTerm = termios.tcgetattr(self.fileDescriptor)

		self.newTerm[3] = (self.newTerm[3] & ~termios.ICANON & ~termios.ECHO)
		termios.tcsetattr(self.fileDescriptor, termios.TCSAFLUSH, self.newTerm)

	def get_key(self):
		dr, dw, de = select([sys.stdin], [], [], 0)
		if (dr != []):
			return sys.stdin.read(1)
		return False

	def flush_istream(self):
		termios.tcflush(self.fileDescriptor, termios.TCIFLUSH)

	def __del__(self):
		termios.tcsetattr(self.fileDescriptor, termios.TCSAFLUSH, self.oldTerm)