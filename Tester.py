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

		self.assertEqual (len(self.playbyplay.goals), len (self.game_summary.goals))

		for index, pbp_goal in enumerate(self.playbyplay.goals):
			gs_goal = self.game_summary.goals[index]
			
			self.assertEqual (
				gs_goal.scoring_player.num, \
				pbp_goal.scoring_player.num
				)
			self.assertEqual (
				gs_goal.scoring_player.first_initial, \
				pbp_goal.scoring_player.first_name[0]
				)
			self.assertEqual (
				gs_goal.scoring_player.last_name, \
				pbp_goal.scoring_player.last_name
				)

			self.assertEqual (
				gs_goal.prim_assist_player.num, \
				pbp_goal.prim_assist_player.num
				)
			if pbp_goal.prim_assist_player.first_name == None:
				self.assertEqual (
					gs_goal.prim_assist_player.first_initial, \
					pbp_goal.prim_assist_player.first_name,
					pbp_goal.prim_assist_player.__str__() + '\n' \
						+ gs_goal.prim_assist_player.__str__()
					)
			else:
				self.assertEqual (
					gs_goal.prim_assist_player.first_initial, \
					pbp_goal.prim_assist_player.first_name[0]
					)
			self.assertEqual (
				gs_goal.prim_assist_player.last_name, \
				pbp_goal.prim_assist_player.last_name
				)

			self.assertEqual (
				gs_goal.sec_assist_player.num, \
				pbp_goal.sec_assist_player.num
				)
			if pbp_goal.sec_assist_player.first_name == None:
				self.assertEqual (
					gs_goal.sec_assist_player.first_initial, \
					pbp_goal.sec_assist_player.first_name
					)
			else:
				self.assertEqual (
					gs_goal.sec_assist_player.first_initial, \
					pbp_goal.sec_assist_player.first_name[0]
					)
			self.assertEqual (
				gs_goal.sec_assist_player.last_name, \
				pbp_goal.sec_assist_player.last_name
				)

if __name__ == '__main__':

	unittest.main()