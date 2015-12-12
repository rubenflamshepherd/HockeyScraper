class Coach:
	def __init__ (self, first_name, last_name):
		self.first_name = first_name
		self.last_name = last_name

	def __str__ (self):

		return str(self.first_name) + ' ' + str(self.last_name)

class Official:
	def __init__ (self, num, first_name, last_name):
		self.num = num
		self.first_name = first_name
		self.last_name = last_name

class Referee (Official):
	def __str__ (self):

		return "Referee: " + str(self.num) + ' ' + str(self.first_name) + ' ' + str(self.last_name)

class Linesman (Official):
	def __str__ (self):

		return "Linesman: " + str(self.num) + ' ' + str(self.first_name) + ' ' + str(self.last_name)
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

		return str(self.num) + '\n' + str(self.height) + '\n' + str(self.weight) + '\n' + str(self.hand)\
		+ '\n' + str(self.draft_team) + '\n' + str(self.draft_yr) + '\n' + str(self.draft_rnd)\
		+ '\n' + str(self.draft_overall) + '\n' + str(self.pos) + '\n' + str(self.twitter)

class Roster:
	def __init__ (self):
		self.num = None
		self.pos = None
		self.first_name = None
		self.last_name = None
		self.A_C = None
		self.starting = 0
		self.scratch = 0
		self.playerid = None

	def __str__ (self):

		return str(self.num) + ' ' + str(self.pos) + ' ' + str(self.first_name) + ' ' + str(self.last_name) + ' '\
		+ str(self.A_C) + ' ' + str(self.starting) + ' ' + str(self.scratch) + ' ' + str(self.playerid)

class GameInfo:
	def __init__(self, game_date, attendance_arena, game_start_end, game_num,\
					 away_score, away_team, away_team_game_nums,\
					 home_score, home_team, home_team_game_nums):
		self.game_date = game_date
		self.attendance_arena = attendance_arena
		self.game_start_end = game_start_end
		self.game_num = game_num
		self.away_score = away_score
		self.away_team = away_team
		self.away_team_game_nums = away_team_game_nums
		self.home_score = home_score
		self.home_team = home_team
		self.home_team_game_nums = home_team_game_nums



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

class PeriodStart(Event):

	def __init__ (self, num, per_num, strength, time, event_type, description, away_on_ice, home_on_ice,\
					start_time, time_zone):
		Event.__init__(self, num, per_num, strength, time,event_type, description, away_on_ice, home_on_ice)
		self.start_time = start_time
		self.time_zone = time_zone
	
	def __str__ (self):
		return self.num.encode('utf-8') + ' ' + self.per_num.encode('utf-8') + ' ' + \
		 self.strength.encode('utf-8') + ' ' + self.time.encode('utf-8') + ' ' + \
		 self.event_type.encode('utf-8') + ' ' + self.description.encode('utf-8') + '\nPeriod start: ' +\
		 self.start_time.encode('utf-8') + '\nTime zone:' + self.time_zone.encode('utf-8')

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
		return self.num.encode('utf-8') + ' ' + self.per_num.encode('utf-8') + ' ' + \
		 self.strength.encode('utf-8') + ' ' + self.time.encode('utf-8') + ' ' + \
		 self.event_type.encode('utf-8') + ' ' + self.description.encode('utf-8') + \
		 '\nZone: ' + self.zone.encode('utf-8') + \
		 '\nWP: ' + self.winning_player[0].encode('utf-8') + ' ' + self.winning_player[1].encode('utf-8') + \
		 '\nLP: ' + self.losing_player[0].encode('utf-8') + ' ' + self.losing_player[1].encode('utf-8') + \
		 '\nWT: ' + self.winning_team.encode('utf-8') + \
		 '\nLT: ' + self.losing_team.encode('utf-8')

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
		return self.num.encode('utf-8') + ' ' + self.per_num.encode('utf-8')\
		 + ' ' + self.strength.encode('utf-8') + ' ' + self.time.encode('utf-8')\
		 + ' ' + self.event_type.encode('utf-8') + ' ' + self.description.encode('utf-8')\
		 + '\nZone: ' + self.zone.encode('utf-8')\
		 + '\nShot type: ' + self.shot_type.encode('utf-8')\
		 + '\nDistance: ' + self.distance.encode('utf-8')\
		 + '\nSP: ' + self.shooting_player[0].encode('utf-8') + ' ' + self.shooting_player[1].encode('utf-8')\
		 + '\nBP: ' + self.blocking_player[0].encode('utf-8') + ' ' + self.blocking_player[1].encode('utf-8')\
		 + '\nST: ' + self.shooting_team.encode('utf-8')\
		 + '\nBT: ' + self.blocking_team.encode('utf-8')