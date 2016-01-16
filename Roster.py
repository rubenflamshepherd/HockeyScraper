import GameHeader
import Operations

class Coach:

	def __init__ (self, first_name, last_name):

		self.first_name = first_name
		self.last_name = last_name
		self.team = None # gets assigned outside of chop_coach function

	def full_name (self):

		return self.first_name + ' ' + self.last_name

	def __str__ (self):

		first_name = (self.first_name.encode('utf-8')).ljust(10)
		last_name = (self.last_name.encode('utf-8')).ljust(10)
		team = (str(self.team).encode('utf-8')).ljust(5)

		return team + first_name + last_name + '\n'

class R_Player:

	def __init__ (self, team, num, pos, first_name, last_name, captaincy, starting, \
			scratch, playerid):

		self.team = team
		self.num = num
		self.pos = pos
		self.first_name = first_name
		self.last_name = last_name
		self.captaincy = captaincy
		self.starting = starting
		self.scratch = scratch
		self.playerid = playerid

		self.show = str(self.num) + ' ' + str(self.last_name)

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.__dict__ == other.__dict__
		else:
			return False

	def __ne__(self, other):
		return not self.__eq__(other)

	def __str__(self):

		num = ("#" + str(self.num).encode('utf-8')).ljust(4)
		pos = ("Pos " + str(self.pos).encode('utf-8')).ljust(6)

		name_raw = str(self.team) + ' ' + str(self.first_name).encode('utf-8') + ' ' \
			+ str(self.last_name).encode('utf-8')
		name = (name_raw).ljust(25)

		captaincy = ("A/C " + str(self.captaincy)).ljust(9)
		starting = ("Strt " + str(self.starting)).ljust(9)
		scratch = ("Scrtch " + str(self.scratch)).ljust(11)
		playerid = ("ID " + str(self.playerid)).ljust(10)

		return num + pos + name + captaincy + starting + \
			scratch + playerid + '\n'

class Official:
	def __init__(self, num, first_name, last_name):
		self.num = num
		self.first_name = first_name
		self.last_name = last_name

class Referee(Official):

	def __str__(self):

		return "Referee: " + str(self.num) + ' ' + str(self.first_name) \
			+ ' ' + str(self.last_name) + '\n'

class Linesman(Official):

	def __str__(self):

		return "Linesman: " + str(self.num) + ' ' + str(self.first_name) \
			+ ' ' + str(self.last_name) + '\n'

class GamePersonnel(object):
	def __init__ (self, away_roster, home_roster, away_coach, home_coach, \
		referees, linesmen):
		self.away_roster = away_roster
		self.home_roster = home_roster
		self.away_coach = away_coach
		self.home_coach = home_coach
		self.referees = referees
		self.linesmen = linesmen

	def __str__ (self):
		
		away_roster = ''.ljust(30,'#') + ' AWAY ROSTER '.center(18) \
			+ ''.ljust(30,'#') + '\n'
		for item in self.away_roster:
			away_roster += item.__str__()

		home_roster = ''.ljust(30,'#') + ' HOME ROSTER '.center(18) \
			+ ''.ljust(30,'#') + '\n'
		for item in self.home_roster:
			home_roster += item.__str__()

		away_coach = ''.ljust(30,'#') + ' AWAY COACH '.center(18) \
			+ ''.ljust(30,'#') + '\n'
		away_coach += self.away_coach.__str__()

		home_coach = ''.ljust(30,'#') + ' HOME COACH '.center(18) \
			+ ''.ljust(30,'#') + '\n'
		home_coach += self.home_coach.__str__()

		officials = ''.ljust(30,'#') + ' OFFICIALS '.center(18) \
			+ ''.ljust(30,'#') + '\n'
		for item in self.referees:
			officials += item.__str__()
		for item in self.linesmen:
			officials += item.__str__()

		return away_roster + home_roster + away_coach + home_coach + \
			officials

def return_null_player():
	return R_Player (None, None, None, None, None, None, None, None, None)

def chop_coach_branch (tree):
	'''
	Given a single table (as an xml tree), return away and home coaches as 
	Coach objects
	'''

	away_coach_raw = tree[9].xpath('./tr/td/text()')[0]
	away_coach = Coach(
		first_name = away_coach_raw.split()[0],
		last_name = " ".join(away_coach_raw.split()[1:])
		)

	home_coach_raw = tree[10].xpath('./tr/td/text()')[0]
	home_coach = Coach(
		first_name = home_coach_raw.split()[0],
		last_name = " ".join(home_coach_raw.split()[1:])
		)
	
	return away_coach, home_coach

def chop_officials_branch (tree):
	'''
	Grab referees and linesmen from an xml tree (of an html roster report) and
	roster html file and return them as a tuple of lists containing 
	([Referees.objects], [Linesmen.objects])
	'''

	officials_raw = tree[11].xpath('./tr/td//tr/td/text()')

	assert len(officials_raw) == 4, "ERROR: 4 Officials not present"

	referees = []
	linesmen = []

	for index, official_raw in enumerate(officials_raw):
		
		official = official_raw.split()
		
		num = official[0].strip('#')
		first_name = official[1]
		last_name = " ".join(official[2:])

		if index < 2:
			temp_official = Referee (num, first_name, last_name)
			referees.append (temp_official)
		else:
			temp_official = Linesman (num, first_name, last_name)
			linesmen.append (temp_official)
		# print temp_official

	return referees, linesmen

def prune_roster_parts (tree, scratch, team, years, roster_objects):
	'''
	Given xml tree of a part of a roster (either scratched or nonscratched 
	list as tree), construct and add R_Player objects to roster_objects list
	'''
	iter_roster = iter(tree)
	next(iter_roster)

	for item in iter_roster:

		captaincy = None
		num = item.xpath('./td/text()')[0]
		position = item.xpath('./td/text()')[1]

		temp_starting = item.xpath ('./td/@class')[0]
		starting = 0
		if 'bold' in temp_starting:
			starting = 1

		temp_name_raw = item.xpath('./td/text()')[2]		
		temp_name_raw_split = temp_name_raw.split()
		first_name = temp_name_raw_split[0]

		if '(A)' in temp_name_raw_split:
			captaincy = 'A'
			temp_name_raw_split.pop (-1)
		elif '(C)' in temp_name_raw_split:
			captaincy = 'C'
			temp_name_raw_split.pop (-1)

		last_name = " ".join(temp_name_raw_split[1:])

		playerid = Operations.get_playerid (
			first_name, last_name, team, years, position)

		roster_objects.append(R_Player(team, num, position, first_name, 
			last_name, captaincy, starting, scratch, playerid))
		
def chop_ind_roster_branch (tree, anchor, game_info, years):
	"""
	Extract indivudal information from an xml tree and return list 
	of roster objects. anchor is 'visitor' or 'home' (used to anchor xml tree)
	"""

	roster_objects = []

	if anchor == 'away':
		x, y = 5, 7
		team = game_info.away_team
	elif anchor == 'home':
		x, y = 6, 8
		team = game_info.home_team
	else:
		assert False, "ERROR: anchor passed to chop_ind_roster_branch invalid"

	tree_active = tree[x].xpath('./tr')
	tree_scratches = tree[y].xpath('./tr')
	prune_roster_parts (tree_active, 0, team, years, roster_objects)
	prune_roster_parts (tree_scratches, 1, team, years, roster_objects)

	return roster_objects

def harvest (year, game_num):
	"""
	Extract roster information from a html file on the
	local machine and create database entries
	"""

	game_info = GameHeader.harvest (year, game_num, 'RO', '02')

	tree = Operations.germinate_report_seed (year, game_num, "RO", '02')

	tables = tree.xpath('//table//table//table//table')

	away_roster = chop_ind_roster_branch (tables, 'away', game_info, year)
	home_roster = chop_ind_roster_branch (tables, 'home', game_info, year)
	
	away_coach, home_coach = chop_coach_branch(tables)
	away_coach.team = game_info.away_team
	home_coach.team = game_info.home_team
	
	referees, linesmen = chop_officials_branch (tables)

	return GamePersonnel (
		away_roster, home_roster, away_coach, home_coach, referees, linesmen
		)

if __name__ == '__main__':
	for x in range (1,100):
		game_num = Operations.pad_game_num(x)
		print harvest('20142015', game_num)