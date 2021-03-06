from lxml import html, etree
import Operations
import re
from datetime import datetime
from pytz import timezone

class GameHeader:
	def __init__(self, game_start, game_end, time_zone, attendance, arena, 
			game_num, away_score, away_team, away_game_num, away_away_game_num, 
			home_score, home_team, home_game_num, home_home_game_num):
		self.game_start = game_start
		self.game_end = game_end
		self.time_zone = time_zone
		self.attendance = attendance
		self.arena = arena
		self.game_num = game_num
		self.away_score = away_score
		self.away_team = away_team # as acronym
		self.away_game_num = away_game_num
		self.away_away_game_num = away_away_game_num
		self.home_score = home_score
		self.home_team = home_team # as acronym
		self.home_game_num = home_game_num
		self.home_home_game_num = home_home_game_num

	def __str__ (self):

		game_num = 'Game ' + self.game_num + ' | '
		attendance_arena = str(self.attendance) + ' at ' + str(self.arena)
		game_start = ('\nStart ' + self.game_start.__str__()  + ' ' \
			+ self.time_zone).ljust(35)
		game_end = ('End ' + self.game_end.__str__() + ' ' \
			+ self.time_zone).ljust(35)
		team_header = '\n' + self.away_team.ljust(35) \
			+ self.home_team.ljust(40)

		away_header = ('\nGame ' + self.away_game_num + ' Away Game ' \
			+ self.away_away_game_num).ljust(35)
		home_header = ('Game ' + self.home_game_num + ' Home Game ' \
			+ self.home_home_game_num).ljust(35)

		score_header = '\n' + self.away_score.ljust(35) \
			+ self.home_score.ljust(35)

		return game_num + attendance_arena + game_start + game_end \
			+ team_header + away_header + home_header + score_header
				 


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
		)[1].split()
	away_team_game_num = away_team_game_nums[1]
	away_team_away_game_num = away_team_game_nums[-1]

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
		)[1].split()
	home_team_game_num = home_team_game_nums[1]
	home_team_away_game_num = home_team_game_nums[-1]

	game_info_raw = tree.xpath(
		'//tr/td/table[@id="GameInfo"]'
		)[0]

	game_date_raw = game_info_raw.xpath(
		'.//td[@style="font-size: 10px;font-weight:bold"]/text()')[0]
	if game_date_raw.find('NHL Winter Classic') != -1 or\
			game_date_raw.find('Stadium Series') != -1:
		game_date_raw = game_info_raw.xpath(
			'.//td[@style="font-size: 10px;font-weight:bold"]/text()')[1]
		location_index = 2
		time_index = 3
		num_index = 4
		report_index = 5
	else:
		location_index = 1
		time_index = 2
		num_index = 3
		report_index = 4
		
	
	game_date_raw = re.split('\W+', game_date_raw)
	game_month = Operations.convert_month_str (game_date_raw[1])
	game_day = int(game_date_raw[2])
	game_yr = int(game_date_raw[3])


	attendance_arena_raw = game_info_raw.xpath(
		'.//td[@style="font-size: 10px;font-weight:bold"]/text()'
		)[location_index].split()
	attendance_raw = attendance_arena_raw[1]
	
	delim_anchor = attendance_raw.find(',')
	
	if delim_anchor != -1:
		attendance_raw = attendance_raw[:delim_anchor] \
		+ attendance_raw[delim_anchor + 1 :]
	attendance = int(attendance_raw)

	try:
		at_anchor = attendance_arena_raw.index('at') + 1
		arena = " ".join (attendance_arena_raw[at_anchor:])
	except ValueError:
		arena = None
		
	game_start_end = game_info_raw.xpath(
		'.//td[@style="font-size: 10px;font-weight:bold"]/text()'
		)[time_index]
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
		game_yr, game_month, game_day, game_start_hr, game_start_min, 0, 0)

	game_end = datetime (
		game_yr, game_month, game_day, game_end_hr, game_end_min, 0, 0)
	
	game_num_raw = game_info_raw.xpath(
		'.//td[@style="font-size: 10px;font-weight:bold"]/text()'
		)[num_index]
	game_num = game_num_raw.split()[-1]
	report_type = game_info_raw.xpath(
		'.//td[@style="font-size: 10px;font-weight:bold"]/text()'
		)[report_index]

	away_team = Operations.team_name_to_acronym (away_team_raw)
	home_team = Operations.team_name_to_acronym (home_team_raw)

	return GameHeader (
		game_start, game_end, time_zone, attendance, arena, game_num,
		away_score, away_team, away_team_game_num, away_team_away_game_num,
		home_score, home_team, home_team_game_num, away_team_away_game_num
		)

if __name__ == '__main__':
	temp = harvest ('20152016', '0002', 'PL', '02')
	print temp.game_start.year
