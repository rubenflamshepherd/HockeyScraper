from lxml import html, etree

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


class Period(object):

	def __init__(self, per_num, num_goals, num_shots, num_penalties, PIM):
		self.per_num = per_num
		self.num_goals = num_goals
		self.num_shots = num_shots
		self.num_penalties = num_penalties
		self.PIM = PIM

	def __str__ (self):
		return "Per #: " + self.per_num.encode('utf-8') + \
		' |Goals: ' + self.num_goals.encode('utf-8') +\
		' |Shots: ' + self.num_shots.encode('utf-8') +\
		' |Penalties: ' + self.num_penalties.encode('utf-8') +\
		' |PIM: ' + self.PIM.encode('utf-8')

class Situation (object):
	def __init__(self, strength, num_goals, num_occurances, time):
		self.strength = strength
		self.num_goals = num_goals
		self.num_occurances = num_occurances
		self.time = time

	def __str__ (self):
		return self.strength + " : " + \
		self.num_goals.encode('utf-8') + "-" +\
		self.num_occurances.encode('utf-8') + "/" +\
		self.time.encode('utf-8') +\
		" (Goals-Occurance/Time)"
		
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
	Period objects
	'''

	periods = []

	for x in range (1,len(tree)-1):
		per_num = tree[x].xpath('./td/text()')[0]
		num_goals = tree[x].xpath('./td/text()')[1]
		num_shots = tree[x].xpath('./td/text()')[2]
		num_penalties = tree[x].xpath('./td/text()')[3]
		PIM = tree[x].xpath('./td/text()')[4]

		periods.append (Period(per_num, num_goals, num_shots, num_penalties, PIM))

	return periods

def chop_situation_branch (tree):
	'''
	Given an indivudal team's situation ("POWERPLAY/EVENSTRNGTH) xml tree 
	(with /table as the root element), return a list of Situation objects
	'''

	situations = []

	header_items = (tree.xpath ("./tr")[0]).xpath("./td/text()")
	item_data = (tree.xpath ("./tr")[1]).xpath("./td/text()")

	assert len(header_items) == len(item_data), " # of situations != # of situations for which there are stats"
	
	for index, strength in enumerate(header_items):
		
		anchor1 = item_data[index].find ('-')
		anchor2 = item_data[index].find ('/')
		
		if anchor2 != -1:
			num_goals = item_data[index][:anchor1]
			num_occurences = item_data[index][anchor1 + 1:anchor2]
			time = item_data[index][anchor2 + 1:]

			temp = Situation(strength, num_goals, num_occurences, time)

			situations.append(temp)

	return situations