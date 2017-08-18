def look(character):
	looks = {
		'W': "########",
		'B': "%%%%%%%%",
		' ': "        ",
		'P': "[^^] ][ ",
		'E': "\--//xx\\",
	}
	return looks[character]

def color(character):
	colors = {
		'W': '\033[94m',
		'B': '\033[93m',
		' ': '\033[94m',
		'P': '\033[92m',
		'E': '\033[94m',
	}
	return colors[character]
