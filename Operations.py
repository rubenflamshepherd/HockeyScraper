from lxml import html
import Objects
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
             ['predators', 'NASHVILLE', 'PREDATORS', 'NSH'],
             ['devils', 'NEW JERSEY', 'DEVILS', 'N.J'],
             ['islanders', 'NEW YORK', 'ISLANDERS', 'NYI'],
             ['rangers', 'NEW YORK', 'RANGERS', 'NYR'],
             ['senators', 'OTTAWA', 'SENATORS', 'OTT'],
             ['flyers', 'PHILADELPHIA', 'FLYERS', 'PHI'],
             ['coyotes', 'PHOENIX', 'COYOTES', 'PHX'],
             ['penguins', 'PITTSBURGH', 'PENGUINS', 'PIT'],
             ['sharks', 'SAN JOSE', 'SHARKS', 'S.J'],
             ['blues', 'ST. LOUIS', 'BLUES', 'STL'],
             ['lightning', 'TAMPA BAY', 'LIGHTNING', 'T.B'],
             ['mapleleafs', 'TORONTO', 'MAPLE LEAFS', 'TOR'],
             ['canucks', 'VANCOUVER', 'CANUCKS', 'VAN'],
             ['capitals', 'WASHINGTON', 'CAPITALS', 'WSH'],
             ['jets', 'WINNIPEG', 'JETS', 'WPG']]

def chop_on_ice_branch(tree):
	'''
	Given xml tree contains table of player on ice data, return that as a list
	of the individual players
	'''

	away_on_ice = []

	away_players_raw = tree.xpath ('.//font')


	for away_player in away_players_raw:
		position_name = away_player.xpath ('./@title')
		number = away_player.xpath ('./text()') [0]

		position, name = position_name[0].split(' - ')

		away_on_ice.append ([position, name, number])

	return away_on_ice

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

	for item in team_list:

		if team_name == " ".join(item[1:-1]):

			team_acronym = item[-1]

			return team_acronym

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

	away_team = team_name_to_acronym (away_team_raw)
	home_team = team_name_to_acronym (home_team_raw)

	return Objects.GameInfo (
		game_date, attendance_arena, game_start_end, game_num,\
		away_score, away_team, away_team_game_nums,\
		home_score, home_team, home_team_game_nums
		)

def get_playerid(first_name, last_name):
	'''
	Given a player's first name and last name, return their playerid as found 
	in nhl.db
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