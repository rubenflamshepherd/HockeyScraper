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