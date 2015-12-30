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