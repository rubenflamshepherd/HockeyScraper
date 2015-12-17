'''
Parse information from html reports stored as local files using xml trees
'''

from lxml import html, etree
import re
import GameSummary
import sqlite3
import os
import requests
import Operations
import time
import Objects
from random import randint
from dateutil.parser import parse

def game_info_extractor (year, game_num):
	'''
	Extract information about a game (attendance, home team, etc.) from an
	standard header on html report (via an xml tree) stored as a local file.
	Return a GameInfo object.
	'''

	file_path = "C:/Users/Ruben/Projects/HockeyScraper/Reports/" \
					+ year + "/PL02" + game_num + ".HTM"
	with open (file_path, 'r') as temp_file:
		read_data = temp_file.read()
		
	tree = html.fromstring(read_data)
	
	away_info_raw = tree.xpath(
		'//tr/td[@valign="top"]/table[@id="Visitor"]'
		)[0]
	away_score = away_info_raw.xpath(
		'.//td[@style="font-size: 40px;font-weight:bold"]/text()'
		)[0]
	away_team_raw = away_info_raw.xpath(
		'.//td[@style="font-size: 10px;font-weight:bold"]/text()'
		)[0]
	away_team_game_nums = away_info_raw.xpath(
		'.//td[@style="font-size: 10px;font-weight:bold"]/text()'
		)[1]

	home_info_raw = tree.xpath(
		'//tr/td[@valign="top"]/table[@id="Home"]'
		)[0]
	home_score = home_info_raw.xpath(
		'.//td[@style="font-size: 40px;font-weight:bold"]/text()'
		)[0]
	home_team_raw = home_info_raw.xpath(
		'.//td[@style="font-size: 10px;font-weight:bold"]/text()'
		)[0]
	home_team_game_nums = home_info_raw.xpath(
		'.//td[@style="font-size: 10px;font-weight:bold"]/text()'
		)[1]

	game_info_raw = tree.xpath(
		'//tr/td/table[@id="GameInfo"]'
		)[0]
	game_date = game_info_raw.xpath(
		'.//td[@style="font-size: 10px;font-weight:bold"]/text()'
		)[0]
	attendance_arena = game_info_raw.xpath(
		'.//td[@style="font-size: 10px;font-weight:bold"]/text()'
		)[1]
	game_start_end = game_info_raw.xpath(
		'.//td[@style="font-size: 10px;font-weight:bold"]/text()'
		)[2]
	game_num = game_info_raw.xpath(
		'.//td[@style="font-size: 10px;font-weight:bold"]/text()'
		)[3]
	report_type = game_info_raw.xpath(
		'.//td[@style="font-size: 10px;font-weight:bold"]/text()'
		)[4]

	away_team = Operations.team_name_to_acronym (away_team_raw)
	home_team = Operations.team_name_to_acronym (home_team_raw)

	return Objects.GameInfo (
		game_date, attendance_arena, game_start_end, game_num,\
		away_score, away_team, away_team_game_nums,\
		home_score, home_team, home_team_game_nums
		)

def game_summary_extractor (year, game_num):
	'''
	Extract information from game summery html file to run tests
	'''

	tree = Operations.germinate_report_seed (year, game_num, "GS", '02')

	tables = tree.xpath('//table[@id="MainTable"]/tr/td/table')
	
	goals_raw = tables[2].xpath('.//tr')

	# Skipping first item in iterable roster
	iter_goals = iter(tables[2].xpath('.//tr'))
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

	penalties_raw = tables[4].xpath('./tr/td/table/tr/td/table/tr/td/table')
	
	home_penalties = GameSummary.chop_penalties_branch (penalties_raw[0])
	away_penalties = GameSummary.chop_penalties_branch (penalties_raw[1])

	byperiod_raw = tables[5].xpath('./tr/td/table/tr/td/table')
	
	away_periods = GameSummary.chop_byperiod_branch (byperiod_raw[0].xpath('./tr'))
	home_periods = GameSummary.chop_byperiod_branch (byperiod_raw[1].xpath('./tr'))

	powerplay_raw = tables[6].xpath('./tr/td/table/tr/td/table')
	evenstrength_raw = tables[7].xpath('./tr/td/table/tr/td/table')

	away_powerplay = GameSummary.chop_situation_branch (powerplay_raw[0])
	home_powerplay = GameSummary.chop_situation_branch (powerplay_raw[1])
	away_evenstrength = GameSummary.chop_situation_branch (evenstrength_raw[0])
	home_evenstrength = GameSummary.chop_situation_branch (evenstrength_raw[1])

	for item in home_powerplay:
		print item
	#print etree.tostring (powerplay_raw[0], pretty_print = True)
		

def playbyplay_extractor (year, game_num):
	"""
	Extract play-by-play information from a html file on the
	local machine (in the form of events)
	"""

	tree = Operations.germinate_report_seed(year,game_num,'PL','02')

	events = [] # empty list for holding unspecified events
	
	for item in tree.xpath('//table/tr[@class="evenColor"]'):
	#for x in range (116, 120):
	#   item = tree.xpath('//table/tr[@class="evenColor"]') [x]
					
		event_raw = item.xpath('./td/text()')

		num = unicode(event_raw[0])
		per_num = unicode(event_raw[1])
		strength = unicode(event_raw[2])
		time = unicode(event_raw[3])
		event_type = unicode(event_raw[5])
		description = unicode(event_raw[6])

		# Goals have an additional row in the description cell for assists
		if event_type == 'GOAL' and event_raw[7].find('Assist') != -1:
			description = unicode(" ".join(event_raw[6:8]))

		players_on_ice = item.xpath('./td/table')

		home_on_ice = []
		away_on_ice = []
			
		if len (players_on_ice) == 2:

			away_players_raw = players_on_ice[0].xpath ('.//font')
			for away_player in away_players_raw:
				position_name = away_player.xpath ('./@title')
				number = away_player.xpath ('./text()') [0]

				position, name = position_name[0].split(' - ')

				away_on_ice.append ([position, name, number])
			
			home_players_raw = players_on_ice[1].xpath ('.//font')
			for home_player in home_players_raw:
				position_name = home_player.xpath ('./@title')
				number = home_player.xpath ('./text()') [0]

				position, name = position_name[0].split(' - ')

				home_on_ice.append ([position, name, number])

		event = Objects.Event(
			num, per_num, strength, time, event_type, description,\
			away_on_ice, home_on_ice
			)
		
		events.append (event)	    
	return events

def event_object_extractor(event_index, event_list, game_personnel, away_team, home_team):
	'''
	Given a string that is the description of an event, return an object of
	that event containing all possible data
	'''
	event = event_list[event_index]

	description_raw = event.description.split ()

	if event.event_type == 'PSTR':
		
		start_time = description_raw[-2]
		time_zone = description_raw[-1]

		return Objects.PeriodStart(
			event.num,\
			event.per_num,\
			event.strength,\
			event.time,\
			event.event_type,\
			event.description,\
			event.away_on_ice,\
			event.home_on_ice,\
			start_time,
			time_zone
			)
	elif event.event_type == 'FAC':
		
		zone = description_raw[2]
		winning_team = description_raw[0]

		anchor = description_raw.index('vs')

		away_team = description_raw[5]
		away_num = description_raw[6].strip('#')
		away_name = " ".join(description_raw[7:anchor])

		home_team = description_raw[anchor + 1]
		home_num = description_raw[anchor + 2].strip('#')
		home_name = " ".join(description_raw[anchor + 3:])

		if winning_team == away_team:
			losing_team = home_team
			winning_player = (away_num, away_name)
			losing_player = (home_num, home_name)
		else:
			losing_team = away_team
			winning_player = (home_num, home_name)
			losing_player = (away_num, away_name)

		return Objects.FaceOff(
			event.num,\
			event.per_num,\
			event.strength,\
			event.time,\
			event.event_type,\
			event.description,\
			event.away_on_ice,\
			event.home_on_ice,\
			zone,\
			winning_player,\
			losing_player,\
			winning_team,\
			losing_team
			)

	elif event.event_type == 'GIVE' or event.event_type == 'TAKE':

		zone = description_raw[-2]
		givetake_team = description_raw[0]
		givietake_num = description_raw[3].strip('#')

		anchor = Operations.index_containing_substring(description_raw, ',') + 1

		assert anchor != 0, "ERROR - Anchor not found"

		givetake_name = (" ".join(description_raw[4:anchor])).strip(',')

		givetake_player = (givietake_num, givetake_name)

		if event.event_type == 'GIVE':
			return Objects.Give(
				event.num,\
				event.per_num,\
				event.strength,\
				event.time,\
				event.event_type,\
				event.description,\
				event.away_on_ice,\
				event.home_on_ice,\
				zone,\
				givetake_player,\
				givetake_team
				)

		elif event.event_type == 'TAKE':
			return Objects.Take(
				event.num,\
				event.per_num,\
				event.strength,\
				event.time,\
				event.event_type,\
				event.description,\
				event.away_on_ice,\
				event.home_on_ice,\
				zone,\
				givetake_player,\
				givetake_team
				)

	elif event.event_type == 'SHOT':
		
		zone = description_raw[-4]
		distance = description_raw[-2]
		shot_type = description_raw[-5].strip(',')
		shooting_team = description_raw[0]
		shooting_num = description_raw[3].strip('#')

		anchor = Operations.index_containing_substring(description_raw, ',') + 1

		assert anchor != 0, "ERROR - Anchor not found"

		shooting_name = (" ".join(description_raw[4:anchor])).strip(',')

		shooting_player = (shooting_num, shooting_name)

		if shooting_team == away_team:
			blocking_on_ice = event.home_on_ice
			blocking_team = home_team
		elif shooting_team == home_team:
			blocking_on_ice = event.away_on_ice
			blocking_team = away_team
			
		for player in blocking_on_ice:
			if player[0] == 'Goalie':
				blocking_name = " ".join(player[1].split()[1:])
				blocking_num = player[2]

		blocking_player = (blocking_num, blocking_name)

		return Objects.Shot(
			event.num,\
			event.per_num,\
			event.strength,\
			event.time,\
			event.event_type,\
			event.description,\
			event.away_on_ice,\
			event.home_on_ice,\
			zone,\
			shot_type,\
			distance,\
			shooting_player,\
			blocking_player,\
			shooting_team,\
			blocking_team
			)

	elif event.event_type == 'BLOCK':
		
		zone = description_raw[-2]
		shot_type = description_raw[-3].strip(',')
		shooting_team = description_raw[0]
		shooting_num = description_raw[1].strip('#')

		anchor1 = Operations.index_containing_substring(description_raw, 'BLOCKED')
		anchor2 = Operations.index_containing_substring(description_raw, ',') + 1

		assert anchor1 != 0 and anchor2 != 0, "ERROR - Anchor not found"

		shooting_name = " ".join(description_raw[2:anchor1])

		shooting_player = (shooting_num, shooting_name)

		blocking_team = description_raw[anchor1 + 2]
		blocking_num = description_raw[anchor1 + 3].strip('#')
		blocking_name = (" ".join(description_raw[anchor1 + 4: anchor2])).strip (',')

		blocking_player = (blocking_num, blocking_name)

		return Objects.Block(
			event.num,\
			event.per_num,\
			event.strength,\
			event.time,\
			event.event_type,\
			event.description,\
			event.away_on_ice,\
			event.home_on_ice,\
			zone,\
			shot_type,\
			shooting_player,\
			blocking_player,\
			shooting_team,\
			blocking_team
			)

	elif event.event_type == 'MISS':
		
		distance = description_raw[-2]
		zone = description_raw[-4]
		shot_type = description_raw[-8].strip(',')
		shooting_team = description_raw[0]
		shooting_num = description_raw[1].strip('#')

		anchor = Operations.index_containing_substring(description_raw, ',') + 1
		
		assert anchor != 0, "ERROR - Anchor not found"

		miss_type = (" ".join(description_raw[anchor + 1:-4])).strip(',')

		shooting_name = (" ".join(description_raw[2:anchor])).strip(',')

		shooting_player = (shooting_num, shooting_name)

		if shooting_team == away_team:
			blocking_on_ice = event.home_on_ice
			blocking_team = home_team
		elif shooting_team == home_team:
			blocking_on_ice = event.away_on_ice
			blocking_team = away_team
			
		for player in blocking_on_ice:
			if player[0] == 'Goalie':
				blocking_name = " ".join(player[1].split()[1:])
				blocking_num = player[2]

		blocking_player = (blocking_num, blocking_name)

		return Objects.Miss(
			event.num,\
			event.per_num,\
			event.strength,\
			event.time,\
			event.event_type,\
			event.description,\
			event.away_on_ice,\
			event.home_on_ice,\
			zone,\
			shot_type,\
			miss_type,\
			distance,\
			shooting_player,\
			blocking_player,\
			shooting_team,\
			blocking_team
			)

	elif event.event_type == 'HIT':
		
		zone = description_raw[-2]
		hitting_team = description_raw[0]
		hitting_num = description_raw[1].strip('#')

		anchor1 = Operations.index_containing_substring(description_raw, 'HIT')
		anchor2 = Operations.index_containing_substring(description_raw, ',') + 1

		assert anchor1 != 0 and anchor2 != 0, "ERROR - Anchor not found"

		hitting_name = " ".join(description_raw[2:anchor1])

		hitting_player = (hitting_num, hitting_name)

		hit_team = description_raw[anchor1 + 1]
		hit_num = description_raw[anchor1 + 2].strip('#')
		hit_name = (" ".join(description_raw[anchor1 + 3: anchor2])).strip (',')

		hit_player = (hit_num, hit_name)

		return Objects.Hit(
			event.num,\
			event.per_num,\
			event.strength,\
			event.time,\
			event.event_type,\
			event.description,\
			event.away_on_ice,\
			event.home_on_ice,\
			zone,\
			hitting_player,\
			hit_player,\
			hitting_team,\
			hit_team
			)

	elif event.event_type == 'STOP':
		stopping_player = (None, None)
		stopping_team = None
		tv_timeout = 0
		timeout_caller = None

		description_raw = re.split('\W+', event.description)
		description_parsed = " ".join(description_raw)
		
		# Parse out 'TV TIMEOUT if not only item'
		if 'TV' in description_raw:
			tv_timeout = 1
			if len(description_raw) != 2:
				index = description_raw.index("TV")
				description_raw.pop (index)
				description_raw.pop (index)
				description_parsed = " ".join(description_raw)

		if 'HOME' in description_raw:
			timeout_caller = game_personnel.home_coach.full_name()
		elif 'VISITOR' in description_raw:
			timeout_caller = game_personnel.away_coach.full_name()
		
		if "GOALIE" in description_raw or 'FROZEN' in description_raw:
			counter = event_index + 1
			next_event = event_list[counter]

			# Sometimes events are logged (penalties, shots, etc) are logged
			# between STOP and subsequent FAC event
			while next_event.event_type != 'FAC':
				counter += 1
				next_event = event_list[counter]

			next_description_raw = next_event.description.split ()
			winning_team = next_description_raw[0]
			winning_zone = next_description_raw[2]

			stopping_team, stopping_on_ice = Operations.team_responsible(
				winning_zone, winning_team, away_team, home_team, event
				)

			for player in stopping_on_ice:
				if player[0] == 'Goalie':
					stopping_name = " ".join(player[1].split()[1:])
					stopping_num = player[2]
					stopping_player = (stopping_num, stopping_name)


		elif "ICING" in description_raw:
			next_event = event_list[event_index + 1]
			next_description_raw = next_event.description.split ()
			winning_team = next_description_raw[0]
			winning_zone = next_description_raw[2]

			stopping_team, stopping_on_ice = Operations.team_responsible(
				winning_zone, winning_team, away_team, home_team, event
				)

		return Objects.Stop(
			event.num,\
			event.per_num,\
			event.strength,\
			event.time,\
			event.event_type,\
			event.description,\
			event.away_on_ice,\
			event.home_on_ice,\
			description_parsed,\
			stopping_player,\
			stopping_team,\
			tv_timeout,\
			timeout_caller
			)

	elif event.event_type == 'GOAL':

		prim_assist_player = (None, None)
		sec_assist_player = (None, None)

		scoring_team = description_raw[0]
		scoring_num = description_raw[1].strip('#')

		anchor1 = Operations.index_containing_substring(description_raw, ',') + 1
		anchor2 = Operations.index_containing_substring(description_raw[anchor1:], ',') + 1
		anchor3 = Operations.index_containing_substring(description_raw, 'ft.')

		scoring_name = (" ".join(description_raw[2:anchor1]))[:-4]
		scoring_player = (scoring_num, scoring_name)

		shot_type = (" ".join(description_raw[anchor1:anchor1+anchor2])).strip(',')
		distance = description_raw[anchor3 - 1]
		zone = description_raw[anchor3 - 3]
		
		if 'Assist:' in description_raw:
			anchor4 = Operations.index_containing_substring(description_raw, 'Assist:') + 1
			
			prim_assist_num = description_raw[anchor4].strip('#')
			prim_assist_name = (" ".join(description_raw[anchor4 + 1:]))[:-3]
			prim_assist_player = (prim_assist_num, prim_assist_name)
			
		elif 'Assists:' in description_raw:
			anchor4 = Operations.index_containing_substring(description_raw, 'Assists:') + 1
			anchor5 = Operations.index_containing_substring(description_raw, ';') + 1
			
			prim_assist_num = description_raw[anchor4].strip('#')
			prim_assist_name = (" ".join(description_raw[anchor4 + 1:anchor5]))[:-4]
			prim_assist_player = (prim_assist_num, prim_assist_name)

			sec_assist_num = description_raw[anchor5].strip('#')
			sec_assist_name = (" ".join(description_raw[anchor5 + 1:]))[:-3]
			sec_assist_player = (sec_assist_num, sec_assist_name)
			
		if scoring_team == home_team:
			defending_on_ice = event.away_on_ice
			defending_team = away_team
		elif scoring_team == away_team:
			defending_on_ice = event.home_on_ice
			defending_team = home_team

		for player in defending_on_ice:
			if player[0] == 'Goalie':
				goalie_name = " ".join(player[1].split()[1:])
				goalie_num = player[2]
				goalie = (goalie_num, goalie_name)
		print goalie

		return Objects.Goal(
			event.num,\
			event.per_num,\
			event.strength,\
			event.time,\
			event.event_type,\
			event.description,\
			event.away_on_ice,\
			event.home_on_ice,\
			zone,\
			shot_type, \
			distance, \
			scoring_player, \
			scoring_team, \
			prim_assist_player, \
			sec_assist_player,\
			goalie,\
			defending_team
			)

	elif event.event_type == 'PENL':

		description_raw = re.split('\W+', event.description)
		#print description_raw
		penalized_team = description_raw[0]
		if penalized_team == home_team:
			drawing_team = away_team
		elif penalized_team == away_team:
			drawing_team = home_team

		penalized_num = description_raw[1].strip('#')

		for index, item in enumerate(description_raw[2:]):
			if not str(item).isupper():
				anchor1 = index + 2
				break

		penalized_name = " ".join(description_raw[2:anchor1])
		penalized_player = (penalized_num, penalized_name)
		
		anchor2 = description_raw.index('min') -1
		length = description_raw [anchor2]
		penalty_type = " ".join(description_raw[anchor1:anchor2])

		anchor3 = description_raw.index('Zone') - 1
		zone = description_raw [anchor3]

		try:
			anchor4 = description_raw.index('By') + 1
			drawing_num = description_raw [anchor4 + 1].strip('#')
			drawing_name = " ".join(description_raw [anchor4 + 2:]).strip('#')
			drawing_player = (drawing_num, drawing_name)

		except ValueError:
			drawing_player = (None, None)

		return Objects.Penalty(
			event.num,\
			event.per_num,\
			event.strength,\
			event.time,\
			event.event_type,\
			event.description,\
			event.away_on_ice,\
			event.home_on_ice,\
			zone,\
			penalty_type,\
			length,\
			penalized_player,\
			drawing_player,\
			penalized_team,\
			drawing_team
			)
			
def get_playerid(first_name, last_name):
	'''
	given a player's first name and last name, find their playerid in db
	'''

	conn = sqlite3.connect ('nhl.db')
	c = conn.cursor ()
	c.execute("SELECT * FROM all_players WHERE first_name = ? AND last_name = ?",\
		(first_name, last_name,))
	temp_return = c.fetchall()

	assert len(temp_return) == 1, "ERROR: more than one player with that first/last name combo"
	
	conn.commit ()
	conn.close()

	return temp_return [0][0]

def game_personnel_creator (year, game_num):
	"""
	Extract roster information from a html file on the
	local machine and create database entries
	"""
	'''
	file_path = "C:/Users/Ruben/Projects/HockeyScraper/Reports/" +\
					year + "/RO02" + game_num + ".HTM"

	with open (file_path, 'r') as temp_file:
		read_data = temp_file.read()
	'''
	tree = Operations.germinate_report_seed (year, game_num, "RO", '02')#html.fromstring(read_data)

	tables = tree.xpath('//table//table//table//table')

	away_roster = ind_roster_grabber (tables, 'visitor')
	home_roster = ind_roster_grabber (tables, 'home')
	
	away_coach, home_coach = coach_grabber(tables)
	
	referees, linesmen = officials_grabber (tables)

	return Objects.GamePersonnel (away_roster, home_roster, away_coach, home_coach, referees, linesmen)

def coach_grabber (tree):
	'''
	Grab away and home coaches from an xml tree (of an html roster report) and
	return them as a tuple of Coach objects
	'''

	away_coach_raw = tree[9].xpath('./tr/td/text()')[0]
	away_coach = Objects.Coach(
		first_name = away_coach_raw.split()[0],
		last_name = " ".join(away_coach_raw.split()[1:])
		)

	home_coach_raw = tree[10].xpath('./tr/td/text()')[0]
	home_coach = Objects.Coach(
		first_name = home_coach_raw.split()[0],
		last_name = " ".join(home_coach_raw.split()[1:])
		)
	#print away_coach, home_coach

	return away_coach, home_coach

def officials_grabber (tree):
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
			temp_official = Objects.Referee (num, first_name, last_name)
			referees.append (temp_official)
		else:
			temp_official = Objects.Linesman (num, first_name, last_name)
			linesmen.append (temp_official)
		# print temp_official

	return referees, linesmen

	
		
def ind_roster_grabber (tree, team):
	"""
	Extract indivudal information from an xml tree and return list 
	of roster objects. team is home or away
	"""
	roster_objects = []

	if team == 'home':
		x, y = 6, 8
	else:
		x, y = 5, 7

	# Skipping first item in iterable roster
	iter_roster = iter(tree[x].xpath('./tr'))
	next (iter_roster)

	for item in iter_roster:
		temp_player = Objects.Roster()

		temp_player.num = item.xpath('./td/text()')[0]
		temp_player.pos = item.xpath('./td/text()')[1]
		temp_name_raw = item.xpath('./td/text()')[2]

		temp_starting = item.xpath ('./td/@class')[0]
		if 'bold' in temp_starting:
			temp_player.starting = 1
			
		temp_name_raw_split = temp_name_raw.split()
		temp_player.first_name = temp_name_raw_split[0]

		if '(A)' in temp_name_raw_split:
			temp_player.A_C = 'A'
			temp_name_raw_split.pop (-1)
		elif '(C)' in temp_name_raw_split:
			temp_player.A_C = 'C'
			temp_name_raw_split.pop (-1)

		temp_player.last_name = " ".join(temp_name_raw_split[1:])

		temp_player.playerid = get_playerid (temp_player.first_name, temp_player.last_name)

		# print temp_player
		roster_objects.append(temp_player)
		#print etree.tostring (item, pretty_print = True)

	iter_scratches = iter(tree[y].xpath('./tr'))
	next (iter_scratches)

	for item in iter_scratches:
		temp_player = Objects.Roster()

		temp_player.scratch = 1
		temp_player.num = item.xpath('./td/text()')[0]
		temp_player.pos = item.xpath('./td/text()')[1]
		temp_name_raw = item.xpath('./td/text()')[2]

		temp_name_raw_split = temp_name_raw.split()
		temp_player.first_name = temp_name_raw_split[0]
		temp_player.last_name = " ".join(temp_name_raw_split[1:])

		temp_player.playerid = get_playerid (temp_player.first_name, temp_player.last_name)

		# print temp_player
		roster_objects.append(temp_player)

	return roster_objects
	
	'''
	for item in tree.xpath('//table//table//table//table'):
		event_raw = item.xpath('./td/text()')
		print etree.tostring (item, pretty_print = True)
	'''

	

if __name__ == '__main__':
	'''
	gameinfo_temp = game_info_extractor	("20152016", "0003")
	gamepersonnel_temp = game_personnel_creator ("20152016", "0003")
	events = playbyplay_extractor ("20152016", "0003")
	
	for x in range (0, 300):
		
		event_object_extractor (x, events, gamepersonnel_temp, gameinfo_temp.away_team, gameinfo_temp.home_team)
	'''

	game_summary_extractor ("20152016", "0003")