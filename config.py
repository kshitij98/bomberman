sleepTime = 0.08

def look(character):
	looks = {
		'W': "########",
		'B': "%%%%%%%%",
		'X': "eeeeeeee",
		' ': "        ",
		'P': "[^^] ][ ",
		'E': "\--//xx\\",
		'a': "\--//aa\\",
		'b': "\--//bb\\",
		'c': "\--//cc\\",
		'd': "\@@//@@\\",
		'3': "33333333",
		'2': "22222222",
		'1': "11111111",
		'0': "00000000",
	}
	return looks[character]

def color(character):
	colors = {
		'W': '\033[44m\033[94m',
		'B': '\033[43m',
		'X': '\033[41m',
		' ': '\033[94m',
		'P': '\033[92m',
		'E': '\033[91m',
		'a': "\033[91m",
		'b': "\033[91m",
		'c': "\033[91m",
		'd': "\033[91m",
		'3': "\033[91m",
		'2': "\033[91m",
		'1': "\033[91m",
		'0': "\033[91m",
	}
	return colors[character]

def time_constant(character):
	times = {
		'main': 24,
		'a': 12,
		'b': 8,
		'c': 6,
		'd': 2,
		'P': 6,
	}
	return times[character]

def score(character):
	scores = {
		'B': 20,
		'a': 100,
		'b': 100,
		'c': 100,
		'd': 150,
	}
	return scores[character]
