import unittest
import Roster
import GameSummary

temp_gamesummmary = GameSummary.harvest ('20152016', '0003')
temp_roster = Roster.harvest ('20152016', '0003')

class GameSummaryVsRoster (unittest.TestCase):
	'''
	Compares data in Game Summary and Roster Files
	'''

	temp_gamesummmary = GameSummary.harvest ('20152016', '0003')
	temp_roster = Roster.harvest ('20152016', '0003')

	def test_officials(self):
		for index, item in enumerate (temp_gamesummmary.referees):

			self.assertEqual (item.num, temp_roster.referees[index].num)
			self.assertEqual (item.first_name, temp_roster.referees[index].first_name)
			self.assertEqual (item.last_name, temp_roster.referees[index].last_name)

		for index, item in enumerate (temp_gamesummmary.linesmen):
			self.assertEqual (item.num, temp_roster.linesmen[index].num)
			self.assertEqual (item.first_name, temp_roster.linesmen[index].first_name)
			self.assertEqual (item.last_name, temp_roster.linesmen[index].last_name)

if __name__ == '__main__':

	unittest.main()

	'''
	for item in temp_gamesummmary.referees:
		print item

	for item in temp_roster.referees:
		print item

	'''


