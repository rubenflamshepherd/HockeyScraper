import GameHeader
import Operations
import re
import Roster
# encoding=utf8  
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

class Event(object):

	def __init__(self, num, period_num, strength, time, event_type, zone,
			description, away_acronym, home_acronym, away_on_ice, home_on_ice):

		self.num = num
		self.period_num = period_num
		self.strength = strength
		self.time = time
		self.event_type = event_type
		self.zone = zone
		self.description = description
		self.away_acronym = away_acronym
		self.home_acronym = home_acronym
		self.away_on_ice = away_on_ice
		self.home_on_ice = home_on_ice

	def create_prefix(self):

		event_num = ("\nE" + str(self.num).encode('utf-8')).ljust(5)
		period_num = (" P" + str(self.period_num).encode('utf-8')).ljust(3)
		strength = (" " + self.strength.encode('utf-8')).ljust(4)
		time = ("@" + self.time.encode('utf-8')).ljust(7)
		event_type = (self.event_type.encode('utf-8')).ljust(6)
		zone = (str(self.zone).encode('utf-8')).ljust(5)

		return event_num + period_num + strength + time + event_type + zone

	def __str__(self):

		event_num = ("\nE#" + str(self.num).encode('utf-8')).ljust(6)
		period_num = (" P#" + str(self.period_num).encode('utf-8')).ljust(4)
		strength = (" " + self.strength.encode('utf-8')).ljust(4)
		time = ("@" + self.time.encode('utf-8')).ljust(7)
		event_type = (self.event_type.encode('utf-8')).ljust(5)
		description = (self.description.encode('utf-8')).ljust(35) 

		return event_num + period_num + strength + time + event_type + description

class Block(Event):

	def __init__(self, num, per_num, strength, time, event_type, zone, 
				 description, away_acronym, home_acronym,
				 away_on_ice, home_on_ice, shot_type,
				 shooting_player, blocking_player, shooting_team, 
				 blocking_team):

		Event.__init__(self, num, per_num, strength, time, event_type, zone, 
			description, away_acronym, home_acronym, away_on_ice, home_on_ice)	
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

class End(Event):

	def __init__(self, num, per_num, strength, time, event_type, zone, 
		description, away_acronym, home_acronym, away_on_ice,
		home_on_ice, end_type, end_time, time_zone):
		
		Event.__init__(self, num, per_num, strength, time, event_type, zone, 
			description, away_acronym, home_acronym, away_on_ice, home_on_ice)
		self.end_type = end_type		
		self.end_time = end_time
		self.time_zone = time_zone
	
	def __str__(self):

		description = (self.end_type + '@' + self.end_time.__str__() + ' '\
			+ self.time_zone).ljust(35) 

		return self.create_prefix() + description

class FaceOff(Event):

	def __init__(self, num, per_num, strength, time, event_type, zone, 
		description, away_acronym, home_acronym, away_on_ice,
		home_on_ice, winning_player, losing_player, winning_team, losing_team):
		
		Event.__init__(self, num, per_num, strength, time, event_type, zone, 
			description, away_acronym, home_acronym, away_on_ice, home_on_ice)		
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
		description, away_acronym, home_acronym, away_on_ice,
		home_on_ice, giving_player, giving_team):
		
		Event.__init__(self, num, per_num, strength, time, event_type, zone, 
			description, away_acronym, home_acronym, away_on_ice, home_on_ice)
		self.giving_player = giving_player
		self.giving_team = giving_team
	
	def __str__ (self):

		giving_player = ('By ' + self.giving_team + ' ' \
			+  self.giving_player.show).ljust(25)		
		
		return self.create_prefix() + giving_player

class GameOff(Event):
	def __init__ (self, num, per_num, strength, time, event_type, zone, 
		description, away_acronym, home_acronym, away_on_ice,
		home_on_ice):

		Event.__init__(self, num, per_num, strength, time, event_type, zone, 
			description, away_acronym, home_acronym, away_on_ice, home_on_ice)

class Goal(Event):

	def __init__(self, num, per_num, strength, time, event_type, zone, 
		description, away_acronym, home_acronym, away_on_ice,
		home_on_ice, shot_type, distance, scoring_player, scoring_team, 
		prim_assist_player, sec_assist_player, goalie, defending_team):
		
		Event.__init__(self, num, per_num, strength, time, event_type, zone, 
			description, away_acronym, home_acronym, away_on_ice, home_on_ice)		
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
		distance = (str(self.distance).encode('utf-8') + 'ft').ljust(5)
		scoring_player = ('SP ' + self.scoring_player.show).ljust(15)		
		prim_assist_player = ('PA ' + self.prim_assist_player.show).ljust(15)		
		sec_assist_player = ('SA ' + self.sec_assist_player.show).ljust(15)		
		goalie = ('G ' + self.goalie.show).ljust(15)		


		return self.create_prefix() + shot_type + distance \
			+ scoring_player + prim_assist_player + sec_assist_player \
			+ goalie

class Hit(Event):

	def __init__(self, num, per_num, strength, time, event_type, zone,
		description, away_acronym, home_acronym, away_on_ice,
		home_on_ice, hitting_player, hit_player, hitting_team, hit_team):
		
		Event.__init__(self, num, per_num, strength, time, event_type, zone, 
			description, away_acronym, home_acronym, away_on_ice, home_on_ice)		
		self.hitting_player = hitting_player
		self.hit_player = hit_player
		self.hitting_team = hitting_team
		self.hit_team = hit_team
	
	def __str__ (self):

		hitting_player = ('Hitting ' + self.hitting_player.show).ljust(22)		
		hit_player = ('Hit ' + self.hit_player.show).ljust(22)

		return self.create_prefix() + hitting_player + hit_player

class Miss(Event):

	def __init__(self, num, per_num, strength, time, event_type, zone, 
		description, away_acronym, home_acronym, away_on_ice,
		home_on_ice, shot_type, miss_type, distance, 
		shooting_player, blocking_player, shooting_team, blocking_team):
		
		Event.__init__(self, num, per_num, strength, time, event_type, zone, 
			description, away_acronym, home_acronym, away_on_ice, home_on_ice)		
		self.shot_type = shot_type
		self.miss_type = miss_type
		self.distance = distance
		self.shooting_player = shooting_player
		self.blocking_player = blocking_player
		self.shooting_team = shooting_team
		self.blocking_team = blocking_team

	def __str__(self):

		shot_type = (str(self.shot_type).encode('utf-8')).ljust(8)		
		miss_type = (str(self.miss_type).encode('utf-8')).ljust(7)		
		distance = (str(self.distance).encode('utf-8')).ljust(4)
		shooting_player = ('SP ' + self.shooting_player.show).ljust(15)		
		blocking_player = ('BP ' + self.blocking_player.show).ljust(15)

		return self.create_prefix() + shot_type + distance + miss_type \
			+ shooting_player + blocking_player

class Penalty(Event):

	def __init__(self, num, per_num, strength, time, event_type, zone, 
	 	description, away_acronym, home_acronym, away_on_ice,
	 	home_on_ice, penalty_type, length, penalized_player, serving_player, 
	 	drawing_player, penalized_team, drawing_team):
		
		Event.__init__(self, num, per_num, strength, time, event_type, zone, 
			description, away_acronym, home_acronym, away_on_ice, home_on_ice)		
		self.penalty_type = penalty_type
		self.length = length
		self.penalized_player = penalized_player
		self.drawing_player = drawing_player
		self.penalized_team = penalized_team
		self.serving_player = serving_player
		self.drawing_team = drawing_team

	def __str__(self):

		penalty_type = (self.penalty_type.encode('utf-8')).ljust(10)		
		length = (str(self.length).encode('utf-8')).ljust(4)
		penalized_player = ('To ' + self.penalized_team + ' ' \
			+ self.penalized_player.show).ljust(15)		
		drawing_player = (' By ' + self.drawing_team + ' ' \
			+ self.drawing_player.show).ljust(15)		
		serving_player = (' Served By ' + self.penalized_team + ' ' \
			+ self.serving_player.show).ljust(15)		

		return self.create_prefix() + penalty_type + length \
			+ penalized_player + drawing_player + serving_player

class ShootoutCompletion(Event):
	def __init__(self, num, per_num, strength, time, event_type, zone, 
		description, away_acronym, home_acronym, away_on_ice,
		home_on_ice, start_time, time_zone):
		
		Event.__init__(self, num, per_num, strength, time, event_type, zone, 
			description, away_acronym, home_acronym, away_on_ice, home_on_ice)		
		self.end_time = start_time
		self.time_zone = time_zone

	def __str__(self):

		description = (self.end_time.__str__() + ' ' + self.time_zone).ljust(35) 

		return self.create_prefix() + description
	
class Shot(Event):

	def __init__(self, num, per_num, strength, time, event_type, zone, 
		description, away_acronym, home_acronym, away_on_ice,
		home_on_ice, shot_type, distance, 
		shooting_player, blocking_player, shooting_team, blocking_team):
		
		Event.__init__(self, num, per_num, strength, time, event_type, zone, 
			description, away_acronym, home_acronym, away_on_ice, home_on_ice)		
		self.shot_type = shot_type
		self.distance = distance
		self.shooting_player = shooting_player
		self.blocking_player = blocking_player
		self.shooting_team = shooting_team
		self.blocking_team = blocking_team
	
	def __str__(self):

		shot_type = (self.shot_type.encode('utf-8')).ljust(8)		
		distance = (str(self.distance).encode('utf-8')).ljust(4)
		shooting_player = ('SP ' + self.shooting_player.show).ljust(15)		
		blocking_player = ('BP ' + self.blocking_player.show).ljust(15)

		return self.create_prefix() + shot_type + distance \
			+ shooting_player + blocking_player

class Start(Event):

	def __init__(self, num, per_num, strength, time, event_type, zone, 
		description, away_acronym, home_acronym, away_on_ice,
		home_on_ice, start_type, start_time, time_zone):
		
		Event.__init__(self, num, per_num, strength, time, event_type, zone, 
			description, away_acronym, home_acronym, away_on_ice, home_on_ice)
		self.start_type = start_type		
		self.start_time = start_time
		self.time_zone = time_zone
	
	def __str__(self):

		description = (self.start_type + '@' + self.start_time.__str__() + ' '\
			+ self.time_zone).ljust(35) 

		return self.create_prefix() + description

class Stop(Event):

	def __init__(self, num, per_num, strength, time, event_type, zone, 
		description, away_acronym, home_acronym, away_on_ice,
		home_on_ice, description_parsed, 
		stopping_player, stopping_team, tv_timeout, timeout_caller):

		Event.__init__(self, num, per_num, strength, time, event_type, zone, 
			description, away_acronym, home_acronym, away_on_ice, home_on_ice)
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
		description, away_acronym, home_acronym, away_on_ice,
		home_on_ice, taking_player, taking_team):

		Event.__init__(self, num, per_num, strength, time, event_type, zone, 
			description, away_acronym, home_acronym, away_on_ice, home_on_ice)
		self.taking_player = taking_player
		self.taking_team = taking_team
	
	def __str__(self):
		
		taking_player = ('By ' + self.taking_team + ' ' + \
			self.taking_player.show).ljust(25)		
		
		return self.create_prefix() + taking_player

class PlayByPlay (object):

	def __init__(self, raw_events, pruned_events):

		self.raw_events = raw_events
		self.pruned_events = pruned_events
		self.blocks = []
		self.faceoffs = []
		self.give_takeaways = []
		self.goals = []
		self.hits = []
		self.misses = []
		self.penalties = []
		self.shots = []
		self.stops = []
		self.start_ends = []

		for event in self.pruned_events:
			if event.event_type == 'BLOCK':
				self.blocks.append(event)
			elif event.event_type == 'EGT' or event.event_type == 'EGPID':
				# No idea what these events are so just......
				pass
			elif event.event_type == 'FAC':
				self.faceoffs.append(event)
			elif event.event_type == 'GIVE' or event.event_type == 'TAKE':
				self.give_takeaways.append(event)
			elif event.event_type == 'GOAL':
				self.goals.append(event)
			elif event.event_type == 'GOFF':
				pass
			elif event.event_type == 'HIT':
				self.hits.append(event)
			elif event.event_type == 'MISS':
				self.misses.append(event)
			elif event.event_type == 'PENL':
				self.penalties.append(event)
			elif event.event_type == 'SHOT':
				self.shots.append(event)
			elif event.event_type == 'SOC':
				pass
			elif event.event_type == 'STOP':
				self.stops.append(event)
			elif event.event_type == 'GEND' or event.event_type == 'PEND' \
					or event.event_type == 'PSTR' or event.event_type == 'EISTR' \
					or event.event_type == 'EIEND':
				self.start_ends.append(event)

def prune_name(name_raw):
	'''
	Given a raw string that contains a player's name, prune chars obfuscating
	name and return name
	'''

	for index, char in enumerate(name_raw):
		if char.isalpha() == False and char != '-'and char != ' ' \
				and char != "'" and char != '.':
			end_anchor = index
			break
	return name_raw[:end_anchor]

def clone_rosterplayer (num, last_name, roster):
	'''
	Given basic player information, match that to a Roster.R_Player object in 
	roster and return that object
	'''

	for player in roster:
		#print player.num, player.last_name				
		if player.num == num and player.last_name == last_name:
			return player
	assert False, "ERROR: no matching player to %s %s"%(num, last_name)

def raw_harvest (year, game_num, away_acronym, home_acronym,
		away_roster, home_roster):
	"""
	Extract play-by-play information from a html file on the
	local machine (in the form of raw, unspeficied events).
	Returns list of unspecified event objects
	"""

	tree = Operations.germinate_report_seed(year,game_num,'PL','02')
	events = [] # empty list for holding unspecified events
	
	for item in tree.xpath('//table/tr[@class="evenColor"]'):
				
		event_raw = item.xpath('./td/text()')

		num = int(event_raw[0])
		per_num = int(event_raw[1])
		strength = unicode(event_raw[2])
		time = unicode(event_raw[3])
		event_type = unicode(event_raw[5])
		description = unicode(event_raw[6])
		try: # Zone not always indicated in event description
			# A bit redudant, done also before pruning events
			description_raw = description.split()
			zone_index = description_raw.index('Zone,') - 1
			zone = description_raw[zone_index]
		except ValueError:
			try: # Certain events have zone at end of description
				zone_index = description_raw.index('Zone') - 1
				zone = description_raw[zone_index]
			except ValueError:
				zone = None
		assert zone == 'Neu.' or zone == 'Off.' or zone == 'Def.' \
			or zone == None, "ERROR: Event zone(%s) invalid"%(zone)

		# Goals have an additional row in the description cell for assists
		if event_type == 'GOAL' and event_raw[7].find('Assist') != -1:
			description = unicode(" ".join(event_raw[6:8]))

		players_on_ice = item.xpath('./td/table')

		home_on_ice = []
		away_on_ice = []
			
		if len (players_on_ice) == 2: # Perhaps make this more robust?			
			away_on_ice = Operations.chop_on_ice_branch (
				players_on_ice[0], away_roster)
			home_on_ice = Operations.chop_on_ice_branch (
				players_on_ice[1], home_roster)

		event = Event(num, per_num, strength, time, event_type, zone, 
			description, away_acronym, home_acronym,
			away_on_ice, home_on_ice)		
		events.append (event)	    
	return events

def prune_block(event, description_raw, game_personnel):

	block_anchor = Operations.substring_index(description_raw, 'BLOCKED')[0]
	delim_index = Operations.substring_index(description_raw, ',')[0] + 1
	assert block_anchor != -1 and delim_index != 0, "ERROR - Anchor not found"
	assert 'Zone' in description_raw, "ERROR - 'Zone' not found"

	shot_type = description_raw[-3].strip(',')

	blocking_team = description_raw[block_anchor + 2]
	blocking_num = description_raw[block_anchor + 3].strip('#')
	blocking_name = (
		" ".join(description_raw[block_anchor + 4: delim_index])).strip (',')

	if blocking_team == event.home_acronym:
		shooting_on_ice = event.away_on_ice
		shooting_roster = game_personnel.away_roster
		blocking_on_ice = event.home_on_ice
		blocking_roster = game_personnel.home_roster
	elif blocking_team == event.away_acronym:
		shooting_on_ice = event.home_on_ice
		shooting_roster = game_personnel.home_roster
		blocking_on_ice = event.away_on_ice
		blocking_roster = game_personnel.away_roster
	else:
		assert False, 'ERROR: shooting_team(%s) doesnt match home (%s) or away\
			(%s) team'%(shooting_team, event.away_acronym, event.home_acronym)
		
	if block_anchor >= 3:
		shooting_name = " ".join(description_raw[2:block_anchor])
		shooting_team = description_raw[0]
		shooting_num = description_raw[1].strip('#')
		shooting_player =  clone_rosterplayer(
			shooting_num, shooting_name, shooting_roster)
	else: # NHL fucked up; loaded a blank shooter
		if blocking_team == event.away_acronym:
			shooting_team = event.home_acronym
		elif blocking_team == event.home_acronym:
			shooting_team = event.home_acronym
		shooting_player = Roster.return_null_player()

	blocking_player =  clone_rosterplayer(
		blocking_num, blocking_name, blocking_roster)

	return Block(
		event.num, event.period_num, event.strength, event.time,
		event.event_type, event.zone,	event.description, event.away_acronym,
		event.home_acronym, event.away_on_ice,
		event.home_on_ice, shot_type, shooting_player, blocking_player,
		shooting_team, blocking_team)

def prune_fac (event, description_raw, game_personnel):

	winning_team = description_raw[0]
	vs_anchor = description_raw.index('vs')
	away_team = description_raw[5]
	away_num = description_raw[6].strip('#')
	away_name = " ".join(description_raw[7:vs_anchor])
	home_team = description_raw[vs_anchor + 1]
	home_num = description_raw[vs_anchor + 2].strip('#')
	home_name = " ".join(description_raw[vs_anchor + 3:])

	if winning_team == away_team:
		losing_team = home_team
		winning_num, winning_name = away_num, away_name
		winning_roster = game_personnel.away_roster
		losing_num, losing_name = home_num, home_name
		losing_roster = game_personnel.home_roster
	elif winning_team == home_team:
		losing_team = away_team
		winning_num, winning_name = home_num, home_name
		winning_roster = game_personnel.home_roster
		losing_num, losing_name = away_num, away_name
		losing_roster = game_personnel.away_roster
	else:
		assert False, "ERROR: Which team(%s) won the faceoff??"%(winning_team)

	winning_player = clone_rosterplayer(
		winning_num, winning_name, winning_roster)
	losing_player = clone_rosterplayer(
		losing_num, losing_name, losing_roster)

	return FaceOff(
		event.num, event.period_num, event.strength, event.time, 
		event.event_type, event.zone, event.description, event.away_acronym,
		event.home_acronym, event.away_on_ice, event.home_on_ice,
		winning_player, losing_player, winning_team, losing_team)

def prune_give_take(event, description_raw, game_personnel):

	givetake_team = description_raw[0]
	givetake_num = description_raw[3].strip('#')

	delim_anchor = Operations.substring_index(description_raw, ',')[0] + 1

	assert delim_anchor != 0, "ERROR - Anchor not found"

	givetake_name = (" ".join(description_raw[4:delim_anchor])).strip(',')

	if givetake_team == event.away_acronym:
		givetake_on_ice = event.away_on_ice
		givetake_roster = game_personnel.away_roster	
	elif givetake_team == event.home_acronym:
		givetake_on_ice = event.home_on_ice
		givetake_roster = game_personnel.home_roster	
	else:
		assert False, "ERROR: Which team(%s) gave/took away??"%(givetake_team)
		
	givetake_player = clone_rosterplayer(
		givetake_num, givetake_name, givetake_roster)

	if event.event_type == 'GIVE':
		return Give(
			event.num, event.period_num, event.strength, event.time,
			event.event_type, event.zone, event.description, event.away_acronym,
			event.home_acronym, event.away_on_ice, event.home_on_ice, 
			givetake_player, givetake_team)
	elif event.event_type == 'TAKE':
		return Take(
			event.num, event.period_num, event.strength, event.time,
			event.event_type, event.zone, event.description, event.away_acronym,
			event.home_acronym, event.away_on_ice, event.home_on_ice, 
			givetake_player, givetake_team)

def prune_goal(event, description_raw, game_personnel):

	prim_assist_player = Roster.return_null_player()
	sec_assist_player = Roster.return_null_player()

	scoring_team = description_raw[0]
	scoring_num = description_raw[1].strip('#')

	if scoring_team == event.away_acronym:
		scoring_on_ice = event.away_on_ice
		scoring_roster = game_personnel.away_roster
		defending_on_ice = event.home_on_ice
		defending_roster = game_personnel.away_roster
		defending_team = event.away_acronym					
	elif scoring_team == event.home_acronym:
		scoring_on_ice = event.home_on_ice
		scoring_roster = game_personnel.home_roster
		defending_on_ice = event.away_on_ice
		defending_roster = game_personnel.home_roster
		defending_team = event.home_acronym
		
	name_anchor = Operations.substring_index(description_raw, ',')[0] + 1
	shot_anchor = Operations.substring_index(
		description_raw[name_anchor:], ',')[0] + name_anchor + 1
	distance_anchor = Operations.substring_index(description_raw, 'ft.')[0]

	scoring_name_raw = " ".join(description_raw[2:name_anchor])
	scoring_name = prune_name(scoring_name_raw)
	scoring_player = clone_rosterplayer(
		scoring_num, scoring_name, scoring_roster)
	
	shot_type = (" ".join(description_raw[name_anchor:shot_anchor])).strip(',')
	distance = description_raw[distance_anchor - 1]

	if 'Assist:' in description_raw:
		assist_anchor = Operations.substring_index(
			description_raw, 'Assist:')[0] + 1
		
		prim_assist_num = description_raw[assist_anchor].strip('#')
		prim_assist_name_raw = " ".join(description_raw[assist_anchor + 1:])
		prim_assist_name = prune_name(prim_assist_name_raw)
		prim_assist_player = clone_rosterplayer(
			prim_assist_num, prim_assist_name, scoring_roster)
		
	elif 'Assists:' in description_raw:
		assist_anchor = Operations.substring_index(
			description_raw, 'Assists:')[0] + 1
		sec_assist_anchor = Operations.substring_index(
			description_raw, ';')[0] + 1
		
		prim_assist_num = description_raw[assist_anchor].strip('#')
		prim_assist_name_raw = (
			" ".join(description_raw[assist_anchor + 1:sec_assist_anchor]))
		prim_assist_name = prune_name(prim_assist_name_raw)
		prim_assist_player = clone_rosterplayer(
			prim_assist_num, prim_assist_name, scoring_roster)

		sec_assist_num = description_raw[sec_assist_anchor].strip('#')
		sec_assist_name_raw = " ".join(description_raw[sec_assist_anchor + 1:])
		sec_assist_name = prune_name(sec_assist_name_raw)
		sec_assist_player = clone_rosterplayer(
			sec_assist_num, sec_assist_name, scoring_roster)

	for player in defending_on_ice:
		# For EN goals, no goalie is on the ice
		goalie = Roster.return_null_player()
		if player.pos == 'Goalie':
			goalie = player

	return Goal(
		event.num, event.period_num, event.strength, event.time,
		event.event_type, event.zone, event.description, event.away_acronym,
		event.home_acronym, event.away_on_ice,
		event.home_on_ice, shot_type, distance, scoring_player,
		scoring_team, prim_assist_player, sec_assist_player,
		goalie, defending_team)

def prune_goff (event, description_raw):
	zone = None
	return GameOff(
		event.num, event.period_num, event.strength, event.time, 
		event.event_type, zone, event.description, event.away_acronym,
		event.home_acronym, event.away_on_ice,
		event.home_on_ice)

def prune_hit(event, description_raw, game_personnel):

	hit_anchor = description_raw.index('HIT')
	delim_anchors = Operations.substring_index(description_raw, ',') 
	assert hit_anchor != -1, "ERROR - Anchor not found"

	if delim_anchors == []: # No zone entered in nhl report
		hit_name = (" ".join(
			description_raw[hit_anchor + 3:])).strip (',')
	else:
		name_anchor = delim_anchors[0] + 1
		hit_name = (" ".join(
			description_raw[hit_anchor + 3: name_anchor])).strip (',')

	hit_team = description_raw[hit_anchor + 1]
	hit_num = description_raw[hit_anchor + 2].strip('#')
	
	if hit_team == event.home_acronym:
		hitting_on_ice = event.away_on_ice
		hitting_roster = game_personnel.away_roster
		hit_on_ice = event.home_on_ice
		hit_roster = game_personnel.home_roster
	elif hit_team == event.away_acronym:
		hitting_on_ice = event.home_on_ice
		hitting_roster = game_personnel.home_roster
		hit_on_ice = event.away_on_ice
		hit_roster = game_personnel.away_roster
	else:
		assert False, 'ERROR: hit_team(%s) doesnt match home (%s) or away\
			(%s) team'%(hit_team, event.away_acronym, event.home_acronym)

	if hit_anchor >= 3:
		hitting_team = description_raw[0]
		hitting_num = description_raw[1].strip('#')
		hitting_name = " ".join(description_raw[2:hit_anchor])
		hitting_player = clone_rosterplayer(
			hitting_num, hitting_name, hitting_roster)
	else:# NHL fucked up; loaded a blank hitter
		if hit_team == event.away_acronym:
			hitting_team = event.home_acronym
		elif hit_team == event.home_acronym:
			hitting_team = event.home_acronym
		hitting_player = Roster.return_null_player()

	hit_player = clone_rosterplayer(hit_num, hit_name, hit_roster)

	return Hit(
		event.num, event.period_num, event.strength, event.time,
		event.event_type, event.zone, event.description, event.away_acronym,
		event.home_acronym, event.away_on_ice,
		event.home_on_ice, hitting_player, hit_player, hitting_team,
		hit_team)

def prune_miss(event, description_raw, game_personnel):

	delim_anchors = Operations.substring_index(description_raw, ',')
	delim_anchor = delim_anchors[0] + 1	
	assert delim_anchor != 0, "ERROR - Anchor not found"
	
	if len(delim_anchors) < 4: # Part of info is missing-usually shot/miss type
		shot_type = None
		miss_type = None
	else:
		shot_type = description_raw[-8].strip(',')
		miss_type = (" ".join(description_raw[delim_anchor + 1:-4])).strip(',')

	distance = description_raw[-2]
	shooting_team = description_raw[0]
	shooting_num = description_raw[1].strip('#')

	shooting_name = (" ".join(description_raw[2:delim_anchor])).strip(',')
	shooting_player = (shooting_num, shooting_name)

	if shooting_team == event.away_acronym:
		shooting_on_ice = event.away_on_ice
		shooting_roster = game_personnel.away_roster
		blocking_on_ice = event.home_on_ice
		blocking_team = event.home_acronym
		blocking_roster = game_personnel.home_roster
	elif shooting_team == event.home_acronym:
		shooting_on_ice = event.home_on_ice
		shooting_roster = game_personnel.home_roster
		blocking_on_ice = event.away_on_ice
		blocking_team = event.away_acronym
		blocking_roster = game_personnel.away_roster
	else:
		assert False, 'ERROR: shooting_team doesnt match home or away team'
	
	for player in blocking_on_ice:
		blocking_player = Roster.return_null_player()
		if player.pos == 'G':
			blocking_player = player

	shooting_player =  clone_rosterplayer(
		shooting_num, shooting_name, shooting_roster)
	
	return Miss(
		event.num, event.period_num, event.strength, event.time,
		event.event_type, event.zone, event.description, event.away_acronym,
		event.home_acronym, event.away_on_ice,
		event.home_on_ice, shot_type, miss_type, distance, shooting_player,
		blocking_player, shooting_team, blocking_team)

def prune_penl(event, description_raw, event_index, event_list, game_personnel):

	penalized_team_acronym = description_raw[0]

	if penalized_team_acronym == event.home_acronym:
		drawing_team = event.away_acronym
		drawing_on_ice = event.away_on_ice
		drawing_roster = game_personnel.away_roster
		penalized_on_ice = event.home_on_ice
		penalized_roster = game_personnel.home_roster
	elif penalized_team_acronym == event.away_acronym:
		drawing_team = event.home_acronym
		drawing_roster = game_personnel.home_roster
		drawing_on_ice = event.home_on_ice
		penalized_on_ice = event.away_on_ice
		penalized_roster = game_personnel.away_roster

	# Grabbing player information using normal split procedure

	# Grabbing penalized player	
	if description_raw[1] == 'TEAM': # No penalized player
		penalized_player = Roster.return_null_player()		
	else:
		for index, item in enumerate(description_raw[2:]):
			if not str(item).isupper():
				name_anchor = index + 2 # Because start index for loop is 2
				break
		penalized_num = description_raw[1].strip('#')
		penalized_name = " ".join(description_raw[2:name_anchor])
		penalized_player = clone_rosterplayer(
			penalized_num, penalized_name, penalized_roster)

	# Grabbing drawing player
	try:
		drawing_anchor = description_raw.index('Drawn') + 2
		drawing_num = description_raw [drawing_anchor + 1].strip('#')
		drawing_name = " ".join(description_raw [drawing_anchor + 2:])
		drawing_player = clone_rosterplayer(
			drawing_num, drawing_name, drawing_roster)
	except ValueError:
		drawing_player = Roster.return_null_player()

	# Grabbing serving player
	try:
		serving_anchor = description_raw.index('Served') + 2
		serving_num = description_raw [serving_anchor].strip('#')
		# Default end of serving name is last index in description_raw
		serving_name = " ".join(description_raw[serving_anchor + 1:])
		
		# However, zone information may be present at end of description_raw
		for index, item in enumerate(description_raw[serving_anchor + 1:]):
			if item.isupper() == False:
				# Because start index for loop is serving_anchor + 1
				end_serving_name = index + serving_anchor + 1 
				serving_name = " ".join(description_raw[serving_anchor + 1: end_serving_name]).strip(',')
				break
		serving_player = clone_rosterplayer(
			serving_num, serving_name, penalized_roster)
	except ValueError:
		serving_player = Roster.return_null_player()

	# Grab other info using regex splitting procedure
	regex_split = re.split('\W+', event.description)
				
	for index, item in enumerate(regex_split[2:]):
		if not str(item).isupper():
			penalty_start = index + 2
			break
	
	penalty_end = regex_split.index('min') - 1

	length = regex_split[penalty_end]
	penalty_type = " ".join(regex_split[penalty_start:penalty_end])

	return Penalty(
		event.num, event.period_num, event.strength, event.time,
		event.event_type, event.zone, event.description, event.away_acronym,
		event.home_acronym, event.away_on_ice,
		event.home_on_ice, penalty_type, length, penalized_player,
		serving_player, drawing_player,	penalized_team_acronym,	drawing_team)

def prune_soc(event, description_raw):

	end_time = description_raw[-2]
	time_zone = description_raw[-1]
	zone = 'Neu.'
	
	return ShootoutCompletion(
		event.num,	event.period_num, event.strength, event.time,
		event.event_type, zone,	event.description, event.away_acronym,
		event.home_acronym, event.away_on_ice,
		event.home_on_ice, end_time, time_zone)

def prune_shot(event, description_raw, game_personnel):
	
	distance = description_raw[-2]
	shot_type = description_raw[-5].strip(',')
	shooting_team = description_raw[0]
	shooting_num = description_raw[3].strip('#')

	delim_anchor = Operations.substring_index(description_raw, ',')[0] + 1

	assert delim_anchor != 0, "ERROR - Anchor not found"

	shooting_name = (" ".join(description_raw[4:delim_anchor])).strip(',')

	if shooting_team == event.away_acronym:
		shooting_on_ice = event.away_on_ice
		shooting_roster = game_personnel.away_roster
		blocking_on_ice = event.home_on_ice
		blocking_team = event.home_acronym
	elif shooting_team == event.home_acronym:
		shooting_on_ice = event.home_on_ice
		shooting_roster = game_personnel.home_roster
		blocking_on_ice = event.away_on_ice
		blocking_team = event.away_acronym
		
	for player in blocking_on_ice:
		if player.pos == 'G':
			blocking_player = player

	shooting_player = clone_rosterplayer(
		shooting_num, shooting_name, shooting_roster)
	
	return Shot(
		event.num, event.period_num, event.strength, event.time, 
		event.event_type, event.zone, event.description, event.away_acronym,
		event.home_acronym, event.away_on_ice,
		event.home_on_ice, shot_type, distance, shooting_player, 
		blocking_player, shooting_team, blocking_team)

def prune_start_end(event, event_description, description_raw):

	startend_raw = event_description.split('-')
	startend_type = startend_raw[0]
	startend_time = description_raw[-2]
	time_zone = description_raw[-1]
	zone = None
	
	if startend_type.find('Start') != -1:
		return Start(
			event.num, event.period_num, event.strength, event.time,
			event.event_type, zone,	event.description, event.away_acronym,
			event.home_acronym, event.away_on_ice,	event.home_on_ice,
			startend_type, startend_time, time_zone)
	elif startend_type.find('End') != -1:
		return End(
			event.num, event.period_num, event.strength, event.time,
			event.event_type, zone,	event.description, event.away_acronym,
			event.home_acronym, event.away_on_ice,	event.home_on_ice,
			startend_type, startend_time, time_zone)
	else:
		assert False, 'ERROR: Start/End find() failure'


def prune_stop(event, description_raw, event_index, event_list, game_personnel):

	stopping_player = Roster.return_null_player()
	stopping_team = None
	zone = None
	tv_timeout = 0
	timeout_caller = None

	description_raw = re.split('\W+', event.description)
	description_parsed = " ".join(description_raw)
	
	# Parse out 'TV TIMEOUT if not only item
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
		stopping_team, stopping_on_ice = Operations.team_responsible(
			event_index, event_list)
		for player in stopping_on_ice:
			if player.pos == 'Goalie':
				stopping_player = player
	elif "ICING" in description_raw:
		stopping_team, stopping_on_ice = Operations.team_responsible(
			event_index, event_list)

	return Stop(
		event.num, event.period_num, event.strength, event.time,
		event.event_type, zone,	event.description, event.away_acronym,
		event.home_acronym, event.away_on_ice,
		event.home_on_ice, description_parsed, stopping_player,
		stopping_team, tv_timeout, timeout_caller)

def prune_event(event_index, event_list, game_personnel):
	'''
	Given a string that is the description of an event, return an object of
	that event containing all possible data
	'''
	event = event_list[event_index]

	description_raw = event.description.split()
	# print description_raw
	if event.event_type == 'BLOCK':
		return prune_block(event, description_raw, game_personnel)
	elif event.event_type == 'EGT' or event.event_type == 'EGPID':
		# No idea what these events are so just......
		return event
	elif event.event_type == 'FAC':
		return prune_fac(event, description_raw, game_personnel)
	elif event.event_type == 'GIVE' or event.event_type == 'TAKE':
		return prune_give_take(event, description_raw, game_personnel)
	elif event.event_type == 'GOAL':
		return prune_goal(event, description_raw, game_personnel)
	elif event.event_type == 'GOFF':
		return prune_goff(event, description_raw)
	elif event.event_type == 'HIT':
		return prune_hit(event, description_raw, game_personnel)
	elif event.event_type == 'MISS':
		return prune_miss(event, description_raw, game_personnel)
	elif event.event_type == 'PENL':
		return prune_penl(event, description_raw, event_index, event_list, game_personnel)
	elif event.event_type == 'SHOT':
		return prune_shot(event, description_raw, game_personnel)
	elif event.event_type == 'SOC':
		return prune_soc(event, description_raw)
	elif event.event_type == 'STOP':
		return prune_stop(event, description_raw, event_index, event_list, game_personnel)
	elif event.event_type == 'GEND' or event.event_type == 'PEND' \
			or event.event_type == 'PSTR' or event.event_type == 'EISTR' \
			or event.event_type == 'EIEND':
		return prune_start_end(event, event.description, description_raw)
	else:
		print event
		assert False, "ERROR: WTF event is this?"

def harvest (year, game_num, report_type, game_type, game_info, game_personnel):
	'''
	Extract information from playbyplay html file and returns a 
	PlayByPlay object with which we run tests/create sql tables
	'''

	raw_events = raw_harvest(year, game_num, game_info.away_team,
		game_info.home_team, game_personnel.away_roster,
		game_personnel.home_roster)
	pruned_events = []

	for index, event in enumerate(raw_events):

		pruned_event = prune_event(index, raw_events, game_personnel)
		pruned_events.append(pruned_event)
		#if pruned_event.event_type == 'HIT':
		#	print pruned_event
			
		
	return PlayByPlay(raw_events, pruned_events)

if __name__ == '__main__':
	
	year = '20142015'
	report_type = 'PL'
	game_type = '02'

	for game_num_raw in range (7,8):
		game_num = Operations.pad_game_num (game_num_raw)
		
		game_info = GameHeader.harvest(year, game_num, report_type, game_type)
		game_personnel = Roster.harvest (year, game_num)
		temp_pbp = harvest(year, game_num, report_type, game_type, game_info, game_personnel)

		print game_info
		for item in temp_pbp.pruned_events:
			if item.event_type == 'PENL':
				print item
