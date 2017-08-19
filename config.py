def look(character):
	looks = {
		'W': "########",
		'B': "%%%%%%%%",
		' ': "        ",
		'P': "[^^] ][ ",
		'E': "\--//xx\\",
		'a': "\--//aa\\",
		'b': "\--//bb\\",
		'c': "\--//cc\\",
		'd': "\--//dd\\",
	}
	return looks[character]

def color(character):
	colors = {
		'W': '\033[44m',
		'B': '\033[43m',
		' ': '\033[94m',
		'P': '\033[92m',
		'E': '\033[91m',
		'a': "\033[91m",
		'b': "\033[91m",
		'c': "\033[91m",
		'd': "\033[91m",
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

