import GameHeader
import GameSummary
import PlayByPlay
import Roster

if __name__ == '__main__':

	year = '20152016'
	game_num = '0001'
	report_type = 'PL'
	game_type = '02'

	game_info = GameHeader.harvest(year, game_num, report_type, game_type)
	game_personnel = Roster.harvest (year, game_num)
	game_summary  = GameSummary.harvest (year, game_num, game_info, game_personnel)
	pbp = PlayByPlay.harvest(year, game_num, report_type, game_type, game_info, game_personnel)