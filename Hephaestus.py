import Database
import GameHeader
import GameSummary
import PlayerPage
import PlayByPlay
import Roster
import sqlite3

if __name__ == '__main__':
	'''

	year = '20152016'
	game_num = '0001'
	report_type = 'PL'
	game_type = '02'

	game_info = GameHeader.harvest(year, game_num, report_type, game_type)
	game_personnel = Roster.harvest (year, game_num)
	game_summary  = GameSummary.harvest (year, game_num, game_info, game_personnel)
	pbp = PlayByPlay.harvest(year, game_num, report_type, game_type, game_info, game_personnel)
	'''

	'''
	playerid = 8471716
	# Db connection to grab player pos (and update with grabbed data later)
	conn = sqlite3.connect('nhl.db')
	c = conn.cursor()
	c.execute("SELECT * FROM all_players WHERE playerid = ?", (playerid,))
	temp_return = c.fetchone()
	pos = temp_return[3]
	conn.commit()
	conn.close()
	
	player_temp = PlayerPage.harvest(playerid, pos)
	Database.ripen_player(player_temp)
	'''
	#Database.germinate_all_players_table()
	#Database.germinate_seasons_table()
	#Database.grow_all_players()
	Database.ripen_all_players()