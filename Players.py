import string
import sqlite3
import time
from lxml import html
import requests
from Objects import Event
from dateutil.parser import parse
from random import randint

def all_players_scraper ():
	'''
	grab all player + related info off nhl.com and store in database
	'''
	# Trackinf time it takes function to run
	start_time = time.time()

	# Create database, connection and cursor
	conn = sqlite3.connect ('nhl.db')
	c = conn.cursor ()
	
	c.execute ('DROP TABLE IF EXISTS all_players')
	c.execute(
		'CREATE TABLE all_players (\
		playerid INTEGER primary key, first_name TEXT, last_name TEXT,\
		position TEXT, current_team TEXT, birth_date TEXT,\
		birth_country TEXT, birth_state TEXT, birth_city TEXT\
		)'
	)
	
	
	# variables tracking that db changes: errors/exisiing file, additions
	sql_errors = []
	sql_additions = 0
	
	# string providing letters of first names that we iterate through
	# helps generate urls
	
	# Grabing player ids from all players ever
	# page_num = 302 # page we start grabbing players from
	no_results = False # variable for checking that page has results
	page_num = randint(1,364)
	checked_pages = []
	
	#while no_results == False:
	while len (checked_pages) < 364:
		page_num = randint(1,364)
		while page_num in checked_pages:
			page_num = randint(1,364)
		checked_pages.append (page_num)
		print checked_pages
		url = "http://www.nhl.com/ice/playersearch.htm?position=S&pg=%d"%page_num
		
		delay = randint(1,15)/60.0 # Disguise parsing signature from servers
		time.sleep (delay)
		
		page = requests.get (url)
		tree = html.fromstring (page.text)

		check = tree.xpath ('//div[@style="padding: 6px; font-weight: bold;"]')

		if len(check) == 1:
			no_results = True
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
					current_team = tags[1].xpath('.//a/text()')[0].rstrip()
				except IndexError:
					current_team = None

				# Parsing player birthdate
				try:
					birthdate_raw = tags[2].xpath('.//nobr/text()')[0].rstrip()
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

				# Inserting records into db if they don't already exist
				insert_statement = "INSERT INTO all_players VALUES (%s,\
					\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\",\
					\"%s\", \"%s\")"\
				%(playerid, first_name, last_name, position,\
				  current_team, birth_date, birth_country, birth_state,\
				  birth_city
				  )
				
				try:
					c.execute(insert_statement)
					print "ID %s added to db" %playerid
					sql_additions +=1
				except sqlite3.IntegrityError:
					print "ERROR: ID %s already exists in primary key column"\
						%playerid
					sql_errors.append (playerid)

			print url
		#no_results = True
	conn.commit ()
	conn.close()

	total_time = time.time() - start_time
	print "%0.2fs - total time taken" %total_time
	print str(sql_additions), " - records imported"
	print str(len (sql_errors)), " - records already saved ('errors')"

def active_players_scraper ():
	'''
	Parse through table of active nhl players on nhl.com and update relevant
	player records 
	'''

	# Tracking time it takes function to run
	start_time = time.time()

	# Create database, connection and cursor
	conn = sqlite3.connect ('nhl.db')
	c = conn.cursor ()
	
	# variables tracking that db changes: errors/exisiing file, additions
	sql_errors = []
	records_updated = 0
	
	# string providing letters of first names that we iterate through
	# helps generate urls
	
	# Grabing player ids from all players ever
	# page_num = 302 # page we start grabbing players from
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

			check = tree.xpath ('//div[@style="padding: 6px; font-weight: bold;"]')
			print url

			if len(check) == 1:
				no_results = True
			else:				
				page_num +=1
				players = tree.xpath('//table[@class="data playerSearch"]/tbody/tr')

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
	
if __name__ == '__main__':
	#game_info_scraper ("20142015", "0001")
	'''
	events = playbyplay_scraper ("20142015", "0001")
	for x in range (0,20):
		print events[x]
	'''
	#all_players_scraper()
	active_players_scraper()