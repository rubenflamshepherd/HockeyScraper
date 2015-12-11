'''
Grab information from nhl.com that does not need to be stored in a local file
Use Creater.py to throw information in sql databases for storage
'''

import string
import sqlite3
import time
from lxml import html, etree
import requests
from Objects import Event, Player
from dateutil.parser import parse
from random import randint

def all_players_scraper ():
	'''
	Grab basic information from EVERY player to player in the NHL from
	nhl.com and store in database 
	player + related info off nhl.com and store in database
	'''
	# Trackinf time it takes function to run
	start_time = time.time()

	# Create database, connection and cursor
	conn = sqlite3.connect ('nhl.db')
	c = conn.cursor ()
	'''
	c.execute ('DROP TABLE IF EXISTS all_players')
	c.execute(
		'CREATE TABLE all_players (\
		playerid INTEGER primary key, first_name TEXT,\
		last_name TEXT, position TEXT, current_team TEXT,\
		birth_date TEXT, birth_country TEXT, birth_state TEXT,\
		birth_city TEXT\
		)'
	)
	'''
		
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

def playerpage_scraper (playerid, pos):
	'''
	Grab supplemental information about player from their page on nhl.com
	Information includes personal details ('tombstone') and season summaries
	Uses funcs tombstone_scraper and career_scraper
	'''

	# Visit player link and grab xml tags
	url = "http://www.nhl.com/ice/player.htm?id=%s"%playerid
	page = requests.get (url)
	tree = html.fromstring (page.text)

	player_tombstone = tombstone_scraper (tree)

	seasons_raw = tree.xpath('//div/div/h3[.="CAREER REGULAR SEASON STATISTICS"]/following-sibling::table[1]//tr')
	playoffs_raw = tree.xpath('//div/div/h3[.="CAREER PLAYOFF STATISTICS"]/following-sibling::table[1]//tr')

	seasons = career_scraper (playerid, pos, seasons_raw, 0)
	playoffs = career_scraper (playerid, pos, playoffs_raw, 1)

	# Database time
	conn = sqlite3.connect ('nhl.db')
	c = conn.cursor ()

	if pos == 'G':
		sql_table = "goalies_seasons"
	else:
		sql_table = "players_seasons"

	for season in seasons:
		#print season
		c.execute("INSERT INTO %s VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"%sql_table, tuple(season))
	for playoff in playoffs:
		#print playoff
		c.execute("INSERT INTO %s VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"%sql_table, tuple(playoff))

	# print etree.tostring (seasons_raw[0], pretty_print = True)
	# print player_tombstone
	conn.commit ()
	conn.close()
	

def tombstone_scraper (tree):
	'''
	'''

	# Container for player information
	temp_player = Player ()
	
	info_raw = tree.xpath('//div[@id="tombstone"]/div/table//tr/td/text()')
	website_raw = tree.xpath('//div[@id="tombstone"]//div[@id="playerSite"]/a/@href')
	position_raw = tree.xpath('//div[@id="tombstone"]/div/div/span/text()')
	twitter_raw = tree.xpath('//div[@id="tombstone"]/div/table/tr/td/a/@href')
	team_pos_raw = tree.xpath('//div[@id="tombstone"]/div/div[@style="float: left; margin-left: 6px; font-weight: bold; color: #999;"]')

	team_raw = team_pos_raw[0].xpath ('./a/text()')
	pos_raw = team_pos_raw[0].xpath ('./span/text()')
	
	info_stripped = [x.strip() for x in info_raw]

	for x in range(len (info_stripped)):
		if info_stripped[x].strip() == "NUMBER:":
			temp_player.num = info_stripped[x+1]
		elif info_stripped[x].strip() == "HEIGHT:":
			height_raw = info_stripped[x+1].split ("\' ")
			temp_player.height = height_raw[0] + ',' + height_raw[1].strip('"')
		elif info_stripped[x].strip() == "WEIGHT:":
			temp_player.weight = info_stripped[x+1]
		elif info_stripped[x].strip() == "DRAFTED:":
			temp_player.draft_team = info_stripped[x+1].strip('/').strip().strip()
		elif info_stripped[x].strip() == "Shoots:":
			temp_player.hand = info_stripped[x+1] [0]
		elif info_stripped[x].strip() == "Catches:":
			temp_player.hand = info_stripped[x+1] [0]
		elif info_stripped[x].strip() == "ROUND:":
			temp_player.draft_rnd = info_stripped[x+1]
			temp_player.draft_overall = info_stripped[x+2].strip('()')

	try:
		temp_player.website = website_raw [0]
	except IndexError:
		pass

	try:
		temp_player.pos = position_raw [0][0]
	except IndexError:
		pass

	try:
		temp_player.current_team = team_raw [0]
	except IndexError:
		pass

	try:
		temp_player.pos = pos_raw [0]
	except IndexError:
		pass

	for item in twitter_raw:
		if item.find ("/ice/draftsearch.htm?team=") != -1:
			temp_player.draft_yr = item.split ('=') [-1]
		elif item.find ("https://twitter.com/") != -1:
			temp_player.twitter = item.split('/') [-1]

	return temp_player


def career_scraper(playerid, pos, rows, season_type):
	'''
	Takes rows from statistical table from player page on
	nhl.com and return consolidated table. Tables summarize either regular 
	season or playoff statistics
	'''
	info = []

	for row_index, row in enumerate(rows):
		info_raw = row.xpath('./td')

		# Grabbbing row information
		if row_index != 0 and row_index != len(rows)-1:
			temp = [None, season_type, playerid]
			for item_index, item in enumerate(info_raw):
				if len(item.xpath('./span')) == 1:
					temp_item = item.xpath('./span/text()')[0].strip()
					temp.append(temp_item)
				elif len(item.xpath('./a')) == 1:
					temp.append(item.xpath('./a/text()')[0])
				
				else:
					try:
						temp_item = item.xpath('./text()')[0].strip()
						if temp_item == '':
							temp.append (None)
						else:
							temp.append (temp_item)

					except IndexError:
						temp.append (None)
					# Playoffs don't have T/OT columns
					if len (temp) == 7 and season_type == 1 and pos == 'G':
						temp.append (None)
						temp.append (None)
			
			# Formatting
			assert len(temp) is 16, "player id %s len(season) %s not 16, is %s, \n %s" %(playerid, temp[0], len(temp), temp)
			if pos != 'G':
				for stat_index, stat in enumerate(temp):
					if stat != None:
						if stat_index == len (temp)-1:
							temp[stat_index] = float(temp[stat_index])
						elif stat_index > 4 and stat_index < len (temp)-1:
							temp[stat_index] = int(temp[stat_index])
			else:
				for stat_index, stat in enumerate(temp):
					if stat != None:
						if stat_index == 13 or stat_index == 14 : # SV% col
							temp[stat_index] = float(temp[stat_index])
						elif stat_index == 8: # Tie col
							if stat =='-':
								temp[stat_index] = None
							else:
								temp[stat_index] = int(temp[stat_index])
						elif stat_index == len (temp)-1 or stat_index == 12: # Min col
							temp[stat_index] = int(temp[stat_index].replace(',',''))
						elif stat_index > 4:
							temp[stat_index] = int(temp[stat_index])
			info.append(temp)
			#print temp
	return info

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
	database_update()
	'''

	conn = sqlite3.connect ('nhl.db')
	c = conn.cursor ()
	c.execute("SELECT * FROM all_players WHERE playerid = ?", (8473994,))
	temp_return = c.fetchone()
	print temp_return
	conn.commit ()
	conn.close()

	playerid, pos = temp_return[0], temp_return[3]

	playerpage_scraper (playerid, pos)
	'''
	
