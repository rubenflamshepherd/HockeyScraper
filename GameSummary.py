class Penalty(object):

	def __init__(self, pen_num, per_num, pen_time, pen_length, pen_type, penalized_player):
		self.pen_num = pen_num
		self.per_num = per_num
		self.pen_time = pen_time
		self.pen_length = pen_length
		self.pen_type = pen_type
		self.penalized_player = penalized_player

	def __str__ (self):
		return "Pen #: " + self.pen_num.encode('utf-8') + \
		'\nPer #: ' + self.per_num.encode('utf-8') +\
		'\nTime: ' + self.pen_time.encode('utf-8') +\
		'\nLength: ' + self.pen_length.encode('utf-8') +\
		'\nType: ' + self.pen_type.encode('utf-8') +\
		 '\nPP: ' + str(self.penalized_player[0]) + ' ' + str(self.penalized_player[1])


class ByPeriod(object):

	def __init__(self, pen_num, per_num, pen_time, pen_length, pen_type, penalized_player):
		self.pen_num = pen_num
		self.per_num = per_num
		self.pen_time = pen_time
		self.pen_length = pen_length
		self.pen_type = pen_type
		self.penalized_player = penalized_player

	def __str__ (self):
		return "Pen #: " + self.pen_num.encode('utf-8') + \
		'\nPer #: ' + self.per_num.encode('utf-8') +\
		'\nTime: ' + self.pen_time.encode('utf-8') +\
		'\nLength: ' + self.pen_length.encode('utf-8') +\
		'\nType: ' + self.pen_type.encode('utf-8') +\
		 '\nPP: ' + str(self.penalized_player[0]) + ' ' + str(self.penalized_player[1])

def chop_penalties_branch (tree):
	'''
	Given an indivudal team's penalties xml tree, return a list of
	GameSummaryPenalty objects
	'''
	iter_penalties = iter(tree)
	next (iter_penalties)

	penalties = []

	for item in iter_penalties:
		item_parts = item.xpath('./td/text()')
		pen_num = item_parts[0]
		per_num = item_parts[1]
		pen_time = item_parts[2]
		pen_length = item_parts[5]
		pen_type = item_parts[6]
		
		player_raw = item.xpath('./td/table/tr/td/text()')
		player_num = player_raw[0]
		player_name = player_raw[3][2:] # First inital infront of name
		penalized_player = (player_num, player_name) 

		temp = Penalty(pen_num, per_num, pen_time, pen_length, pen_type, penalized_player)

		penalties.append (temp)
	return penalties

def chop_byperiod_branch (tree):
	'''
	Given an indivudal team's "BY PERIOD" xml treeh, return a list of
	...something
	'''
	pass