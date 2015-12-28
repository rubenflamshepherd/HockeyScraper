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
		time = ("@" + self.time.encode('utf-8')).ljust(7)
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
		miss_type = (self.miss_type.encode('utf-8')).ljust(7)		
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

		zone = (self.zone.encode('utf-8')).ljust(5)		
		hitting_player = ('Hitting ' + self.hitting_player.show).ljust(22)		
		hit_player = ('Hit ' + self.hit_player.show).ljust(22)

		return self.create_prefix() + zone + hitting_player + hit_player

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

		description_parsed = self.description_parsed.ljust(20)
		stopping_player = ('By ' + str(self.stopping_team) + ' '\
			+ str(self.stopping_player.show)).ljust(19)
		tv_timeout = ('TVTO ' + str(self.tv_timeout)).ljust(8)
		to_caller = ('TOBy ' + str(self.timeout_caller)).ljust(15)

		return self.create_prefix() + description_parsed + stopping_player \
			+ tv_timeout + to_caller

class Give(Event):

	def __init__ (self, num, per_num, strength, time, event_type, description, away_on_ice, home_on_ice,\
					zone, giving_player, giving_team):
		Event.__init__(self, num, per_num, strength, time,event_type, description, away_on_ice, home_on_ice)
		self.zone = zone
		self.giving_player = giving_player
		self.giving_team = giving_team
	
	def __str__ (self):

		zone = (self.zone.encode('utf-8')).ljust(5)		
		giving_player = ('By ' + self.giving_player.show).ljust(25)		
		
		return self.create_prefix() + zone + giving_player

class Take(Event):

	def __init__ (self, num, per_num, strength, time, event_type, description, away_on_ice, home_on_ice,\
					zone, taking_player, taking_team):
		Event.__init__(self, num, per_num, strength, time,event_type, description, away_on_ice, home_on_ice)
		self.zone = zone
		self.taking_player = taking_player
		self.taking_team = taking_team
	
	def __str__ (self):
		
		zone = (self.zone.encode('utf-8')).ljust(5)		
		taking_player = ('By ' + self.taking_player.show).ljust(25)		
		
		return self.create_prefix() + zone + taking_player

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

		zone = (self.zone.encode('utf-8')).ljust(5)		
		shot_type = (self.shot_type.encode('utf-8')).ljust(8)		
		distance = (self.distance.encode('utf-8') + 'ft').ljust(5)
		scoring_player = ('SP ' + self.scoring_player.show).ljust(15)		
		prim_assist_player = ('PA ' + self.prim_assist_player.show).ljust(15)		
		sec_assist_player = ('SA ' + self.sec_assist_player.show).ljust(15)		
		goalie = ('G ' + self.goalie.show).ljust(15)		


		return self.create_prefix() + zone + shot_type + distance \
			+ scoring_player + prim_assist_player + sec_assist_player \
			+ goalie

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

		zone = (self.zone.encode('utf-8')).ljust(5)		
		penalty_type = (self.penalty_type.encode('utf-8')).ljust(10)		
		length = (self.length.encode('utf-8')).ljust(4)
		penalized_player = ('To ' + self.penalized_team + ' ' \
			+ self.penalized_player.show).ljust(15)		
		drawing_player = ('D By ' + self.drawing_team + ' ' \
			+ self.drawing_player.show).ljust(15)		
		
		return self.create_prefix() + zone + penalty_type + length \
			+ penalized_player + drawing_player
