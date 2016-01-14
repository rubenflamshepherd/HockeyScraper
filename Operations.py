from lxml import html
import sqlite3

#list for [url, city, team name, team acronym]
team_list = [['ducks', 'ANAHEIM', 'DUCKS', 'ANA'],
             ['bruins', 'BOSTON', 'BRUINS', 'BOS'],
             ['sabres', 'BUFFALO', 'SABRES', 'BUF'],
             ['flames', 'CALGARY', 'FLAMES', 'CGY'],
             ['hurricanes', 'CAROLINA', 'HURRICANES', 'CAR'],
             ['blackhawks', 'CHICAGO', 'BLACKHAWKS', 'CHI'],
             ['avalanche', 'COLORADO', 'AVALANCHE', 'COL'],
             ['bluejackets', 'COLUMBUS', 'BLUE JACKETS', 'CBJ'],
             ['stars', 'DALLAS', 'STARS', 'DAL'],          
             ['redwings', 'DETROIT', 'RED WINGS', 'DET'],
             ['oilers', 'EDMONTON', 'OILERS', 'EDM'],
             ['panthers', 'FLORIDA', 'PANTHERS', 'FLA'],
             ['kings', 'LOS ANGELES', 'KINGS', 'L.A'],
             ['wild', 'MINNESOTA', 'WILD', 'MIN'],
             ['canadiens', 'MONTREAL', 'CANADIENS', 'MTL'],
             ['canadiens', u'MONTR\xc9AL', 'CANADIENS', 'MTL'], #unicode accent
             ['predators', 'NASHVILLE', 'PREDATORS', 'NSH'],
             ['devils', 'NEW JERSEY', 'DEVILS', 'N.J'],
             ['islanders', 'NEW YORK', 'ISLANDERS', 'NYI'],
             ['rangers', 'NEW YORK', 'RANGERS', 'NYR'],
             ['senators', 'OTTAWA', 'SENATORS', 'OTT'],
             ['flyers', 'PHILADELPHIA', 'FLYERS', 'PHI'],
             ['coyotes', 'ARIZONA', 'COYOTES', 'PHX'],
             ['penguins', 'PITTSBURGH', 'PENGUINS', 'PIT'],
             ['sharks', 'SAN JOSE', 'SHARKS', 'S.J'],
             ['blues', 'ST. LOUIS', 'BLUES', 'STL'],
             ['lightning', 'TAMPA BAY', 'LIGHTNING', 'T.B'],
             ['mapleleafs', 'TORONTO', 'MAPLE LEAFS', 'TOR'],
             ['canucks', 'VANCOUVER', 'CANUCKS', 'VAN'],
             ['capitals', 'WASHINGTON', 'CAPITALS', 'WSH'],
             ['jets', 'WINNIPEG', 'JETS', 'WPG']]

def convert_month_str(month_raw):
	month_dic = {
		'January': 1, \
		'February': 2, \
		'March': 3, \
		'April': 4, \
		'May': 5, \
		'June': 6, \
		'July': 7, \
		'August': 8, \
		'September': 9, \
		'October': 10, \
		'November': 11, \
		'December': 12, \
		}
	return month_dic[month_raw]

def clone_rosterplayer (num, pos, first_name, last_name, roster):
	'''
	Given basic player information, match that to a Roster.Player object in 
	roster and return that object
	'''
	for player in roster:
				
		if player.num == num and \
			player.pos == pos and \
			player.first_name == first_name and \
			player.last_name == last_name:

			return player

def chop_on_ice_branch(tree, roster):
	'''
	Given xml tree contains table of player on ice data, return that as a list
	of the individual Roster.Player objects
	'''

	on_ice_players = []

	players_raw = tree.xpath ('.//font')


	for player in players_raw:
		position_name = player.xpath ('./@title')
		num = player.xpath ('./text()') [0]

		pos_raw, name_raw = position_name[0].split(' - ')
		name_raw = name_raw.split()

		pos = pos_raw[0]
		first_name = name_raw[0]
		last_name = " ".join(name_raw[1:])

		temp_player = clone_rosterplayer(num, pos, first_name, last_name, roster)
		
		on_ice_players.append (temp_player)

	return on_ice_players

def germinate_report_seed (year, game_num, report_type, game_type):
	'''
	Given a report type, return the xml tree created from an locally stored
	html file  
	'''

	root = "C:/Users/Ruben/Projects/HockeyScraper/Reports/"
	
	file_path = root + year + "/" + report_type + game_type + game_num + ".HTM"

	with open (file_path, 'r') as temp_file:
		read_data = temp_file.read()

	return html.fromstring(read_data)

def team_responsible(winning_zone, winning_team, away_team, home_team, event):
	'''
	Given an event (icing, goalie stoppage, etc.) that results in an faceoff
	in an offending teams zone,	discern the team responsible and return 
	them (as 3 letter acronym) and their on ice players
	'''

	if winning_zone == "Def.":

		if winning_team == home_team:
			stopping_team = home_team
			stopping_on_ice = event.home_on_ice

		elif winning_team == away_team:
			stopping_team = away_team
			stopping_on_ice = event.away_on_ice
	else:

		if winning_team == home_team:
			stopping_team = away_team
			stopping_on_ice = event.away_on_ice

		elif winning_team == away_team:
			stopping_team = home_team
			stopping_on_ice = event.home_on_ice

	return stopping_team, stopping_on_ice

def team_name_to_acronym (team_name):
	'''
	given a team name, return the three letter acronym for that team 
	'''

	team_name = team_name.upper()

	for item in team_list:

		if team_name == " ".join(item[1:-1]):

			team_acronym = item[-1]

			return team_acronym
	
	assert False, "ERROR: cannot convert %s to acronym"%(team_name)

def team_acronym_to_titlecase (team_acronym):
	'''
	given a team acronym, return name of that team in titlecase
	'''

	for item in team_list:

		if team_acronym == item[-1]:

			team_titlecase = item[2].title()

			return team_titlecase
	
	assert False, "ERROR: cannot convert %s to titlecase"%(team_acronym)

def team_acronym_to_uppercase (team_acronym):
	'''
	given a team acronym, return name of that team in titlecase
	'''

	for item in team_list:

		if team_acronym == item[-1]:

			team_titlecase = (item[1] + ' ' + item[2]).upper()

			return team_titlecase
	
	assert False, "ERROR: cannot convert %s to titlecase"%(team_acronym)


def index_containing_substring(the_list, substring):
    for i, s in enumerate(the_list):
        if substring in s:
              return i
    return -1

def pad_game_num (game_num):

	game_num = str(game_num)

	if len (game_num) == 4:
		return game_num

	elif len (game_num) == 3:
		return "0" + game_num

	elif len (game_num) == 2:
		return "00" + game_num

	elif len (game_num) == 1:
		return "000" + game_num

	else:
		print "problem with padding game number (Operations.pad_game_num)"

def get_playerid(first_name, last_name, team_acronym, year_raw, position_table):
	'''
	Given a player's first name and last name, return their playerid as found 
	in nhl.db. If more than one player have supplied first_name/last_name
	combo then check seasons and match team/year/playerid
	'''
	# Setting up function
	team_name = team_acronym_to_titlecase(team_acronym)
	if position_table == 'G':
		season_table = 'goalie_seasons'
	else:
		season_table = 'player_seasons'
	year = "-".join([year_raw[:4],year_raw[4:]])

	# Grabbing ALL players with first_name/last_name combo	
	conn = sqlite3.connect ('nhl.db')
	c = conn.cursor ()
	c.execute("SELECT * FROM all_players WHERE upper(first_name) = ? \
			   AND upper(last_name) = ?", (first_name, last_name,))
	
	matching_players = c.fetchall()
	'''
	Sometimes first names are different from table to game sheet
	When this happens NO player is returned and we must do a wider search 
	for the player
	'''
	if len(matching_players) == 0:
		c.execute("SELECT * FROM all_players WHERE upper(last_name) = ?",
			(last_name,))
		matching_players = c.fetchall()

	# From the players we have grabbed 
	if len(matching_players) == 1:
		playerid = matching_players[0][0]
		return playerid
	# If more than 1 player is grabbed, cross reference seasons to match
	else:
		for player in matching_players:
			playerid = player[0]
			c.execute("SELECT * FROM {} WHERE playerid = ? AND year = ? \
				AND team = ?".format(season_table), (playerid, year, team_name))

			matching_season = c.fetchall()
			if len(matching_season) > 0:
				conn.close()
				return playerid

	# Error checking
	print matching_players
	assert False, "ERROR: > 1 matching first/last name w/o matching nhl season"
