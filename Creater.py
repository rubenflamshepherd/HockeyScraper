'''
Create databases, save things into databases
'''

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
def ripen_playerpage(player):
	'''
	Give a Grabber.Player object, put their information into nhl.db
	'''
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
