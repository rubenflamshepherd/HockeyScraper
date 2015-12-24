import Operations
import Objects # To be largely refactored out. MIGHT BE NECCISARY
import re

class Event:

	def __init__ (self, num, per_num, strength, time,event_type, description, away_on_ice, home_on_ice):
		self.num = num
		self.per_num = per_num
		self.strength = strength
		self.time = time
		self.event_type = event_type
		self.description = description
		self.away_on_ice = away_on_ice
		self.home_on_ice = home_on_ice

	def __str__ (self):

		return self.num.encode('utf-8') + ' ' + self.per_num.encode('utf-8') + ' ' + \
		 self.strength.encode('utf-8') + ' ' + self.time.encode('utf-8') + ' ' + \
		 self.event_type.encode('utf-8') + ' ' + self.description.encode('utf-8')

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

		event = Event(
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
		#print goalie

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

if __name__ == '__main__':

	import Roster
	
	gameinfo_temp = Operations.game_info_extractor	("20152016", "0003")
	gamepersonnel_temp = Roster.harvester ("20152016", "0003")
	events = playbyplay_extractor ("20152016", "0003")
	
	for x in range (0, 300):
		
		print event_object_extractor (x, events, gamepersonnel_temp, gameinfo_temp.away_team, gameinfo_temp.home_team)

	print len(events)
	
