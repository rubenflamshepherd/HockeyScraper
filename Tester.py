import GameSummary
import PlayByPlay
import Roster
import unittest

class GameSummaryVsRoster (unittest.TestCase):

	def setUp(self):
		print 'In setUp()'
		self.roster = Roster.harvest ('20152016', '0003')
		self.game_summary = GameSummary.harvest ('20152016', '0003')

	def tearDown(self):
		print 'In tearDown()'
		del self.roster
		del self.game_summary

	def test_officials(self):
		for index, item in enumerate (self.game_summary.referees):

			self.assertEqual (item.num, self.roster.referees[index].num)
			self.assertEqual (item.first_name, self.roster.referees[index].first_name)
			self.assertEqual (item.last_name, self.roster.referees[index].last_name)

		for index, item in enumerate (self.game_summary.linesmen):
			self.assertEqual (item.num, self.roster.linesmen[index].num)
			self.assertEqual (item.first_name, self.roster.linesmen[index].first_name)
			self.assertEqual (item.last_name, self.roster.linesmen[index].last_name)

class GameSummaryVsPlayByPlay (unittest.TestCase):

	def setUp(self):
		print 'In setUp()'
		self.game_summary = GameSummary.harvest ('20152016', '0003')
		self.playbyplay = PlayByPlay.harvest('20152016', '0003', 'PL', '02') 

	def tearDown(self):
		print 'In tearDown()'
		del self.game_summary
		del self.playbyplay

	def test_goals (self):
		for index, goal in enumerate(self.playbyplay.goals):
			print goal	


if __name__ == '__main__':

	unittest.main()

	'''
	for item in temp_gamesummmary.referees:
		print item

	for item in temp_roster.referees:
		print item

	'''


