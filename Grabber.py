'''
Grab information from nhl.com that does not need to be stored in a local file
Use Creater.py to throw information in sql databases for storage
'''

import string
import sqlite3
import time
from lxml import html, etree
import requests
from dateutil.parser import parse
import Operations
from random import randint

class Player(object):

	def __init__ (self):

		self.playerid = None
		self.current_num = None
		self.pos = None
		self.height = None
		self.weight = None
		self.hand = None # Because can be shoots OR catches
		self.current_team = None
		self.draft_team = None
		self.draft_year = None
		self.draft_round = None
		self.draft_overall = None
		self.twitter = None
		self.website = None
		self.regular_seasons = None
		self.playoff_seasons = None

	def __str__ (self):

		num = ("#" + str(self.current_num).encode('utf-8')).ljust(4)
		pos = ("Pos " + str(self.pos).encode('utf-8')).ljust(6)
		height = (" Hgt " + str(self.height).encode('utf-8')).ljust(9)
		weight = (str(self.weight).encode('utf-8') + ' lbs').ljust(8)
		hand = ("Shts " + str(self.hand).encode('utf-8')).ljust(12)
		current_team = ("Tm " \
			+ str(self.current_team).encode('utf-8') + '\n'
			).ljust(7)
		drafted = ("Drafted " + str(self.draft_year) + ' '\
			+ str(self.draft_overall).encode('utf-8') + ' ' \
			+ " overall in " + str(self.draft_round) + ' rnd by '\
			+ str(self.draft_team) + '\n'
			).ljust(20)
		twitter = ("Twt " + str(self.twitter).encode('utf-8')).ljust(10)
		website = (" Site " + str(self.website).encode('utf-8')).ljust(20)

		return num + pos + height + weight + hand + current_team \
			+ drafted + twitter + website

class Season(object):

	def __init__ (self, year, team, games_played):

		self.year = year
		self.team = team
		self.games_played = games_played

class GoalieSeason(Season):

	def __init__ (self, year, team, games_played, wins, loses, ties,
		overtime_loses, shutouts, goals_against, shots_against,
		save_percentage, gaa, minutes_played):

		Season.__init__(self, year, team, games_played)
		self.wins = wins
		self.loses = loses
		self.ties = ties
		self.overtime_loses = overtime_loses
		self.shutouts = shutouts
		self.goals_against = goals_against
		self.shots_against = shots_against
		self.save_percentage = save_percentage
		self.gaa = gaa
		self.minutes_played = minutes_played

	def __str__(self):

		year = ("\n" + self.year).ljust(11)
		team = (self.team).ljust(12)
		games_played = ("GP " + str(self.games_played)).ljust(6)
		wins = ("W " + str(self.wins)).ljust(5)
		loses = ("L " + str(self.loses)).ljust(5)
		ties = ("T " + str(self.ties)).ljust(7)
		overtime_loses = ("OT " + str(self.overtime_loses)).ljust(8)
		shutouts = ("SO " + str(self.shutouts)).ljust(6)
		goals_against = ("GA " + str(self.goals_against)).ljust(8)
		shots_against = ("SA " + str(self.shots_against)).ljust(9)
		save_percentage = ("SA " + str(self.save_percentage)).ljust(8)
		gaa = ("GAA " + str(self.gaa)).ljust(9)
		minutes_played = ("Min " + str(self.minutes_played)).ljust(10)

		
		return year + team + games_played + wins + loses + ties \
			+ overtime_loses + shutouts + goals_against + save_percentage \
			+ shots_against + gaa + minutes_played
		

class PlayerSeason(Season):

	def __init__ (self, year, team, games_played, goals, assists, points, 
		plus_minus, pim, powerplay_goals, shorthanded_goals, gamewinning_goals,
		shots, shooting_percentage):

		Season.__init__(self, year, team, games_played)
		self.goals = goals
		self.assists = assists
		self.points = points
		self.plus_minus = plus_minus
		self.pim = pim
		self.powerplay_goals = powerplay_goals
		self.shorthanded_goals = shorthanded_goals
		self.gamewinning_goals = gamewinning_goals
		self.shots = shots
		self.shooting_percentage = shooting_percentage

	def __str__(self):

		year = ("\n" + self.year).ljust(11)
		team = (self.team).ljust(12)
		games_played = ("GP " + str(self.games_played)).ljust(6)
		goals = ("G " + str(self.goals)).ljust(5)
		assists = ("A " + str(self.assists)).ljust(5)
		points = ("P " + str(self.points)).ljust(7)
		plus_minus = ("+/- " + str(self.plus_minus)).ljust(8)
		pim = ("PIM " + str(self.pim)).ljust(6)
		powerplay_goals = ("PPG " + str(self.powerplay_goals)).ljust(8)
		shorthanded_goals = ("SHG " + str(self.shorthanded_goals)).ljust(9)
		gamewinning_goals = ("GWG " + str(self.gamewinning_goals)).ljust(8)
		shots = ("Sh " + str(self.shots)).ljust(9)
		shooting_percentage = ("S% " + str(self.shooting_percentage)).ljust(10)

		
		return year + team + games_played + goals + assists + points \
			+ plus_minus + pim + powerplay_goals + shorthanded_goals \
			+ gamewinning_goals + shots + shooting_percentage

def check_num_playerdb():
	'''
	Go to a random page of the nhl.com table containing all players and compare
	number currently in the table to the number previously grabbed
	Return True if numbers equal, False if they don't
	'''

	page_num = randint(1,70)
	url = "http://www.nhl.com/ice/playersearch.htm?position=S&pg=%d"%page_num
	page = requests.get (url)
	tree = html.fromstring (page.text)
	check = tree.xpath ('//div[@class="resultCount"]/text()')[0]
	num_online = check.split()[2]

	conn = sqlite3.connect ('nhl.db')
	c = conn.cursor ()
	c.execute ("SELECT count(*) FROM all_players")
	num_offline = c.fetchone()[0]
	conn.close()

	return num_offline == num_online
	

def harvest_all_players():
	'''
	Grab basic information from EVERY player to player in the NHL from
	nhl.com (all players table) and store in database 
	'''
	# Trackinf time it takes function to run
	start_time = time.time()

	# Create database, connection and cursor
	conn = sqlite3.connect ('nhl.db')
	c = conn.cursor ()
	
	c.execute ('DROP TABLE IF EXISTS all_players')
	c.execute(
		'CREATE TABLE all_players (\
		playerid INTEGER primary key, first_name TEXT,\
		last_name TEXT, position TEXT, current_team TEXT,\
		birth_date TEXT, birth_country TEXT, birth_state TEXT,\
		birth_city TEXT\
		)'
	)
			
	# variables tracking db changes: errors/exisiing file, additions
	sql_errors = []
	sql_additions = 0
	
	# Grabing player ids from all players ever
	page_num = randint(1,370)
	checked_pages = []
	
	#while no_results == False:
	while len (checked_pages) < 370:
		page_num = randint(1,370)
		while page_num in checked_pages:
			page_num = randint(1,370)
		checked_pages.append (page_num)
		print checked_pages
		url = "http://www.nhl.com/ice/playersearch.htm?position=S&pg=%d"%page_num
		
		delay = randint(1,15)/60.0 # Disguise parsing signature from servers
		time.sleep (delay)
		
		page = requests.get (url)
		tree = html.fromstring (page.text)

		# Check to see if page falls inside rage of those containing
		# part of player info table (364 pages as of 9/12/15)
		check = tree.xpath (
			'//div[@style="padding: 6px; font-weight: bold;"]'
			)

		if len(check) == 1:
			pass
		else:
			page_num +=1
			players = tree.xpath('//table[@class="data playerSearch"]/tbody/tr')

			for player in players:
				tags = player.xpath ('.//td')

				#Parsing first, last name and position
				name_position_raw = tags[0].xpath('.//a/text()')[0]\
					.rstrip()
				position = name_position_raw.split()[-1].strip('()')

				# Differentiating the first name from the last name
				name_raw = name_position_raw.split()[:-1]
				for x in range (0, len (name_raw)):
					if name_raw[x].find (",") != -1:
						name_raw[x] = name_raw[x].strip (",")
						index = x + 1 #last index not inclusive

				first_name = " ".join (name_raw[index:]) 
				last_name = " ".join (name_raw[:index]) 

				# Parsing the unique player identifier (playerid)
				playerid_raw = tags[0].xpath('.//a/@href')[0].rstrip()
				equal_index = playerid_raw.find('=') + 1
				playerid = int(playerid_raw [equal_index:])

				# Parsing the players current team
				try:
					current_team = tags[1].xpath('.//a/text()')[0]\
						.rstrip()
				except IndexError:
					current_team = None

				# Parsing player birthdate
				try:
					birthdate_raw = tags[2]\
						.xpath('.//nobr/text()')[0].rstrip()
					birth_date = parse(birthdate_raw)
				except IndexError:
					birth_date = None

				# Parsing the players birthplace
				birthplace_raw = tags[3].xpath('.//text()')[0]\
					.split (",")

				# Parsing birthplace info
				birth_country = birthplace_raw[-1].strip()
				if birth_country == "-":
					birth_country = None
					birth_city = None
					birth_state = None					
				else:
					birth_city = birthplace_raw[0]
					if len (birthplace_raw) == 3:
						birth_state = birthplace_raw[1].strip()
					else:
						birth_state = None

				# Insert records into db if they don't already exist
				insert_statement = "INSERT INTO all_players VALUES\
					(%s, \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \
					\"%s\",\"%s\", \"%s\")"\
				%(playerid, first_name, last_name, position,\
				  current_team, birth_date, birth_country,\
				  birth_state, birth_city
				  )
				
				try:
					c.execute(insert_statement)
					print "ID %s added to db" %playerid
					sql_additions +=1
				except sqlite3.IntegrityError:
					print "ERROR: ID %s already exists\
						in primary key column"%playerid
					sql_errors.append (playerid)

			print url
		
	conn.commit ()
	conn.close()

	total_time = time.time() - start_time
	print "%0.2fs - total time taken" %total_time
	print str(sql_additions), " - records imported"
	print str(len (sql_errors)), " - records already saved ('errors')"

def active_players_scraper ():
	'''
	Parse through table of active nhl players on nhl.com and update
	records of players present in all_players (db) 
	'''

	# Tracking time it takes function to run
	start_time = time.time()

	# Create database, connection and cursor
	conn = sqlite3.connect ('nhl.db')
	c = conn.cursor ()
	
	# variables tracking that db changes: errors/exisiing file, additions
	sql_errors = []
	records_updated = 0
	
	# Grabing player ids from all players ever
	no_results = False # variable for checking that page has results
	checked_pages = []
	
	for letter in string.ascii_uppercase:
		page_num = 1
		no_results = False

		while no_results == False:
						
			url = "http://www.nhl.com/ice/playersearch.htm?letter=%s&pg=%d"\
				%(letter, page_num)
			delay = randint(1,15)/60.0 # Disguise parsing signature from nhl
			page = requests.get (url)
			tree = html.fromstring (page.text)

			check = tree.xpath (
				'//div[@style="padding: 6px; font-weight: bold;"]'
				)
			print url

			if len(check) == 1:
				no_results = True
			else:				
				page_num +=1
				players = tree.xpath(
					'//table[@class="data playerSearch"]/tbody/tr'
					)

				for player in players:
					tags = player.xpath ('.//td')

					# Parsing the unique player identifier (playerid)
					playerid_raw = tags[0].xpath('.//a/@href')[0].rstrip()
					equal_index = playerid_raw.find('=') + 1
					playerid = int(playerid_raw [equal_index:])

					# Parsing the players current team
					try:
						current_team = tags[1].xpath('.//a/text()')[0].rstrip()
					except IndexError:
						current_team = None

					# Inserting records into db if they don't already exist
					update_statement = "UPDATE all_players\
						SET currently_active = 1, current_team = '%s'\
						WHERE playerid =%s" %(current_team, playerid)
					
					c.execute(update_statement)
					records_updated += 1
					
	conn.commit ()
	conn.close()

	total_time = time.time() - start_time
	print "%0.2fs - total time taken" %total_time
	print str(records_updated), " - records updated"


def tombstone_scraper (tree):
	'''
	Using passed xml tree, grab data from player tombstone
	'''

	temp_player = Player () # Container for player information
	
	info_raw = tree.xpath('//div[@id="tombstone"]/div/table//tr/td/text()')
	website_raw = tree.xpath('//div[@id="tombstone"]//div[@id="playerSite"]/a/@href')
	position_raw = tree.xpath('//div[@id="tombstone"]/div/div/span/text()')
	twitter_raw = tree.xpath('//div[@id="tombstone"]/div/table/tr/td/a/@href')
	team_pos_raw = tree.xpath('//div[@id="tombstone"]/div/div[@style="float: left; margin-left: 6px; font-weight: bold; color: #999;"]')
	team_raw = team_pos_raw[0].xpath ('./a/text()')
	pos_raw = team_pos_raw[0].xpath ('./span/text()')
	
	info_stripped = [x.strip() for x in info_raw]
	info_iter = iter(info_stripped)
	for item in info_iter:
		if item == "NUMBER:":
			temp_player.current_num = next(info_iter)
		elif item == "HEIGHT:":
			height_raw = next(info_iter).split ("\' ")
			temp_player.height = height_raw[0] + ',' + height_raw[1].strip('"')
		elif item == "WEIGHT:":
			temp_player.weight = next(info_iter)
		elif item == "DRAFTED:":
			temp_player.draft_team = next(info_iter).strip('/').strip().strip()
		elif item == "Shoots:":
			temp_player.hand = next(info_iter)
		elif item == "Catches:":
			temp_player.hand = next(info_iter)[0]
		elif item == "ROUND:":
			temp_player.draft_round = next(info_iter)
			temp_player.draft_overall = next(info_iter).strip('()')

	try:
		temp_player.website = website_raw [0]
	except IndexError:
		pass
	try:
		temp_player.pos = position_raw [0][0]
	except IndexError:
		pass
	try:
		temp_player.current_team = Operations.team_name_to_acronym(team_raw[0])
	except IndexError:
		pass
	try:
		temp_player.pos = pos_raw [0]
	except IndexError:
		pass

	for item in twitter_raw:
		if item.find ("/ice/draftsearch.htm?team=") != -1:
			temp_player.draft_year = item.split ('=') [-1]
		elif item.find ("https://twitter.com/") != -1:
			temp_player.twitter = item.split('/') [-1]
	print temp_player
	return temp_player

def prune_season_field(field):
	'''
	Given a field (cell in a season as xml 'sapling'),
	return the contents of that field
	'''

	if len(field.xpath('./span')) == 1:
		temp_item = field.xpath('./span/text()')[0].strip()
	elif len(field.xpath('./a')) == 1:
		temp_item = field.xpath('./a/text()')[0]
	else:
		try:
			temp_item = field.xpath('./text()')[0].strip()
			if temp_item == '':
				temp_item = None
			
		except IndexError:
			temp_item = None

	return temp_item

def career_scraper(pos, seasons, season_type):
	'''
	Takes rows (seasons) from statistical table from player page on
	nhl.com and return consolidated table. Tables summarize either regular 
	season or playoff statistics
	season_type = 0/1 for regular/playoff season
	'''
	seasons_pruned = []

	if pos == 'G':
		for row_index, season in enumerate(seasons):
			season_fields = season.xpath('./td')

			# Grabbbing row (season) information 
			# Avoiding first and last (Header+Total rows)
			if row_index != 0 and row_index != len(seasons)-1:
				# Iterating through fields in season
				field_index = 0
				# No enumerate because playoffs and reg season are different
				for field in season_fields:
					if field_index == 0:
						year = prune_season_field (field)
					elif field_index == 1:
						team = prune_season_field (field)
					elif field_index == 2:
						games_played = prune_season_field (field)						
					elif field_index == 3:
						wins = prune_season_field (field)
					elif field_index == 4:
						loses = prune_season_field (field)
					elif field_index == 5 and season_type == 0:
						ties = prune_season_field (field)
						if ties == '-': #Tie entry for modern season (not None)
							ties = None
					elif field_index == 5 and season_type == 1:
						ties = None
						overtime_loses = None
						shutouts = prune_season_field (field)
						field_index += 2
					elif field_index == 6 and season_type == 0:
						overtime_loses = prune_season_field (field)
					elif field_index == 7 and season_type == 0:
						shutouts = prune_season_field (field)
					elif field_index == 8:
						goals_against = prune_season_field (field)
					elif field_index == 9:
						shots_against = prune_season_field (field)
					elif field_index == 10:
						save_percentage = prune_season_field (field)
					elif field_index == 11:
						gaa = prune_season_field (field)
					elif field_index == 12:
						minutes_played = prune_season_field (field)

					field_index += 1
				
				seasons_pruned.append (GoalieSeason (
					year, team, games_played, wins, loses, ties, 
					overtime_loses, shutouts, goals_against, shots_against,
					save_percentage, gaa, minutes_played))

	elif pos != 'G':
		for row_index, season in enumerate(seasons):
			season_fields = season.xpath('./td')

			# Grabbbing row (season) information 
			# Avoiding first and last (Header+Total rows)
			if row_index != 0 and row_index != len(seasons)-1:
				# Iterating through fields in season
				field_index = 0
				# Can use enumerate because playoffs and reg season the same
				for field_index, field in enumerate(season_fields):
					if field_index == 0:
						year = prune_season_field (field)
					elif field_index == 1:
						team = prune_season_field (field)
					elif field_index == 2:
						games_played = prune_season_field (field)						
					elif field_index == 3:
						goals = prune_season_field (field)
					elif field_index == 4:
						assists = prune_season_field (field)
					elif field_index == 5:
						points = prune_season_field (field)
					elif field_index == 6:
						plus_minus = prune_season_field (field)
					elif field_index == 7:
						pim = prune_season_field (field)
					elif field_index == 8:
						powerplay_goals = prune_season_field (field)
					elif field_index == 9:
						shorthanded_goals = prune_season_field (field)
					elif field_index == 10:
						gamewinning_goals = prune_season_field (field)
					elif field_index == 11:
						shots = prune_season_field (field)
					elif field_index == 12:
						shooting_percentage = prune_season_field (field)
				
				seasons_pruned.append (PlayerSeason (
					year, team, games_played, goals, assists, points, 
					plus_minus, pim, powerplay_goals, shorthanded_goals, 
					gamewinning_goals, shots, shooting_percentage))

	return seasons_pruned					

def playerpage_scraper (playerid):
	'''
	Grab supplemental information about player from their page on nhl.com
	Information includes personal details ('tombstone') and season summaries
	Uses funcs tombstone_scraper and career_scraper
	'''
	# Db connection to grab player pos (and update with grabbed data later)
	conn = sqlite3.connect ('nhl.db')
	c = conn.cursor ()
	c.execute("SELECT * FROM all_players WHERE playerid = ?", (playerid,))
	temp_return = c.fetchone()
	pos = temp_return[3]
	
	# Visit player link and grab xml tags
	url = "http://www.nhl.com/ice/player.htm?id=%s"%playerid
	page = requests.get (url)
	tree = html.fromstring (page.text)

	player = tombstone_scraper(tree)
	player.playerid = playerid

	seasons_raw = tree.xpath('//div/div/h3[.="CAREER REGULAR SEASON STATISTICS"]/following-sibling::table[1]//tr')
	playoffs_raw = tree.xpath('//div/div/h3[.="CAREER PLAYOFF STATISTICS"]/following-sibling::table[1]//tr')

	player.regular_seasons = career_scraper (pos, seasons_raw, 0)
	player.playoff_seasons = career_scraper (pos, playoffs_raw, 1)

	# Database time
	conn = sqlite3.connect ('nhl.db')
	c = conn.cursor ()

	if pos == 'G':
		sql_table = "goalies_seasons"
	else:
		sql_table = "players_seasons"
	
	for season in player.regular_seasons:
		print season
	'''	
		c.execute("INSERT INTO %s VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
			%sql_table, tuple(season))
	for playoff in player.playoff_seasons:
		#print playoff
		c.execute("INSERT INTO %s VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"\
			%sql_table, tuple(playoff))
		'''

	# print etree.tostring (seasons_raw[0], pretty_print = True)
	# print player_tombstone
	conn.commit ()
	conn.close()

def create_seasons_playoffs_table():
	# Create database, connection and cursor
	conn = sqlite3.connect ('nhl.db')
	c = conn.cursor ()

	c.execute ('DROP TABLE IF EXISTS players_seasons')
	c.execute ('DROP TABLE IF EXISTS goalies_seasons')
	
	c.execute(
		'CREATE TABLE players_seasons (\
		key INTEGER PRIMARY KEY, season_type INTEGER, playerid INTEGER, season_yr TEXT, team TEXT,\
		gp INTEGER, g INTEGER, a INTEGER, p INTEGER, plus_minus INTEGER,\
		pim INTEGER, ppg INTEGER, shg INTEGER, gwg INTEGER, s INTEGER,\
		s_percent REAL\
		)'
	)

	c.execute(
		'CREATE TABLE goalies_seasons (\
		key INTEGER PRIMARY KEY, season_type INTEGER, playerid INTEGER, season_yr TEXT, team TEXT,\
		gp INTEGER, w INTEGER, l INTEGER, t INTEGER, ot INTEGER,\
		so INTEGER, ga INTEGER, sa INTEGER, sv_percent REAL, gaa REAL,\
		min INTEGER\
		)'
	)

	conn.commit ()
	conn.close()

def database_update():
	conn = sqlite3.connect ('nhl.db')
	c = conn.cursor ()
	c.execute ('select * from all_players')
	players = c.fetchall()

	for player in players:
		playerid = player[0]
		first_name = player[1]
		last_name = player[2]
		update_statement = "UPDATE all_players\
							SET first_name = ?, last_name = ? \
							WHERE playerid = ?"

		print (first_name.upper(), last_name.upper(), playerid,)
					
		c.execute(update_statement, (first_name.upper(), last_name.upper(), playerid,))
		#print update_statement
	

	conn.commit ()
	conn.close()
	
if __name__ == '__main__':
	# all_players_scraper()
	# active_players_scraper()
	
	# create_seasons_playoffs_table()
	# database_update()
	
	'''
	conn = sqlite3.connect ('nhl.db')
	c = conn.cursor ()
	c.execute("SELECT * FROM all_players WHERE playerid = ?", (8473994,))
	temp_return = c.fetchone()
	print temp_return
	conn.commit ()
	conn.close()
	'''

	#playerid, pos = temp_return[0], temp_return[3]
	playerid = 8471716

	playerpage_scraper (playerid)