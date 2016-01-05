import GameHeader
import Operations
import re
import Roster

class Event(object):

	def __init__(self, num, period_num, strength, time, event_type, zone,
				 description, away_on_ice, home_on_ice):

		self.num = num
		self.period_num = period_num
		self.strength = strength
		self.time = time
		self.event_type = event_type
		self.zone = zone
		self.description = description
		self.away_on_ice = away_on_ice
		self.home_on_ice = home_on_ice

	def create_prefix(self):

		event_num = ("\nE" + self.num.encode('utf-8')).ljust(5)
		period_num = (" P" + self.period_num.encode('utf-8')).ljust(3)
		strength = (" " + self.strength.encode('utf-8')).ljust(4)
		time = ("@" + self.time.encode('utf-8')).ljust(7)
		event_type = (self.event_type.encode('utf-8')).ljust(6)
		zone = (str(self.zone).encode('utf-8')).ljust(5)

		return event_num + period_num + strength + time + event_type + zone

	def __str__(self):

		event_num = ("\nE#" + self.num.encode('utf-8')).ljust(6)
		period_num = (" P#" + self.period_num.encode('utf-8')).ljust(4)
		strength = (" " + self.strength.encode('utf-8')).ljust(4)
		time = ("@" + self.time.encode('utf-8')).ljust(7)
		event_type = (self.event_type.encode('utf-8')).ljust(5)
		description = (self.description.encode('utf-8')).ljust(35) 

		return event_num + per_num + strength + time + event_type + description

class Block(Event):

	def __init__(self, num, per_num, strength, time, event_type, zone, 
				 description, away_on_ice, home_on_ice, shot_type,
				 shooting_player, blocking_player, shooting_team, 
				 blocking_team):
	
		Event.__init__(self, num, per_num, strength, time, event_type, zone, 
					   description, away_on_ice, home_on_ice)	
		self.shot_type = shot_type
		self.shooting_player = shooting_player
		self.blocking_player = blocking_player
		self.shooting_team = shooting_team
		self.blocking_team = blocking_team
	
	def __str__(self):

		shot_type = (self.shot_type.encode('utf-8')).ljust(8)		
		shooting_player = ('SP ' + self.shooting_player.show).ljust(20)		
		blocking_player = ('BP ' + self.blocking_player.show).ljust(20)

		return self.create_prefix() + shot_type + shooting_player \
			   + blocking_player

class FaceOff(Event):

	def __init__(self, num, per_num, strength, time, event_type, zone, \
		description, away_on_ice, home_on_ice, winning_player, 
		losing_player, winning_team, losing_team):
		
		Event.__init__(self, num, per_num, strength, time, event_type, zone, \
			description, away_on_ice, home_on_ice)
		
		self.winning_player = winning_player
		self.losing_player = losing_player
		self.winning_team = winning_team
		self.losing_team = losing_team
	
	def __str__(self):

		winning_player = ('WP ' + self.winning_player.show).ljust(20)		
		losing_player = ('LP ' + self.losing_player.show).ljust(20)

		return self.create_prefix() + winning_player + losing_player

class Give(Event):

	def __init__(self, num, per_num, strength, time, event_type, zone, 
		description, away_on_ice, home_on_ice, giving_player, giving_team):
		
		Event.__init__(self, num, per_num, strength, time, event_type, zone, \
			description, away_on_ice, home_on_ice)

		self.giving_player = giving_player
		self.giving_team = giving_team
	
	def __str__ (self):

		giving_player = ('By ' + self.giving_team + ' ' \
			+  self.giving_player.show).ljust(25)		
		
		return self.create_prefix() + giving_player

class Goal(Event):

	def __init__(self, num, per_num, strength, time, event_type, zone, 
		description, away_on_ice, home_on_ice, shot_type, distance, 
		scoring_player, scoring_team, prim_assist_player, sec_assist_player,
		goalie, defending_team):
		
		Event.__init__(self, num, per_num, strength, time, event_type, zone, \
			description, away_on_ice, home_on_ice)
		
		self.shot_type = shot_type
		self.distance = distance
		self.scoring_player = scoring_player
		self.scoring_team = scoring_team
		self.prim_assist_player = prim_assist_player
		self.sec_assist_player = sec_assist_player
		self.goalie = goalie
		self.defending_team = defending_team

	def __str__ (self):

		shot_type = (self.shot_type.encode('utf-8')).ljust(8)		
		distance = (self.distance.encode('utf-8') + 'ft').ljust(5)
		scoring_player = ('SP ' + self.scoring_player.show).ljust(15)		
		prim_assist_player = ('PA ' + self.prim_assist_player.show).ljust(15)		
		sec_assist_player = ('SA ' + self.sec_assist_player.show).ljust(15)		
		goalie = ('G ' + self.goalie.show).ljust(15)		


		return self.create_prefix() + shot_type + distance \
			+ scoring_player + prim_assist_player + sec_assist_player \
			+ goalie

class Hit(Event):

	def __init__(self, num, per_num, strength, time, event_type, zone,
		description, away_on_ice, home_on_ice, hitting_player, hit_player,
		hitting_team, hit_team):
		
		Event.__init__(self, num, per_num, strength, time, event_type, zone, \
			description, away_on_ice, home_on_ice)
		
		self.hitting_player = hitting_player
		self.hit_player = hit_player
		self.hitting_team = hitting_team
		self.hit_team = hit_team
	
	def __str__ (self):

		hitting_player = ('Hitting ' + self.hitting_player.show).ljust(22)		
		hit_player = ('Hit ' + self.hit_player.show).ljust(22)

		return self.create_prefix() + hitting_player + hit_player

class Miss(Event):

	def __init__(self, num, per_num, strength, time, event_type, zone, \
		description, away_on_ice, home_on_ice, shot_type, miss_type, distance, \
		shooting_player, blocking_player, shooting_team, blocking_team):
		
		Event.__init__(self, num, per_num, strength, time, event_type, zone, \
			description, away_on_ice, home_on_ice)
		
		self.shot_type = shot_type
		self.miss_type = miss_type
		self.distance = distance
		self.shooting_player = shooting_player
		self.blocking_player = blocking_player
		self.shooting_team = shooting_team
		self.blocking_team = blocking_team

	def __str__(self):

		shot_type = (self.shot_type.encode('utf-8')).ljust(8)		
		miss_type = (self.miss_type.encode('utf-8')).ljust(7)		
		distance = (self.distance.encode('utf-8')).ljust(4)
		shooting_player = ('SP ' + self.shooting_player.show).ljust(15)		
		blocking_player = ('BP ' + self.blocking_player.show).ljust(15)

		return self.create_prefix() + shot_type + distance + miss_type \
			+ shooting_player + blocking_player

class Penalty(Event):

	def __init__(self, num, per_num, strength, time, event_type, zone, \
	 	description, away_on_ice, home_on_ice, penalty_type, length, \
	 	penalized_player, drawing_player, penalized_team, drawing_team):
		
		Event.__init__(self, num, per_num, strength, time, event_type, zone, \
			description, away_on_ice, home_on_ice)
		
		self.penalty_type = penalty_type
		self.length = length
		self.penalized_player = penalized_player
		self.drawing_player = drawing_player
		self.penalized_team = penalized_team
		self.drawing_team = drawing_team

	def __str__(self):

		penalty_type = (self.penalty_type.encode('utf-8')).ljust(10)		
		length = (self.length.encode('utf-8')).ljust(4)
		penalized_player = ('To ' + self.penalized_team + ' ' \
			+ self.penalized_player.show).ljust(15)		
		drawing_player = ('D By ' + self.drawing_team + ' ' \
			+ self.drawing_player.show).ljust(15)		
		
		return self.create_prefix() + penalty_type + length \
			+ penalized_player + drawing_player

class PeriodStart(Event):

	def __init__ (self, num, per_num, strength, time, event_type, zone, \
		description, away_on_ice, home_on_ice, start_time, time_zone):
		
		Event.__init__(self, num, per_num, strength, time, event_type, zone, \
			description, away_on_ice, home_on_ice)
		
		self.start_time = start_time
		self.time_zone = time_zone
	

	def __str__ (self):

		description = (self.start_time.__str__() + ' ' + self.time_zone).ljust(35) 

		return self.create_prefix() + description

class PeriodEnd(Event):

	def __init__(self, num, per_num, strength, time, event_type, zone, \
		description, away_on_ice, home_on_ice, start_time, time_zone):
		
		Event.__init__(self, num, per_num, strength, time, event_type, zone, \
			description, away_on_ice, home_on_ice)
		
		self.end_time = start_time
		self.time_zone = time_zone
	

	def __str__(self):

		description = (self.end_time.__str__() + ' ' + self.time_zone).ljust(35) 

		return self.create_prefix() + description

class GameEnd(Event):

	def __init__ (self, num, per_num, strength, time, event_type, zone, \
		description, away_on_ice, home_on_ice, start_time, time_zone):
		
		Event.__init__(self, num, per_num, strength, time, event_type, zone, \
			description, away_on_ice, home_on_ice)
		
		self.end_time = start_time
		self.time_zone = time_zone
	

	def __str__(self):

		description = (self.end_time.__str__() + ' ' + self.time_zone).ljust(35) 

		return self.create_prefix() + description
	
class Shot(Event):

	def __init__(self, num, per_num, strength, time, event_type, zone, \
		description, away_on_ice, home_on_ice, shot_type, distance, \
		shooting_player, blocking_player, shooting_team, blocking_team):
		
		Event.__init__(self, num, per_num, strength, time, event_type, zone, \
			description, away_on_ice, home_on_ice)
		
		self.shot_type = shot_type
		self.distance = distance
		self.shooting_player = shooting_player
		self.blocking_player = blocking_player
		self.shooting_team = shooting_team
		self.blocking_team = blocking_team
	
	def __str__(self):

		shot_type = (self.shot_type.encode('utf-8')).ljust(8)		
		distance = (self.distance.encode('utf-8')).ljust(4)
		shooting_player = ('SP ' + self.shooting_player.show).ljust(15)		
		blocking_player = ('BP ' + self.blocking_player.show).ljust(15)

		return self.create_prefix() + shot_type + distance \
			+ shooting_player + blocking_player

class Stop(Event):

	def __init__(self, num, per_num, strength, time, event_type, zone, \
		description, away_on_ice, home_on_ice, description_parsed, \
		stopping_player, stopping_team, tv_timeout, timeout_caller):

		Event.__init__(self, num, per_num, strength, time, event_type, zone, \
			description, away_on_ice, home_on_ice)

		self.description_parsed = description_parsed
		self.stopping_player = stopping_player
		self.stopping_team = stopping_team
		self.tv_timeout = tv_timeout
		self.timeout_caller = timeout_caller
	
	def __str__(self):

		description_parsed = self.description_parsed.ljust(20)
		stopping_player = ('By ' + str(self.stopping_team) + ' '\
			+ str(self.stopping_player.show)).ljust(19)
		tv_timeout = ('TVTO ' + str(self.tv_timeout)).ljust(8)
		to_caller = ('TOBy ' + str(self.timeout_caller)).ljust(15)

		return self.create_prefix() + description_parsed + stopping_player \
			+ tv_timeout + to_caller

class Take(Event):

	def __init__ (self, num, per_num, strength, time, event_type, zone, 
		description, away_on_ice, home_on_ice, taking_player, taking_team):

		Event.__init__(self, num, per_num, strength, time, event_type, zone, \
			description, away_on_ice, home_on_ice)

		self.taking_player = taking_player
		self.taking_team = taking_team
	
	def __str__(self):
		
		taking_player = ('By ' + self.taking_team + ' ' + \
			self.taking_player.show).ljust(25)		
		
		return self.create_prefix() + taking_player

class PlayByPlay (object):

	def __init__(self, raw_events):

		self.raw_events = raw_events

		self.blocks = []
		self.faceoffs = []
		self.hits = []
		self.goals = []
		self.misses = []
		self.penalties = []
		self.period_starts = []
		self.stops = []
		self.shots = []
		self.take_aways = []
		self.give_aways = []

def clone_rosterplayer (num, last_name, roster):
	'''
	Given basic player information, match that to a Roster.Player object in 
	roster and return that object
	'''
	for player in roster:
				
		if player.num == num and player.last_name == last_name:

			return player

	assert True, "ERROR: no matching player"

def raw_harvest (year, game_num, away_roster, home_roster):
	"""
	Extract play-by-play information from a html file on the
	local machine (in the form of raw, unspeficied events).
	Returns list of unspecified event objects
	"""

	tree = Operations.germinate_report_seed(year,game_num,'PL','02')

	events = [] # empty list for holding unspecified events
	
	for item in tree.xpath('//table/tr[@class="evenColor"]'):
				
		event_raw = item.xpath('./td/text()')

		num = unicode(event_raw[0])
		per_num = unicode(event_raw[1])
		strength = unicode(event_raw[2])
		time = unicode(event_raw[3])
		event_type = unicode(event_raw[5])
		zone = None # Zone is not initially parsed in raw harvest
		description = unicode(event_raw[6])

		# Goals have an additional row in the description cell for assists
		if event_type == 'GOAL' and event_raw[7].find('Assist') != -1:
			description = unicode(" ".join(event_raw[6:8]))

		players_on_ice = item.xpath('./td/table')

		home_on_ice = []
		away_on_ice = []
			
		if len (players_on_ice) == 2:

			away_on_ice = Operations.chop_on_ice_branch (
				players_on_ice[0], away_roster
				)
			home_on_ice = Operations.chop_on_ice_branch (
				players_on_ice[1], home_roster
				)

		event = Event(num, per_num, strength, time, event_type, zone, \
			description, away_on_ice, home_on_ice)
		
		events.append (event)	    
	return events

def event_prune(event_index, event_list, game_personnel, away_team, home_team):
	'''
	Given a string that is the description of an event, return an object of
	that event containing all possible data
	'''
	event = event_list[event_index]

	description_raw = event.description.split ()

	if event.event_type == 'PSTR':
		
		start_time = description_raw[-2]
		time_zone = description_raw[-1]
		zone = 'Neu.'

		return PeriodStart(
			event.num,
			event.period_num,
			event.strength,
			event.time,
			event.event_type,
			zone,
			event.description,
			event.away_on_ice,
			event.home_on_ice,
			start_time,
			time_zone
			)

	elif event.event_type == 'PEND':
		
		end_time = description_raw[-2]
		time_zone = description_raw[-1]
		zone = 'Neu.'

		return PeriodEnd(
			event.num,
			event.period_num,
			event.strength,
			event.time,
			event.event_type,
			zone,
			event.description,
			event.away_on_ice,
			event.home_on_ice,
			end_time,
			time_zone
			)
	
	elif event.event_type == 'GEND':
		
		end_time = description_raw[-2]
		time_zone = description_raw[-1]
		zone = 'Neu.'

		return GameEnd(
			event.num,
			event.period_num,
			event.strength,
			event.time,
			event.event_type,
			zone,
			event.description,
			event.away_on_ice,
			event.home_on_ice,
			end_time,
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
			winning_player = clone_rosterplayer(
				away_num, away_name, event.away_on_ice
				)
			losing_player = clone_rosterplayer(
				home_num, home_name, event.home_on_ice
				)
		else:
			losing_team = away_team
			winning_player = clone_rosterplayer(
				home_num, home_name, event.home_on_ice
				)
			losing_player = clone_rosterplayer(
				away_num, away_name, event.away_on_ice
				)

		return FaceOff(
			event.num,
			event.period_num,
			event.strength,
			event.time,
			event.event_type,
			zone,
			event.description,
			event.away_on_ice,
			event.home_on_ice,
			winning_player,
			losing_player,
			winning_team,
			losing_team
			)

	elif event.event_type == 'GIVE' or event.event_type == 'TAKE':

		zone = description_raw[-2]
		givetake_team = description_raw[0]
		givetake_num = description_raw[3].strip('#')

		anchor = Operations.index_containing_substring(description_raw, ',') + 1

		assert anchor != 0, "ERROR - Anchor not found"

		givetake_name = (" ".join(description_raw[4:anchor])).strip(',')

		if givetake_team == away_team:
			givetake_on_ice = event.away_on_ice
		
		elif givetake_team == home_team:
			givetake_on_ice = event.home_on_ice
			
		givetake_player = clone_rosterplayer(
			givetake_num, givetake_name, givetake_on_ice
			)

		if event.event_type == 'GIVE':
			return Give(
				event.num,
				event.period_num,
				event.strength,
				event.time,
				event.event_type,
				zone,
				event.description,
				event.away_on_ice,
				event.home_on_ice,
				givetake_player,
				givetake_team
				)

		elif event.event_type == 'TAKE':
			return Take(
				event.num,
				event.period_num,
				event.strength,
				event.time,
				event.event_type,
				zone,
				event.description,
				event.away_on_ice,
				event.home_on_ice,
				givetake_player,
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

		if shooting_team == away_team:
			shooting_on_ice = event.away_on_ice
			blocking_on_ice = event.home_on_ice
			blocking_team = home_team
		elif shooting_team == home_team:
			shooting_on_ice = event.home_on_ice
			blocking_on_ice = event.away_on_ice
			blocking_team = away_team
			
		for player in blocking_on_ice:
			if player.pos == 'G':
				blocking_player = player

		shooting_player = clone_rosterplayer(
			shooting_num, shooting_name, shooting_on_ice
			)
		
		return Shot(
			event.num,
			event.period_num,
			event.strength,
			event.time,
			event.event_type,
			zone,
			event.description,
			event.away_on_ice,
			event.home_on_ice,
			shot_type,
			distance,
			shooting_player,
			blocking_player,
			shooting_team,
			blocking_team
			)

	elif event.event_type == 'BLOCK':
		
		zone = description_raw[-2]
		shot_type = description_raw[-3].strip(',')
		shooting_team = description_raw[0]
		shooting_num = description_raw[1].strip('#')

		anchor1 = Operations.index_containing_substring(
			description_raw, 'BLOCKED'
			)
		anchor2 = Operations.index_containing_substring(
			description_raw, ','
			) + 1

		assert anchor1 != 0 and anchor2 != 0, "ERROR - Anchor not found"

		shooting_name = " ".join(description_raw[2:anchor1])

		shooting_player = (shooting_num, shooting_name)

		blocking_team = description_raw[anchor1 + 2]
		blocking_num = description_raw[anchor1 + 3].strip('#')
		blocking_name = (
			" ".join(description_raw[anchor1 + 4: anchor2])
			).strip (',')

		blocking_player = (blocking_num, blocking_name)

		if shooting_team == away_team:
			shooting_on_ice = event.away_on_ice
			blocking_on_ice = event.home_on_ice
		elif shooting_team == home_team:
			shooting_on_ice = event.home_on_ice
			blocking_on_ice = event.away_on_ice
		else:
			assert False, 'ERROR: shooting_team doesnt match home or away team'
			
		shooting_player =  clone_rosterplayer(
			shooting_num, shooting_name, shooting_on_ice
			)
		blocking_player =  clone_rosterplayer(
			blocking_num, blocking_name, blocking_on_ice
			)


		return Block(
			event.num,
			event.period_num,
			event.strength,
			event.time,
			event.event_type,
			zone,
			event.description,
			event.away_on_ice,
			event.home_on_ice,
			shot_type,
			shooting_player,
			blocking_player,
			shooting_team,
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
			shooting_on_ice = event.away_on_ice
			blocking_on_ice = event.home_on_ice
			blocking_team = home_team
		elif shooting_team == home_team:
			shooting_on_ice = event.home_on_ice
			blocking_on_ice = event.away_on_ice
			blocking_team = away_team
		else:
			assert False, 'ERROR: shooting_team doesnt match home or away team'
			
		for player in blocking_on_ice:
			if player.pos == 'G':
				blocking_player = player

		shooting_player =  clone_rosterplayer(
			shooting_num, shooting_name, shooting_on_ice
			)
		
		return Miss(
			event.num,
			event.period_num,
			event.strength,
			event.time,
			event.event_type,
			zone,
			event.description,
			event.away_on_ice,
			event.home_on_ice,
			shot_type,
			miss_type,
			distance,
			shooting_player,
			blocking_player,
			shooting_team,
			blocking_team
			)

	elif event.event_type == 'HIT':
		
		zone = description_raw[-2]
		hitting_team = description_raw[0]
		hitting_num = description_raw[1].strip('#')

		anchor1 = Operations.index_containing_substring(description_raw, 'HIT')
		anchor2 = Operations.index_containing_substring(description_raw, ',') + 1

		assert anchor1 != -1 and anchor2 != 0, "ERROR - Anchor not found"

		hitting_name = " ".join(description_raw[2:anchor1])

		hit_team = description_raw[anchor1 + 1]
		hit_num = description_raw[anchor1 + 2].strip('#')
		hit_name = (" ".join(description_raw[anchor1 + 3: anchor2])).strip (',')

		if hitting_team == away_team:
			hitting_on_ice = event.away_on_ice
			hit_on_ice = event.home_on_ice
			assert hit_team == home_team, \
				"ERROR: hit team internal check failure"
			
		elif hitting_team == home_team:
			hitting_on_ice = event.home_on_ice
			hit_on_ice = event.away_on_ice
			assert hit_team == away_team, \
				"ERROR: hit team internal check failure"

		hitting_player = clone_rosterplayer(hitting_num, hitting_name, hitting_on_ice)
		hit_player = clone_rosterplayer(hit_num, hit_name, hit_on_ice)

		return Hit(
			event.num,
			event.period_num,
			event.strength,
			event.time,
			event.event_type,
			zone,
			event.description,
			event.away_on_ice,
			event.home_on_ice,
			hitting_player,
			hit_player,
			hitting_team,
			hit_team
			)

	elif event.event_type == 'STOP':
		stopping_player = Roster.return_null_player()
		stopping_team = None
		zone = None
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
				if player.pos == 'Goalie':
					stopping_player = player


		elif "ICING" in description_raw:
			next_event = event_list[event_index + 1]
			next_description_raw = next_event.description.split ()
			winning_team = next_description_raw[0]
			winning_zone = next_description_raw[2]

			stopping_team, stopping_on_ice = Operations.team_responsible(
				winning_zone, winning_team, away_team, home_team, event
				)

		return Stop(
			event.num,
			event.period_num,
			event.strength,
			event.time,
			event.event_type,
			zone,
			event.description,
			event.away_on_ice,
			event.home_on_ice,
			description_parsed,
			stopping_player,
			stopping_team,
			tv_timeout,
			timeout_caller
			)

	elif event.event_type == 'GOAL':

		prim_assist_player = Roster.return_null_player()
		sec_assist_player = Roster.return_null_player()

		scoring_team = description_raw[0]
		scoring_num = description_raw[1].strip('#')

		if scoring_team == away_team:
			scoring_on_ice = event.away_on_ice
			defending_on_ice = event.home_on_ice
			defending_team = away_team
						
		elif scoring_team == home_team:
			scoring_on_ice = event.home_on_ice
			defending_on_ice = event.away_on_ice
			defending_team = home_team
			
		anchor1 = Operations.index_containing_substring(
			description_raw, ','
			) + 1
		anchor2 = Operations.index_containing_substring(
			description_raw[anchor1:], ','
			) + 1
		anchor3 = Operations.index_containing_substring(
			description_raw, 'ft.'
			)

		scoring_name = (" ".join(description_raw[2:anchor1]))[:-4]
		scoring_player = clone_rosterplayer(
			scoring_num, scoring_name, scoring_on_ice
			)
		
		shot_type = (" ".join(description_raw[anchor1:anchor1+anchor2])).strip(',')
		distance = description_raw[anchor3 - 1]
		zone = description_raw[anchor3 - 3]
		
		if 'Assist:' in description_raw:
			anchor4 = Operations.index_containing_substring(description_raw, 'Assist:') + 1
			
			prim_assist_num = description_raw[anchor4].strip('#')
			prim_assist_name = (" ".join(description_raw[anchor4 + 1:]))[:-3]
			prim_assist_player = clone_rosterplayer(
				prim_assist_num, prim_assist_name, scoring_on_ice
				)
			
		elif 'Assists:' in description_raw:
			anchor4 = Operations.index_containing_substring(
				description_raw, 'Assists:'
				) + 1
			anchor5 = Operations.index_containing_substring(
				description_raw, ';'
				) + 1
			
			prim_assist_num = description_raw[anchor4].strip('#')
			prim_assist_name = (" ".join(description_raw[anchor4 + 1:anchor5]))[:-4]
			prim_assist_player = clone_rosterplayer(
				prim_assist_num, prim_assist_name, scoring_on_ice
				)

			sec_assist_num = description_raw[anchor5].strip('#')
			sec_assist_name = (" ".join(description_raw[anchor5 + 1:]))[:-3]
			sec_assist_player = clone_rosterplayer(
				sec_assist_num, sec_assist_name, scoring_on_ice
				)

		for player in defending_on_ice:

			# For EN goals, no goalie is on the ice
			goalie = Roster.return_null_player()

			if player.pos == 'Goalie':
				goalie = player

		return Goal(
			event.num,
			event.period_num,
			event.strength,
			event.time,
			event.event_type,
			zone,
			event.description,
			event.away_on_ice,
			event.home_on_ice,
			shot_type,
			distance,
			scoring_player,
			scoring_team,
			prim_assist_player,
			sec_assist_player,
			goalie,
			defending_team
			)

	elif event.event_type == 'PENL':

		name_raw = event.description.split()

		penalized_team = name_raw[0]

		if penalized_team == home_team:
			drawing_team = away_team
			drawing_on_ice = event.away_on_ice
			drawing_roster = game_personnel.away_roster
			penalized_on_ice = event.home_on_ice
			penalized_roster = game_personnel.home_roster
		elif penalized_team == away_team:
			drawing_team = home_team
			drawing_roster = game_personnel.home_roster
			drawing_on_ice = event.home_on_ice
			penalized_on_ice = event.away_on_ice
			penalized_roster = game_personnel.away_roster

		# Grab the names first using standard splitting procedure

		for index, item in enumerate(name_raw[2:]):
			if not str(item).isupper():
				anchor1 = index + 2 # Because start index for loop is 2
				break

		penalized_num = name_raw[1].strip('#')
		penalized_name = " ".join(name_raw[2:anchor1])
		penalized_player = clone_rosterplayer(
			penalized_num, penalized_name, penalized_roster
			)

		# Grab other info using regex splitting procedure
		description_raw = re.split('\W+', event.description)
				
		for index, item in enumerate(description_raw[2:]):
			if not str(item).isupper():
				anchor2 = index + 2
				break
		
		anchor3 = description_raw.index('min') - 1
		anchor4 = description_raw.index('Zone') - 1
		length = description_raw [anchor3]
		penalty_type = " ".join(description_raw[anchor2:anchor3])
		zone = description_raw [anchor4]

		try:
			anchor5 = description_raw.index('By') + 1
			drawing_num = description_raw [anchor5 + 1].strip('#')
			drawing_name = " ".join(description_raw [anchor5 + 2:]).strip('#')
			drawing_player = clone_rosterplayer(
				drawing_num, drawing_name, drawing_roster
				)

		except ValueError:
			drawing_player = Roster.return_null_player()

		return Penalty(
			event.num, 
			event.period_num,
			event.strength,
			event.time,
			event.event_type,
			zone,
			event.description,
			event.away_on_ice,
			event.home_on_ice,
			penalty_type,
			length,
			penalized_player,
			drawing_player,
			penalized_team,
			drawing_team
			)

def harvest (year, game_num, report_type, game_type, game_info, game_personnel):
	'''
	Extract information from playbyplay html file and returns a 
	PlayByPlay object with which we run tests/create sql tables
	'''

	raw_events = raw_harvest (year, game_num, game_personnel.away_roster,
							  game_personnel.home_roster)

	playbyplay = PlayByPlay(raw_events)

	for index, event in enumerate(raw_events):

		pruned_event = event_prune(
			index, raw_events, game_personnel,
			game_info.away_team, game_info.home_team
			)
		# print pruned_event
				
		if pruned_event.event_type == 'BLOCK':
			playbyplay.blocks.append(pruned_event)
		elif pruned_event.event_type == 'FACE':
			playbyplay.faceoffs.append(pruned_event)
		elif pruned_event.event_type == 'GIVE':
			playbyplay.give_aways.append(pruned_event)
		elif pruned_event.event_type == 'GOAL':
			playbyplay.goals.append(pruned_event)
		elif pruned_event.event_type == 'HIT':
			playbyplay.hits.append(pruned_event)
		elif pruned_event.event_type == 'MISS':
			playbyplay.misses.append(pruned_event)
		elif pruned_event.event_type == 'PENL':
			playbyplay.penalties.append(pruned_event)
		elif pruned_event.event_type == 'PSTR':
			playbyplay.period_starts.append(pruned_event)
		elif pruned_event.event_type == 'SHOT':
			playbyplay.shots.append(pruned_event)		
		elif pruned_event.event_type == 'STOP':
			playbyplay.stops.append(pruned_event)
		elif pruned_event.event_type == 'TAKE':
			playbyplay.take_aways.append(pruned_event)

	return playbyplay

if __name__ == '__main__':
	
	year = '20152016'
	game_num = '0001'
	report_type = 'PL'
	game_type = '02'

	game_info = GameHeader.harvest(year, game_num, report_type, game_type)
	game_personnel = Roster.harvest (year, game_num)
	temp_pbp = harvest(year, game_num, report_type, game_type, game_info, game_personnel)
