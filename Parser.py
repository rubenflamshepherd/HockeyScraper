'''
Parse information from html reports stored as local files using xml trees
'''

from lxml import html, etree
import sqlite3
import os
import requests
import Operations
import time
from Objects import Event, Roster, Coach, Referee, Linesman, PeriodStart, FaceOff
from random import randint
from dateutil.parser import parse

def game_info_extractor (year, game_num):
	'''
	Extract information about a game (attendance, home team, etc.) from an
	standard header on html report (via an xml tree) stored as a local file.
	'''

	file_path = "C:/Users/Ruben/Projects/HockeyScraper/Reports/" + year + "/PL02" + game_num + ".HTM"
	with open (file_path, 'r') as temp_file:
		read_data = temp_file.read()
		
	tree = html.fromstring(read_data)
	
	away_info_raw = tree.xpath('//tr/td[@valign="top"]/table[@id="Visitor"]')[0]
	away_score = away_info_raw.xpath('.//td[@style="font-size: 40px;font-weight:bold"]/text()')[0]
	away_team = away_info_raw.xpath('.//td[@style="font-size: 10px;font-weight:bold"]/text()')[0]
	away_team_game_nums = away_info_raw.xpath('.//td[@style="font-size: 10px;font-weight:bold"]/text()')[1]

	home_info_raw = tree.xpath('//tr/td[@valign="top"]/table[@id="Home"]')[0]
	home_score = home_info_raw.xpath('.//td[@style="font-size: 40px;font-weight:bold"]/text()')[0]
	home_team = home_info_raw.xpath('.//td[@style="font-size: 10px;font-weight:bold"]/text()')[0]
	home_team_game_nums = home_info_raw.xpath('.//td[@style="font-size: 10px;font-weight:bold"]/text()')[1]

	game_info_raw = tree.xpath('//tr/td/table[@id="GameInfo"]')[0]
	game_date = game_info_raw.xpath('.//td[@style="font-size: 10px;font-weight:bold"]/text()')[0]
	attendance_arena = game_info_raw.xpath('.//td[@style="font-size: 10px;font-weight:bold"]/text()')[1]
	game_start_end = game_info_raw.xpath('.//td[@style="font-size: 10px;font-weight:bold"]/text()')[2]
	game_num = game_info_raw.xpath('.//td[@style="font-size: 10px;font-weight:bold"]/text()')[3]
	report_type = game_info_raw.xpath('.//td[@style="font-size: 10px;font-weight:bold"]/text()')[4]
	
	print game_date, attendance_arena, game_start_end, game_num, report_type
	print away_score, away_team, away_team_game_nums
	print home_score, home_team, home_team_game_nums
	

def playbyplay_extractor (year, game_num):
	"""
	Extract play-by-play information from a html file on the
	local machine (in the form of events)
	"""
	
	file_path = "C:/Users/Ruben/Projects/HockeyScraper/Reports/" + year + "/PL02" + game_num + ".HTM"
	with open (file_path, 'r') as temp_file:
		read_data = temp_file.read()
	tree = html.fromstring(read_data)

	events = []
	
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
			
	    #print away_on_ice
	    #print home_on_ice

	    event = Event(num, per_num, strength, time, event_type, description, away_on_ice, home_on_ice)
	    #print num , per_num , strength , time, event_type, description
	    
	    events.append (event)	    
	return events

def event_decription_extractor(event):
	'''
	Given a string that is the discritpion of an event, return an object of
	that event containing all possible data
	'''
	
	description_raw = event.description.split ()

	if event.event_type == 'PSTR':
		
		start_time = description_raw[-2]
		time_zone = description_raw[-1]
		
		return PeriodStart(
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

		return FaceOff(
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

def game_personel_creator (year, game_num):
	"""
	Extract roster information from a html file on the
	local machine and create database entries
	"""
	
	file_path = "C:/Users/Ruben/Projects/HockeyScraper/Reports/" +\
					year + "/RO02" + game_num + ".HTM"

	with open (file_path, 'r') as temp_file:
		read_data = temp_file.read()

	tree = html.fromstring(read_data)

	tables = tree.xpath('//table//table//table//table')

	away_roster = ind_roster_grabber (tables, 'visitor')
	home_roster = ind_roster_grabber (tables, 'home')
	
	away_coach, home_coach = coach_grabber(tables)
	
	officials_grabber (tables)

def coach_grabber (tree):
	'''
	Grab away and home coaches from an xml tree (of an html roster report) and
	return them as a tuple of Coach objects
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
			temp_official = Referee (num, first_name, last_name)
			referees.append (temp_official)
		else:
			temp_official = Linesman (num, first_name, last_name)
			linesmen.append (temp_official)
		# print temp_official

	return referees, linesmen

	
		
def ind_roster_grabber (tree, team):
	"""
	Extract indivudal information from a xml tree and return list 
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
		temp_player = Roster()

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
		temp_player = Roster()

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
	# grabber ("20142015", 1, 110, '02')
	# print checker ('http://www.nhl.com/scores/htmlreports/20142015/PL021230.HTM')
	#game_info_scraper ("20142015", "0001")
	
	events = playbyplay_extractor ("20142015", "0001")
	for x in range (0,20):
		print events[x]
		print event_decription_extractor (events[x])
		print events[x].away_on_ice
		print events[x].home_on_ice
	

	# game_personel_creator ("20142015", "0001")
	

