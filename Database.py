'''
Create databases, save things into databases
'''
from dateutil.parser import parse
from lxml import html, etree
import PlayerPage
import random
import requests
import sqlite3
import time


class DB_Player(object):

	def __init__(self, playerid, first_name, last_name, position_table, 
		current_team, birth_date, birth_country, birth_state, birth_city):
		
		self.playerid = playerid
		self.first_name = first_name
		self.last_name = last_name
		self.position_table = position_table
		self.current_team = current_team
		self.birth_date = birth_date
		self.birth_country = birth_country
		self.birth_state = birth_state
		self.birth_city = birth_city

def update():
	'''
	General function for updating database
	'''

	conn = sqlite3.connect ('nhl.db')
	c = conn.cursor ()
	c.execute ('select * from all_players')
	players = c.fetchall()

	for player in players:
		pass

	conn.commit ()
	conn.close()

def germinate_seasons_table():
	'''
	Create tables for storing player seasons as parsed from their player pages
	'''

	# Create database, connection and cursor
	conn = sqlite3.connect ('nhl.db')
	c = conn.cursor ()

	c.execute ('DROP TABLE IF EXISTS {}'.format('goalie_seasons'))
	c.execute('CREATE TABLE {} (\
		key INTEGER PRIMARY KEY, playerid INTEGER, nhl_season INTEGER, \
		season_type INTEGER, year TEXT, team TEXT, games_played INTEGER, \
		wins INTEGER, loses INTEGER, ties INTEGER, overtime_loses INTEGER, \
		shutouts INTEGER, goals_against INTEGER, shots_against INTEGER, \
		save_percentage REAL, goals_against_average REAL, \
		minutes_played INTEGER)'.format('goalie_seasons'))

	c.execute ('DROP TABLE IF EXISTS {}'.format('player_seasons'))
	c.execute('CREATE TABLE {} (\
		key INTEGER PRIMARY KEY, playerid INTEGER, nhl_season INTEGER, \
		season_type INTEGER, year TEXT, team TEXT, games_played INTEGER, \
		goals INTEGER, assists INTEGER, points INTEGER, plus_minus INTEGER, \
		pim INTEGER, powerplay_goals INTEGER, shorthanded_goals INTEGER, \
		gamewinning_goals INTEGER, shots INTEGER, shooting_percentage REAL\
		)'.format('player_seasons'))
	
	conn.commit ()
	conn.close()

def germinate_all_players_table():
	'''
	Create tables for storing general player data as parsed from their player
	page
	'''

	# Create database, connection and cursor
	conn = sqlite3.connect ('nhl.db')
	c = conn.cursor ()

	c.execute ('DROP TABLE IF EXISTS all_players')
		
	c.execute(
		'CREATE TABLE all_players (\
		playerid INTEGER primary key, first_name TEXT, last_name TEXT,\
		position_table TEXT, position_page TEXT, current_team TEXT, \
		birth_date TEXT, birth_country TEXT, birth_state TEXT,\
		birth_city TEXT, last_nhl_season TEXT, current_num INTEGER,\
		weight TEXT, shoots TEXT, draft_year INTEGER, draft_team TEXT,\
		draft_round INTEGER, draft_overall INTEGER, \
		twitter TEXT, website TEXT\
		)'
	)

	conn.commit ()
	conn.close()

def prune_all_players_table_page(tree):
	'''
	Given a xml tree of a page of players from all the table containing all
	nhl players, put information from each row into a local DB_Player object 
	and return a list of the players
	Used in func grow_all_players
	'''

	players_raw = tree.xpath('//table[@class="data playerSearch"]/tbody/tr')
	players = []

	for player in players_raw:
		tags = player.xpath ('.//td')

		#Parsing first, last name and position
		name_position_raw = tags[0].xpath('.//a/text()')[0]\
			.rstrip()
		position_table = name_position_raw.split()[-1].strip('()')

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
			current_team = tags[1].xpath('.//a/text()')[0].rstrip()
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
		players.append(DB_Player(playerid, first_name, last_name, 
			position_table, current_team, birth_date, birth_country, 
			birth_state, birth_city))

	return players

def grow_all_players():
	'''
	Grab basic information from EVERY player to player in the NHL from
	nhl.com (all players table) and store in database 
	'''
	# Tracking time it takes function to run
	start_time = time.time()

	# Create database, connection and cursor
	conn = sqlite3.connect ('nhl.db')
	c = conn.cursor ()
			
	# variables tracking db changes: errors/exisiing file, additions
	sql_errors = []
	sql_additions = 0
	
	# Grabing player ids from all players ever
	checked_pages = []
	
	while len (checked_pages) < 380: # (380 pages as of 05/01/15)
		page_num = random.randint(1,380)
		while page_num in checked_pages:
			if page_num == 380:
				page_num = random.randint(1,380)
			else:
				page_num += 1
		checked_pages.append (page_num)
		print str(len(checked_pages)) + "/" + '380'
		url = "http://www.nhl.com/ice/playersearch.htm?position=S&pg=%d"\
			%page_num
		print url		

		delay = random.randint(1,15)/60.0 # Disguise parsing from servers
		time.sleep (delay)
		
		page = requests.get (url)
		tree = html.fromstring (page.text)
		# Check to see if page falls inside rage of those containing
		# part of player info table (364 pages as of 05/01/15)
		check = tree.xpath (
		'//div[@style="padding: 6px; font-weight: bold;"]'
		)
		if len(check) == 1:
			pass
		else:
			temp_page = prune_all_players_table_page(tree)

			# Insert records into db if they don't already exist
			for player in temp_page:
				
				try:
					c.execute(
						"INSERT INTO all_players VALUES \
						(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", \
						(player.playerid, player.first_name, \
						player.last_name, player.position_table, None, \
						player.current_team, player.birth_date, \
						player.birth_country, player.birth_state, \
						player.birth_city, None, None, None, None, None, None, \
						None, None, None, None,)
						)
						
					# print "ID %s added to db" %player.playerid
					sql_additions +=1
				except sqlite3.IntegrityError:
					print "ERROR: ID %s already exists\
						in primary key column"%player.playerid
					sql_errors.append (player.playerid)
		
	conn.commit ()
	conn.close()

	total_time = time.time() - start_time
	print "%0.2fs - total time taken" %total_time
	print str(sql_additions), " - records imported"
	print str(len (sql_errors)), " - records already saved ('errors')"

def ripen_tombstone(c, player):
	'''
	Put player tombstone information in PlayerPage object 'player' into db
	using database connection c
	Used in func ripen_player
	'''
	
	c.execute("UPDATE all_players SET position_page = ?, last_nhl_season = ?,\
		current_num = ?, weight = ?, shoots = ?, draft_year = ?,\
		draft_team = ?, draft_round = ?, draft_overall = ?, twitter = ?,\
		website = ?\
		WHERE playerid = ? ", (player.position_page, player.last_nhl_season,
			player.current_num, player.weight, player.shoots,
			player.draft_year, player.draft_team, player.draft_round, 
			player.draft_overall, player.twitter, player.website, 
			player.playerid)
			)

def ripen_season(c, table_name, season):
	'''
	Put player season information in PlayerPage object 'player' into db
	using database connection c
	Used in func ripen_player
	'''
	if table_name == 'goalie_seasons':
		c.execute("INSERT INTO {} VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"\
			.format(table_name), (\
				None, season.playerid, season.nhl_season, season.season_type, 
				season.year, season.team, season.games_played, season.wins, 
				season.loses, season.ties, season.overtime_loses, 
				season.shutouts, season.goals_against, season.shots_against, 
				season.save_percentage, season.goals_against_average, 
				season.minutes_played,)
				)
	elif table_name == 'player_seasons':
		c.execute("INSERT INTO {} VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"\
			.format(table_name), (\
				None, season.playerid, season.nhl_season, season.season_type,
				season.year, season.team, season.games_played, season.goals, 
				season.assists,	season.points, season.plus_minus, season.pim, 
				season.powerplay_goals, season.shorthanded_goals, 
				season.gamewinning_goals, season.shots, 
				season.shooting_percentage,)
				)
	else:
		assert True, "ERROR: WTF are you passing as table_name in ripen_season"

def ripen_player(c, player):
	'''
	Put PlayerPage object 'player' information into nhl.db using database 
	connetion 'c'
	Used in func ripen_all_players
	'''
	
	delay = random.randint(1,15)/60.0 # Disguise parsing from servers
	time.sleep (delay)

	ripen_tombstone (c, player)
	
	if player.position_page == 'Goalie':
		for season in player.regular_seasons:
			ripen_season(c, 'goalie_seasons', season)
		for season in player.playoff_seasons:
			ripen_season(c, 'goalie_seasons', season)
	else:
		for season in player.regular_seasons:
			ripen_season(c, 'player_seasons', season)
		for season in player.playoff_seasons:
			ripen_season(c, 'player_seasons', season)

def ripen_all_players():
	'''
	Populate db table 'all_players' in nhl.db with tombstone details by going
	to individual player pages using already stored playerids
	Table MUST have been seeded using grow_all_players previously
	Top level function
	'''

	# Tracking time it takes function to run/num of players grabbed
	start_time = time.time()
	num_players = 0
	player_counter = 0

	conn = sqlite3.connect ('nhl.db')
	c = conn.cursor ()

	c.execute('SELECT * FROM all_players')

	rows = c.fetchall()

	# Grabing player ids from all players ever
	checked_players = []
	num_rows = len(rows)
	max_index = len (rows) - 1

	 # (380 pages/18196 rows as of 05/01/15)	
	while len (checked_players) < num_rows:
		index_num = random.randint(0, max_index)
		while index_num in checked_players:
			if index_num == max_index:
				index_num = random.randint(0, max_index)
			else:
				index_num += 1
		checked_players.append (index_num)
		print (str(len(checked_players)) + "/" + str(num_rows)).ljust(15),
		
		player_counter += 1				
		playerid = rows[index_num][0]
		position_table = rows[index_num][3]
		print ('RIPENED ' + str(playerid)).ljust(30)
		assert position_table in ['G', 'D', 'LW', 'C', 'RW'],\
			'ERROR: position_table invalid (=%s)'%(position_table)
		player = PlayerPage.harvest(playerid, position_table)
		ripen_player(c, player)
		num_players += 1
		conn.commit ()
	
	conn.close()

	total_time = time.time() - start_time
	print "%0.2fs - total time taken" %total_time
	print str(num_players), " - records imported"
	print str(total_time/num_players) + 'secs/player'


if __name__ == '__main__':
	germinate_all_players_table()
	germinate_seasons_table()
	grow_all_players()

	player = PlayerPage.harvest(8449783, 'G')
	
	conn = sqlite3.connect ('nhl.db')
	c = conn.cursor ()
	c.execute('SELECT * FROM all_players WHERE playerid = ?',(8449783,))

	row = c.fetchone()
	playerid = row[0]
	position = row[3]
	player = PlayerPage.harvest(playerid, position)
	ripen_player (c, player)	
