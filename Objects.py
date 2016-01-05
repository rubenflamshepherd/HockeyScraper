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