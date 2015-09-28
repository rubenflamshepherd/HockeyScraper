class Player:
	def __init__ (self):
		self.num = None
		self.height = None
		self.weight = None
		self.hand = None
		self.draft_team = None
		self.draft_yr = None
		self.draft_rnd = None
		self.draft_overall = None
		self.pos = None
		self.twitter = None


	def __str__ (self):

		return self.num + '\n' + self.height + '\n' + self.weight + '\n' + self.hand\
		+ '\n' + self.draft_team + '\n' + self.draft_yr + '\n' + self.draft_rnd\
		+ '\n' + self.draft_overall + '\n' + self.pos + '\n' + self.twitter

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