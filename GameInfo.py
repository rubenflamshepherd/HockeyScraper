from lxml import html, etree
import Operations
import re
from datetime import datetime
from pytz import timezone

class GameInfo:
	def __init__(self, game_start, game_end, time_zone, attendance, arena, game_num,\
					 away_score, away_team, away_team_game_nums,\
					 home_score, home_team, home_team_game_nums):
		self.game_start = game_start
		self.game_end = game_end
		self.time_zone = time_zone
		self.attendance = attendance
		self.arena = arena
		self.game_num = game_num
		self.away_score = away_score
		self.away_team = away_team
		self.away_team_game_nums = away_team_game_nums
		self.home_score = home_score
		self.home_team = home_team
		self.home_team_game_nums = home_team_game_nums

	def __str__ (self):

		return '\nAttendance: ' + str(self.attendance)\
				 + '\nGame Num: ' + str(self.game_num)\
				 + '\n' + str(self.away_team) + ' vs ' + str(self.home_team)\
				 + '\n' + str(self.away_score) + ' - ' + str(self.home_score)\
				 + '\nAway ' + str(self.away_team_game_nums)\
				 + '\nHome ' + str(self.home_team_game_nums)


def harvest (year, game_num, report_type, game_type):
	'''
	Extract information about a game (attendance, home team, etc.) from an
	standard header on html report (via an xml tree) stored as a local file.
	Return a GameInfo object.
	'''
	
	tree = Operations.germinate_report_seed(
		year, game_num, report_type, game_type
		)
	
	away_info_raw = tree.xpath(
		'//tr/td[@valign="top"]/table[@id="Visitor"]'
		)[0]
	away_score = away_info_raw.xpath(
		'.//td[@style="font-size: 40px;font-weight:bold"]/text()'
		)[0]
	away_team_raw = away_info_raw.xpath(
		'.//td[@style="font-size: 10px;font-weight:bold"]/text()'
		)[0]
	away_team_game_nums = away_info_raw.xpath(
		'.//td[@style="font-size: 10px;font-weight:bold"]/text()'
		)[1]

	home_info_raw = tree.xpath(
		'//tr/td[@valign="top"]/table[@id="Home"]'
		)[0]
	home_score = home_info_raw.xpath(
		'.//td[@style="font-size: 40px;font-weight:bold"]/text()'
		)[0]
	home_team_raw = home_info_raw.xpath(
		'.//td[@style="font-size: 10px;font-weight:bold"]/text()'
		)[0]
	home_team_game_nums = home_info_raw.xpath(
		'.//td[@style="font-size: 10px;font-weight:bold"]/text()'
		)[1]

	game_info_raw = tree.xpath(
		'//tr/td/table[@id="GameInfo"]'
		)[0]

	game_date_raw = game_info_raw.xpath(
		'.//td[@style="font-size: 10px;font-weight:bold"]/text()'
		)[0]
	game_date_raw = re.split('\W+', game_date_raw)
	game_month = Operations.convert_month_str (game_date_raw[1])
	game_day = int(game_date_raw[2])
	game_yr = int(game_date_raw[3])


	attendance_arena_raw = game_info_raw.xpath(
		'.//td[@style="font-size: 10px;font-weight:bold"]/text()'
		)[1].split()
	attendance_raw = attendance_arena_raw[1]
	
	anchor1 = attendance_raw.find(',')
	
	if anchor1 != -1:
		attendance_raw = attendance_raw[:anchor1] + attendance_raw[anchor1 + 1 :]
	attendance = int(attendance_raw)

	anchor2 = attendance_arena_raw.index('at') + 1

	assert anchor2 != 0,"ERROR: no anchor for indexing arena name"
	arena = " ".join (attendance_arena_raw[anchor2:])
	print arena, attendance
	
	print attendance_arena_raw
	
	game_start_end = game_info_raw.xpath(
		'.//td[@style="font-size: 10px;font-weight:bold"]/text()'
		)[2]
	game_start_end = re.split('\W+', game_start_end)

	game_start_hr = int(game_start_end[1])
	game_start_min = int(game_start_end[2])
	game_start_tz = game_start_end[3]

	game_end_hr = int(game_start_end[5])
	game_end_min = int(game_start_end[6])
	game_end_tz = game_start_end[7]

	assert game_start_tz == game_end_tz, "ERROR: tz start/end dont match"
	time_zone = game_start_tz

	game_start = datetime (
		game_yr, \
		game_month, \
		game_day, \
		game_start_hr, \
		game_start_min, \
		0, \
		0
		)

	game_end = datetime (
		game_yr, \
		game_month, \
		game_day, \
		game_end_hr, \
		game_end_min, \
		0, \
		0
		)
	
	game_num = game_info_raw.xpath(
		'.//td[@style="font-size: 10px;font-weight:bold"]/text()'
		)[3]
	report_type = game_info_raw.xpath(
		'.//td[@style="font-size: 10px;font-weight:bold"]/text()'
		)[4]

	away_team = Operations.team_name_to_acronym (away_team_raw)
	home_team = Operations.team_name_to_acronym (home_team_raw)

	return GameInfo (
		game_start, game_end, time_zone, attendance, arena, game_num,\
		away_score, away_team, away_team_game_nums,\
		home_score, home_team, home_team_game_nums
		)

if __name__ == '__main__':
	print harvest ('20152016', '0003', 'PL', '02')
