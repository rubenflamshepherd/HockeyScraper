from lxml import html, etree
import Operations
import Objects

class Goal (object):

	def __init__(self, goal_num, per_num, time, strength, scoring_team, \
		scoring_player, prim_assist_player, sec_assist_player, \
		away_on_ice, home_on_ice):
		self.goal_num = goal_num
		self.per_num = per_num
		self.time = time
		self.strength = strength
		self.scoring_team = scoring_team
		self.scoring_player = scoring_player
		self.prim_assist_player = prim_assist_player
		self.sec_assist_player = sec_assist_player
		self.away_on_ice = away_on_ice
		self.home_on_ice = home_on_ice

	def __str__ (self):
		return "Goal #: " + self.goal_num.encode('utf-8') + \
		'\nPer #: ' + self.per_num.encode('utf-8') +\
		'\nStr: ' + self.strength.encode('utf-8') +\
		'\nScoring Team: ' + self.scoring_team.encode('utf-8') +\
		'\nSP: ' + str(self.scoring_player[0]) + ' ' + str(self.scoring_player[1]) +\
		'\nPA: ' + str(self.prim_assist_player[0]) + ' ' + str(self.prim_assist_player[1]) +\
		'\nSA: ' + str(self.sec_assist_player[0]) + ' ' + str(self.sec_assist_player[1])

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

class Goalie (object):
	def __init__(self, num, first_name, last_name, status, fields_list):
		self.num = num
		self.first_name = first_name
		self.last_name = last_name
		self.status = status #(W/L/OT/None)
		self.fields_list = fields_list

	def __str__ (self):

		fields_header = ''
		fields_data = ''
		for item in self.fields_list:
			fields_header += item.field_title.ljust(6)
		
		for item in self.fields_list:
			fields_data += item.field_content.ljust(6)
		
		basic_data = self.num + " | " + \
			self.first_name.encode('utf-8') + " " +\
			self.last_name.encode('utf-8') + "|" +\
			str(self.status).encode('utf-8')

		all_strings = basic_data + \
			"\n" + fields_header + \
			"\n" + fields_data

		return all_strings
		
class GoalieField (object):
	def __init__(self, field_title, field_content):
		self.field_title = field_title
		self.field_content = field_content

	def __str__ (self):
		return self.field_title + " | " + \
		self.field_content.encode('utf-8')

def chop_goals_branch (tree):
	'''
	Given the goal xml tree, return a list of Goal objects
	'''

	goals = []
	
	# Skipping first item in iterable roster
	iter_goals = iter(tree)
	next (iter_goals)

	for item in iter_goals:
		temp_goal = item.xpath('.//td/text()')
		temp_xpath = item.xpath('.//td')
		
		goal_num = temp_goal[0]
		per_num = temp_goal[1]
		time = temp_goal[2]
		strength = temp_goal[3]
		scoring_team = temp_goal[4]
		
		scoring_player_raw = temp_goal [5].split()
		scoring_num = scoring_player_raw[0]
		name_raw = scoring_player_raw[1]
		scoring_name = name_raw[name_raw.find(".") + 1:name_raw.find("(")]

		scoring_player = (scoring_num, scoring_name)
		
		try:
			prim_assist_player_raw = temp_goal [6].split()
			prim_assist_num = prim_assist_player_raw[0]
			name_raw = prim_assist_player_raw[1]
			prim_assist_name = name_raw[name_raw.find(".") + 1:name_raw.find("(")]

			prim_assist_player = (prim_assist_num, prim_assist_name)

		except:
			prim_assist_player = (None, None)
		
		try:
			sec_assist_player_raw = temp_goal [7].split()
			sec_assist_num = sec_assist_player_raw[0]
			name_raw = sec_assist_player_raw[1]
			sec_assist_name = name_raw[name_raw.find(".") + 1:name_raw.find("(")]

			sec_assist_player = (sec_assist_num, sec_assist_name)

		except:
			sec_assist_player = (None, None)
		
		away_on_ice = Operations.chop_on_ice_branch (temp_xpath[8])
		home_on_ice = Operations.chop_on_ice_branch (temp_xpath[9])

		goals.append(Goal(goal_num, per_num, time, strength, scoring_team, \
			scoring_player, prim_assist_player, sec_assist_player, \
			away_on_ice, home_on_ice))

	return goals
		
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
	Given an indivudal team's situation ("POWERPLAY/EVENSTRENGTH) xml tree 
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

def chop_goalie_branch(tree):
	'''
	Given a single table (as an xml tree) return lists containing Goalie
	objects for each team
	'''

	for item in tree.xpath('./tr'):
		
		# Setting the list to be populated (away vs home)
		item_down = item.xpath("./td")[0]
		if item_down.attrib['class'] == 'rborder + bborder + visitorsectionheading': 
			active_headers = item.xpath('./td/text()')
			active_goalies = []
		
		elif item_down.attrib['class'] == 'rborder + bborder + homesectionheading': 
			active_headers = item.xpath('./td/text()')
			away_goalies = active_goalies
			active_goalies = []

		# Creating Goalie and GoalieField objects
		elif 'class' in item.attrib:
			if item.attrib['class'] == 'evenColor' or \
				item.attrib['class'] == 'oddColor':
				
				goalie_raw = item.xpath ('./td/text()')
				# Instatiate list containing GoalieField objects
				fields = []

				for index, cell in enumerate(goalie_raw):
					if index == 0:
						goalie_num = cell

					elif index == 1:
						goalie_pos = cell
						assert goalie_pos == 'G', "ERROR: goalie pos not 'G'"

					elif index == 2:
						name_raw = cell.split()

						if name_raw[-1].find("(") != -1:
							status = name_raw[-1]
							name_raw.pop()
						else:
							status = None

						anchor = Operations.index_containing_substring(name_raw, ",")

						last_name = (" ".join(name_raw[:anchor + 1])).strip(',')
						first_name = " ".join(name_raw[anchor + 1:])

					elif index >= 3:
						field_title = active_headers[index-3]
						if cell == u'\xa0':
							cell = None
						field_content = str(cell)
						fields.append (GoalieField(field_title, field_content))
						
				active_goalies.append (Goalie (goalie_num, first_name, last_name, status, fields))
	home_goalies = active_goalies

	return away_goalies, home_goalies

def chop_officials_branch(tree):
	'''
	Given a table (as an xml tree) return lists containing Goalie
	objects for each team. Table also contains 3 stars
	'''

	referees = []
	linesmen = []

	officials_raw = tree.xpath('./tr/td/table')[0]
	referees_raw = officials_raw.xpath('./tr/td/table')[0].xpath('./tr/td/text()')
	linesmen_raw = officials_raw.xpath('./tr/td/table')[1].xpath('./tr/td/text()')

	for item in referees_raw:
		referee_raw = item.split()
		num =  referee_raw[0].strip('#')
		first_name = referee_raw[1]
		last_name = " ".join(referee_raw[2:])
		referees.append(Objects.Referee(num, first_name, last_name))

	for item in linesmen_raw:
		linesman_raw = item.split()
		num =  linesman_raw[0].strip('#')
		first_name = linesman_raw[1]
		last_name = " ".join(linesman_raw[2:])
		linesmen.append(Objects.Linesman(num, first_name, last_name))
	
	return linesmen, referees	

def chop_stars_branch(tree):
	'''
	Given a table (as an xml tree) return lists containing Goalie
	objects for each team. Table also contains officials
	'''

	stars = []
	picker_raw = tree.xpath('./tr/td/text()')[1]

	anchor = picker_raw.find(':')
	picker = picker_raw[anchor + 1:]	

	stars_raw = tree.xpath('./tr/td/table')[1].xpath('./tr/td/table/tr')

	for item in stars_raw:
		star_num = item.xpath('./td/text()')[0].strip('.')
		team = item.xpath('./td/text()')[1]
		pos = item.xpath('./td/text()')[2]
		name_raw = item.xpath('./td/text()')[3].split()
		player_num = name_raw [0]

		anchor = name_raw[1].find('.')
		last_name = name_raw[1][anchor + 1:]
		stars.append((star_num, team, player_num, last_name))
	
	#print etree.tostring (stars_raw, pretty_print = True)
 	return picker, stars
