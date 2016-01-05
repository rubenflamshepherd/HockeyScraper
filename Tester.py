import GameHeader
import GameSummary
import PlayByPlay
import Roster
import unittest

class GameSummaryVsRoster(unittest.TestCase):

	def setUp(self):

		year = '20142015'
		game_num = '0002'
		report_type = 'PL'
		game_type = '02'

		print 'In setUp()'
		self.game_info = GameHeader.harvest(year, game_num, report_type, game_type)
		self.game_personnel = Roster.harvest(year, game_num)
		self.game_summary = GameSummary.harvest(year, game_num, self.game_info, self.game_personnel)

	def tearDown(self):

		print 'In tearDown()'
		del self.game_personnel
		del self.game_summary

	def test_officials(self):

		for index, item in enumerate(self.game_summary.referees):
			self.assertEqual(item.num, self.game_personnel.referees[index].num)
			self.assertEqual(item.first_name, self.game_personnel.referees[index].first_name)
			self.assertEqual(item.last_name, self.game_personnel.referees[index].last_name)

		for index, item in enumerate(self.game_summary.linesmen):
			self.assertEqual(item.num, self.game_personnel.linesmen[index].num)
			self.assertEqual(item.first_name, self.game_personnel.linesmen[index].first_name)
			self.assertEqual(item.last_name, self.game_personnel.linesmen[index].last_name)

class GameSummaryVsPlayByPlay(unittest.TestCase):

	def setUp(self):

		year = '20142015'
		game_num = '0002'
		report_type = 'PL'
		game_type = '02'

		print 'In setUp()'
		self.game_info = GameHeader.harvest(year, game_num, report_type, game_type)
		self.game_personnel = Roster.harvest(year, game_num)
		self.game_summary = GameSummary.harvest(year, game_num, self.game_info, self.game_personnel)
		self.playbyplay = PlayByPlay.harvest(year, game_num, report_type, game_type, self.game_info, self.game_personnel)

	def tearDown(self):

		print 'In tearDown()'
		del self.game_summary
		del self.playbyplay

	def test_goals(self):

		self.assertEqual(len(self.playbyplay.goals), len(self.game_summary.goals))

		for index, pbp_goal in enumerate(self.playbyplay.goals):
			gs_goal = self.game_summary.goals[index]

			self.assertEqual(
				gs_goal.goal_num, \
				str(index + 1)
				)
			self.assertEqual(
				gs_goal.period_num, \
				pbp_goal.period_num
				)
			self.assertEqual(
				gs_goal.time, \
				pbp_goal.time
				)						
			self.assertEqual(
				gs_goal.scoring_player, \
				pbp_goal.scoring_player
				)
			self.assertEqual(
				gs_goal.prim_assist_player, \
				pbp_goal.prim_assist_player
				)
			self.assertEqual(
				gs_goal.sec_assist_player, \
				pbp_goal.sec_assist_player
				)

	def test_penalties(self):

		gs_penalties = len(self.game_summary.away_penalties) \
			+ len(self.game_summary.home_penalties)

		self.assertEqual(len(self.playbyplay.penalties), gs_penalties)

		away_counter = 0
		home_counter = 0

		for index, pbp_penalty in enumerate(self.playbyplay.penalties):
			if pbp_penalty.penalized_player.team == self.game_info.away_team:
				gs_penalty = self.game_summary.away_penalties[away_counter]
				away_counter += 1
			elif pbp_penalty.penalized_player.team == self.game_info.home_team:
				gs_penalty = self.game_summary.home_penalties[home_counter]
				home_counter += 1

			self.assertEqual(
				gs_penalty.period_num, \
				pbp_penalty.period_num
				)
			self.assertEqual(
				gs_penalty.time, \
				pbp_penalty.time
				)
			self.assertEqual(
				gs_penalty.length, \
				pbp_penalty.length
				)
			self.assertEqual(
				gs_penalty.penalized_player, \
				pbp_penalty.penalized_player
				)
			self.assertEqual(
				gs_penalty.penalty_type, \
				pbp_penalty.penalty_type
				)

	def test_byperiod (self):

		away_goals_dict = {}
		home_goals_dict = {}
		away_shots_dict = {}
		home_shots_dict = {}
		away_penalties_dict = {}
		home_penalties_dict = {}

		# Setting up dictionaries for tests
		for goal in self.playbyplay.goals:
			if goal.scoring_player.team == self.game_info.away_team:
				away_goals_dict.setdefault(goal.period_num, []).append(goal)
			elif goal.scoring_player.team == self.game_info.home_team:
				home_goals_dict.setdefault(goal.period_num, []).append(goal)

		for shot in self.playbyplay.shots:
			if shot.shooting_player.team == self.game_info.away_team:
				away_shots_dict.setdefault(shot.period_num, []).append(shot)
			elif goal.scoring_player.team == self.game_info.home_team:
				home_shots_dict.setdefault(shot.period_num, []).append(shot)
		
		for penalty in self.playbyplay.penalties:
			if penalty.penalized_player.team == self.game_info.away_team:
				away_penalties_dict.setdefault(
					penalty.period_num, []
					).append(penalty)
			elif penalty.penalized_player.team == self.game_info.home_team:
				home_penalties_dict.setdefault(
					penalty.period_num, []
					).append(penalty)

		# Running tests
		for period in self.game_summary.away_periods:
			# vars for tracking totals in Goalie.Field objects
			gs_goalie_num_goals = 0
			gs_goalie_num_shots = 0
			# away goals are scored on home_goalie
			for goalie in self.game_summary.home_goalies:
				for field in goalie.fields_list:
					if field.field_title == period.period_num and \
							field.field_content != None:
						field_goals = field.field_content.split('-')[0]
						field_shots = field.field_content.split('-')[1]
						gs_goalie_num_goals += int (field_goals)
						gs_goalie_num_shots += int (field_shots)
			
			if period.period_num in away_goals_dict:
				self.assertEqual(
					period.num_goals, \
					str(len(away_goals_dict[period.period_num]))
					)
				self.assertEqual(
					gs_goalie_num_goals,
					len(away_goals_dict[period.period_num])
					)
			if period.period_num in away_shots_dict:
				self.assertEqual(
					int(period.num_shots) - int(period.num_goals), \
					len(away_shots_dict[period.period_num])
					)
				self.assertEqual(
					gs_goalie_num_shots - gs_goalie_num_goals,
					len(away_shots_dict[period.period_num])
					)
			if period.period_num in away_penalties_dict:
				self.assertEqual(
					int(period.num_penalties), \
					len(away_penalties_dict[period.period_num])
					)
				
				PIM_counter = 0
				for item in away_penalties_dict[period.period_num]:
					PIM_counter += int(item.length)

				self.assertEqual(
					period.PIM, \
					str(PIM_counter)
					)

		for period in self.game_summary.home_periods:
			if period.period_num in home_goals_dict:
				self.assertEqual(
					period.num_goals, \
					str(len(home_goals_dict[period.period_num]))
					)

				gs_goalie_num_goals = 0
				# home goals are scored on away_goalie
				for goalie in self.game_summary.away_goalies:
					for field in goalie.fields_list:
						if field.field_title == period.period_num and \
								field.field_content != None:
							field_goals = field.field_content.split('-')[0]
							field_shots = field.field_content.split('-')[1]
							gs_goalie_num_goals += int (field_goals)
				self.assertEqual(
					gs_goalie_num_goals,
					len(home_goals_dict[period.period_num])
					)

			if period.period_num in home_shots_dict:
				self.assertEqual(
					int(period.num_shots) - int(period.num_goals), \
					len(home_shots_dict[period.period_num])
					)
			if period.period_num in home_penalties_dict:
				self.assertEqual (
					int(period.num_penalties), \
					len(home_penalties_dict[period.period_num])
					)

				PIM_counter = 0
				for item in home_penalties_dict[period.period_num]:
					PIM_counter += int(item.length)

				self.assertEqual(
					period.PIM, \
					str(PIM_counter)
					)

if __name__ == '__main__':

	unittest.main()