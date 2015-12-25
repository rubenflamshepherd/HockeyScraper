# sys.setdefaultencoding() does not exist, here!
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

class Official:
	def __init__ (self, num, first_name, last_name):
		self.num = num
		self.first_name = first_name
		self.last_name = last_name

class Referee (Official):

	def __str__ (self):

		return "Referee: " + str(self.num) + ' ' + str(self.first_name) \
			+ ' ' + str(self.last_name) + '\n'

class Linesman (Official):

	def __str__ (self):

		return "Linesman: " + str(self.num) + ' ' + str(self.first_name) \
			+ ' ' + str(self.last_name) + '\n'

class Player:

	def __init__ (self):

		self.num = None
		self.height = None
		self.weight = None
		self.hand = None
		self.current_team = None
		self.draft_team = None
		self.draft_yr = None
		self.draft_rnd = None
		self.draft_overall = None
		self.pos = None
		self.twitter = None

	def __str__ (self):

		return str(self.num) + '\n' + str(self.height) + '\n' \
			+ str(self.weight) + '\n' + str(self.hand) + '\n' \
			+ str(self.draft_team) + '\n' + str(self.draft_yr) + '\n' \
			+  str(self.draft_rnd) + '\n' + str(self.draft_overall) + '\n' \
			+ str(self.pos) + '\n' + str(self.twitter)

class Event:

	def __init__ (self, num, per_num, strength, time,event_type, \
			description, away_on_ice, home_on_ice):

		self.num = num
		self.per_num = per_num
		self.strength = strength
		self.time = time
		self.event_type = event_type
		self.description = description
		self.away_on_ice = away_on_ice
		self.home_on_ice = home_on_ice

	def create_prefix(self):

		event_num = ("\nE" + self.num.encode('utf-8')).ljust(5)
		per_num = (" P" + self.per_num.encode('utf-8')).ljust(3)
		strength = (" " + self.strength.encode('utf-8')).ljust(4)
		time = ("@" + self.time.encode('utf-8')).ljust(6)
		event_type = (self.event_type.encode('utf-8')).ljust(6)

		return event_num + per_num + strength + time + event_type

	def __str__ (self):

		description = (self.description.encode('utf-8')).ljust(35) 

		return self.create_prefix() + description

class PeriodStart(Event):

	def __init__ (self, num, per_num, strength, time, event_type, description, away_on_ice, home_on_ice,\
					start_time, time_zone):
		Event.__init__(self, num, per_num, strength, time,event_type, description, away_on_ice, home_on_ice)
		self.start_time = start_time
		self.time_zone = time_zone
	

	def __str__ (self):

		description = (self.start_time.__str__() + ' ' + self.time_zone).ljust(35) 

		return self.create_prefix() + description
	
class FaceOff(Event):

	def __init__ (self, num, per_num, strength, time, event_type, description, away_on_ice, home_on_ice,\
					zone, winning_player, losing_player, winning_team, losing_team):
		Event.__init__(self, num, per_num, strength, time,event_type, description, away_on_ice, home_on_ice)
		self.zone = zone
		self.winning_player = winning_player
		self.losing_player = losing_player
		self.winning_team = winning_team
		self.losing_team = losing_team
	
	def __str__ (self):

		zone = (self.zone.encode('utf-8')).ljust(5)		
		winning_player = ('WP ' + self.winning_player.show).ljust(20)		
		losing_player = ('LP ' + self.losing_player.show).ljust(20)

		return self.create_prefix() + zone + winning_player + losing_player

class Shot(Event):

	def __init__ (self, num, per_num, strength, time, event_type, description, away_on_ice, home_on_ice,\
					zone, shot_type, distance, shooting_player, blocking_player, shooting_team, blocking_team):
		Event.__init__(self, num, per_num, strength, time,event_type, description, away_on_ice, home_on_ice)
		self.zone = zone
		self.shot_type = shot_type
		self.distance = distance
		self.shooting_player = shooting_player
		self.blocking_player = blocking_player
		self.shooting_team = shooting_team
		self.blocking_team = blocking_team
	
	def __str__ (self):

		shot_type = (self.shot_type.encode('utf-8')).ljust(8)		
		distance = (self.distance.encode('utf-8')).ljust(4)
		zone = (self.zone.encode('utf-8')).ljust(5)		
		shooting_player = ('SP ' + self.shooting_player.show).ljust(15)		
		blocking_player = ('BP ' + self.blocking_player.show).ljust(15)

		return self.create_prefix() + shot_type + distance + zone \
			+ shooting_player + blocking_player

class Block(Event):

	def __init__ (self, num, per_num, strength, time, event_type, description, away_on_ice, home_on_ice,\
					zone, shot_type, shooting_player, blocking_player, shooting_team, blocking_team):
		Event.__init__(self, num, per_num, strength, time,event_type, description, away_on_ice, home_on_ice)
		self.zone = zone
		self.shot_type = shot_type
		self.shooting_player = shooting_player
		self.blocking_player = blocking_player
		self.shooting_team = shooting_team
		self.blocking_team = blocking_team
	
	def __str__ (self):

		shot_type = (self.shot_type.encode('utf-8')).ljust(8)		
		zone = (self.zone.encode('utf-8')).ljust(5)		
		shooting_player = ('SP ' + self.shooting_player.show).ljust(20)		
		blocking_player = ('BP ' + self.blocking_player.show).ljust(20)

		return self.create_prefix() + shot_type + zone \
			+ shooting_player + blocking_player

class Miss(Event):

	def __init__ (self, num, per_num, strength, time, event_type, description, away_on_ice, home_on_ice,\
					zone, shot_type, miss_type, distance, shooting_player, blocking_player, shooting_team, blocking_team):
		Event.__init__(self, num, per_num, strength, time,event_type, description, away_on_ice, home_on_ice)
		self.zone = zone
		self.shot_type = shot_type
		self.miss_type = miss_type
		self.distance = distance
		self.shooting_player = shooting_player
		self.blocking_player = blocking_player
		self.shooting_team = shooting_team
		self.blocking_team = blocking_team

	def __str__ (self):

		shot_type = (self.shot_type.encode('utf-8')).ljust(8)		
		miss_type = (self.miss_type.encode('utf-8')).ljust(8)		
		distance = (self.distance.encode('utf-8')).ljust(4)
		zone = (self.zone.encode('utf-8')).ljust(5)		
		shooting_player = ('SP ' + self.shooting_player.show).ljust(15)		
		blocking_player = ('BP ' + self.blocking_player.show).ljust(15)

		return self.create_prefix() + shot_type + distance + zone + miss_type\
			+ shooting_player + blocking_player

class Hit(Event):

	def __init__ (self, num, per_num, strength, time, event_type, description, away_on_ice, home_on_ice,\
					zone, hitting_player, hit_player, hitting_team, hit_team):
		Event.__init__(self, num, per_num, strength, time,event_type, description, away_on_ice, home_on_ice)
		self.zone = zone
		self.hitting_player = hitting_player
		self.hit_player = hit_player
		self.hitting_team = hitting_team
		self.hit_team = hit_team
	
	def __str__ (self):
		return self.num.encode('utf-8') + ' ' + self.per_num.encode('utf-8')\
		 + ' ' + self.strength.encode('utf-8') + ' ' + self.time.encode('utf-8')\
		 + ' ' + self.event_type.encode('utf-8') + ' ' + self.description.encode('utf-8')\
		 + '\nZone: ' + self.zone.encode('utf-8')\
		 + '\nHittingP: ' + self.hitting_player[0].encode('utf-8') + ' ' + self.hitting_player[1].encode('utf-8')\
		 + '\nHitP: ' + self.hit_player[0].encode('utf-8') + ' ' + self.hit_player[1].encode('utf-8')\
		 + '\nHittingT: ' + self.hitting_team.encode('utf-8')\
		 + '\nHitT: ' + self.hit_team.encode('utf-8')

class Stop(Event):

	def __init__ (self, num, per_num, strength, time, event_type, description, away_on_ice, home_on_ice,\
					description_parsed, stopping_player, stopping_team, tv_timeout, timeout_caller):
		Event.__init__(self, num, per_num, strength, time,event_type, description, away_on_ice, home_on_ice)
		self.description_parsed = description_parsed
		self.stopping_player = stopping_player
		self.stopping_team = stopping_team
		self.tv_timeout = tv_timeout
		self.timeout_caller = timeout_caller
	
	def __str__ (self):
		return self.num.encode('utf-8') + ' ' + self.per_num.encode('utf-8')\
		 + ' ' + self.strength.encode('utf-8') + ' ' + self.time.encode('utf-8')\
		 + ' ' + self.event_type.encode('utf-8') + ' ' + self.description.encode('utf-8')\
		 + '\nDESCR Parsed: ' + self.description_parsed.encode('utf-8')\
		 + '\nST: ' + str(self.stopping_team)\
		 + '\nSP: ' + str(self.stopping_player[0]) + ' ' + str(self.stopping_player[1])\
		 + '\nTVTO: ' + str(self.tv_timeout)\
		 + '\nTO Caller: ' + str(self.timeout_caller)

class Give(Event):

	def __init__ (self, num, per_num, strength, time, event_type, description, away_on_ice, home_on_ice,\
					zone, giving_player, giving_team):
		Event.__init__(self, num, per_num, strength, time,event_type, description, away_on_ice, home_on_ice)
		self.zone = zone
		self.giving_player = giving_player
		self.giving_team = giving_team
	
	def __str__ (self):
		return self.num.encode('utf-8') + ' ' + self.per_num.encode('utf-8')\
		 + ' ' + self.strength.encode('utf-8') + ' ' + self.time.encode('utf-8')\
		 + ' ' + self.event_type.encode('utf-8') + ' ' + self.description.encode('utf-8')\
		 + '\nZone: ' + self.zone.encode('utf-8')\
		 + '\nPlayer: ' + self.giving_player[0].encode('utf-8') + ' ' + self.giving_player[1].encode('utf-8')\
		 + '\nTeam: ' + self.giving_team.encode('utf-8')

class Take(Event):

	def __init__ (self, num, per_num, strength, time, event_type, description, away_on_ice, home_on_ice,\
					zone, taking_player, taking_team):
		Event.__init__(self, num, per_num, strength, time,event_type, description, away_on_ice, home_on_ice)
		self.zone = zone
		self.taking_player = taking_player
		self.taking_team = taking_team
	
	def __str__ (self):
		return self.num.encode('utf-8') + ' ' + self.per_num.encode('utf-8')\
		 + ' ' + self.strength.encode('utf-8') + ' ' + self.time.encode('utf-8')\
		 + ' ' + self.event_type.encode('utf-8') + ' ' + self.description.encode('utf-8')\
		 + '\nZone: ' + self.zone.encode('utf-8')\
		 + '\nPlayer: ' + self.taking_player[0].encode('utf-8') + ' ' + self.taking_player[1].encode('utf-8')\
		 + '\nTeam: ' + self.taking_team.encode('utf-8')

class Goal(Event):

	def __init__ (self, num, per_num, strength, time, event_type, description, away_on_ice, home_on_ice,\
					zone, shot_type, distance, scoring_player, scoring_team, prim_assist_player, sec_assist_player,\
					goalie, defending_team):
		Event.__init__(self, num, per_num, strength, time,event_type, description, away_on_ice, home_on_ice)
		self.zone = zone
		self.shot_type = shot_type
		self.distance = distance
		self.scoring_player = scoring_player
		self.scoring_team = scoring_team
		self.prim_assist_player = prim_assist_player
		self.sec_assist_player = sec_assist_player
		self.goalie = goalie
		self.defending_team = defending_team

	def __str__ (self):
		return self.num.encode('utf-8') + ' ' + self.per_num.encode('utf-8')\
		 + ' ' + self.strength.encode('utf-8') + ' ' + self.time.encode('utf-8')\
		 + ' ' + self.event_type.encode('utf-8') + ' ' + self.description.encode('utf-8')\
		 + '\nZone: ' + self.zone.encode('utf-8')\
		 + '\nShot type: ' + self.shot_type.encode('utf-8')\
		 + '\nDistance: ' + self.distance.encode('utf-8')\
		 + '\nSP: ' + str(self.scoring_player[0]) + ' ' + str(self.scoring_player[1])\
		 + '\nPA: ' + str(self.prim_assist_player[0]) + ' ' + str(self.prim_assist_player[1])\
		 + '\nSA: ' + str(self.sec_assist_player[0]) + ' ' + str(self.sec_assist_player[1])\
		 + '\nGoalie: ' + str(self.goalie[0]) + ' ' + str(self.goalie[1])\
		 + '\nDT: ' + self.defending_team.encode('utf-8')

class Penalty(Event):

	def __init__ (self, num, per_num, strength, time, event_type, description, away_on_ice, home_on_ice,\
					zone, penalty_type, length, penalized_player, drawing_player, penalized_team, drawing_team):
		Event.__init__(self, num, per_num, strength, time,event_type, description, away_on_ice, home_on_ice)
		self.zone = zone
		self.penalty_type = penalty_type
		self.length = length
		self.penalized_player = penalized_player
		self.drawing_player = drawing_player
		self.penalized_team = penalized_team
		self.drawing_team = drawing_team

	def __str__ (self):
		return self.num.encode('utf-8') + ' ' + self.per_num.encode('utf-8')\
		 + ' ' + self.strength.encode('utf-8') + ' ' + self.time.encode('utf-8')\
		 + ' ' + self.event_type.encode('utf-8') + ' ' + self.description.encode('utf-8')\
		 + '\nZone: ' + self.zone.encode('utf-8')\
		 + '\nPenalty type: ' + self.penalty_type.encode('utf-8')\
		 + '\nLength: ' + self.length.encode('utf-8')\
		 + '\nPP: ' + str(self.penalized_player[0]) + ' ' + str(self.penalized_player[1])\
		 + '\nDP: ' + str(self.drawing_player[0]) + ' ' + str(self.drawing_player[1])\
		 + '\nPT: ' + str(self.penalized_team)\
		 + '\nDT: ' + str(self.drawing_team)
