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