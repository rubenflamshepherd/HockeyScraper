import GameHeader
import Operations
from lxml import html, etree

class ES_Player:

	def __init__ (self, team_acronym, num, position, first_name, last_name,
			goals, assists, points, plus_minus, num_penalties, pim, total_minutes,
			num_shifts, avg_shift_length, powerplay_minutes,
			shorthanded_minutes, evenstrength_minutes, shots,
			attempts_blocked, missed_shots, hits, give_aways, take_aways,
			blocked_shots, faceoff_wins, faceoff_losses, faceoff_percentage,
			playerid):

		self.team_acronym = team_acronym
		self.num = num
		self.position = position
		self.first_name = first_name
		self.last_name = last_name
		self.goals = goals
		self.assists = assists
		self.points = points
		self.plus_minus = plus_minus
		self.num_penalties = num_penalties
		self.pim = pim
		self.total_minutes = total_minutes
		self.num_shifts = num_shifts
		self.avg_shift_length = avg_shift_length
		self.powerplay_minutes = powerplay_minutes
		self.shorthanded_minutes = shorthanded_minutes
		self.evenstrength_minutes = evenstrength_minutes
		self.shots = shots
		self.attempts_blocked = attempts_blocked
		self.missed_shots = missed_shots
		self.hits = hits
		self.give_aways = give_aways
		self.take_aways = take_aways
		self.blocked_shots = blocked_shots
		self.faceoff_losses = faceoff_losses
		self.faceoff_wins = faceoff_wins
		self.faceoff_percentage = faceoff_percentage
		self.playerid = playerid

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.__dict__ == other.__dict__
		else:
			return False

	def __ne__(self, other):
		return not self.__eq__(other)

	def __str__(self):

		team_acronym = (self.team_acronym.encode('utf-8')).ljust(4)
		num = (self.num.encode('utf-8')).ljust(3)
		position = (self.position.encode('utf-8')).ljust(2)

		name_raw = self.first_name.encode('utf-8') + ' ' \
			+ self.last_name.encode('utf-8')
		name = (name_raw).ljust(25)

		goals = (self.goals.encode('utf-8')).ljust(2)
		assists = (self.assists.encode('utf-8')).ljust(2)
		points = (self.points.encode('utf-8')).ljust(2)
		plus_minus = (self.plus_minus.encode('utf-8')).ljust(3)
		num_penalties = (self.num_penalties.encode('utf-8')).ljust(2)
		pim = (self.pim.encode('utf-8')).ljust(3)
		total_minutes = (self.total_minutes.encode('utf-8')).ljust(6)
		num_shifts = (self.num_shifts.encode('utf-8')).ljust(3)
		avg_shift_length = (self.avg_shift_length.encode('utf-8')).ljust(6)
		powerplay_minutes = (self.powerplay_minutes.encode('utf-8')).ljust(6)
		shorthanded_minutes = (self.shorthanded_minutes.encode('utf-8')).ljust(6)
		evenstrength_minutes = (self.evenstrength_minutes.encode('utf-8')).ljust(6)
		shots = (self.shots.encode('utf-8')).ljust(3)
		attempts_blocked = (self.attempts_blocked.encode('utf-8')).ljust(3)
		missed_shots = (self.missed_shots.encode('utf-8')).ljust(3)
		hits = (self.hits.encode('utf-8')).ljust(3)
		give_aways = (self.give_aways.encode('utf-8')).ljust(3)
		take_aways = (self.take_aways.encode('utf-8')).ljust(3)
		blocked_shots = (self.blocked_shots.encode('utf-8')).ljust(3)
		faceoff_wins = (self.faceoff_wins.encode('utf-8')).ljust(3)
		faceoff_losses = (self.faceoff_losses.encode('utf-8')).ljust(3)
		faceoff_percentage = (self.faceoff_percentage.encode('utf-8')).ljust(4)

		playerid = ("ID " + str(self.playerid)).ljust(10)

		return team_acronym + num + position + name + goals + assists + points + \
			plus_minus + num_penalties + pim + total_minutes + \
			num_shifts + avg_shift_length + powerplay_minutes + \
			shorthanded_minutes + evenstrength_minutes + shots + \
			attempts_blocked + missed_shots + hits + give_aways + take_aways + \
			blocked_shots +	faceoff_wins + faceoff_losses + \
			faceoff_percentage + '\n'

def chop_team_summary(tree):
	pass

def harvest(year, game_num):

	game_info = GameHeader.harvest (year, game_num, 'RO', '02')
	away_full_name = Operations.team_acronym_to_uppercase(
		game_info.away_team)
	home_full_name = Operations.team_acronym_to_uppercase(
		game_info.home_team)

	tree = Operations.germinate_report_seed (year, game_num, "ES", '02')

	tables = tree.xpath('//table[@class="tablewidth" and @align="center"]/tr/td/table[@width="100%"]')
	rows = tables[3].xpath('./tr')

	roster = []
	team_acronym = game_info.away_team
	
	for item in rows:
		if item.xpath('./td/text()')[0] == home_full_name:
			away_roster = roster
			roster = []
			team_acronym = game_info.home_team
		elif item.get('class') == 'evenColor' or\
				item.get('class') == 'oddColor':
			fields = item.xpath('./td/text()')
			for index, field in enumerate(fields):
				if field == u'\xa0':
					field = '0'

				if index == 0:
					number = field
				elif index == 1:
					position = field
				elif index == 2:
					name_raw = field.split(', ')
					first_name = name_raw[1]
					last_name = name_raw[0]
				elif index == 3:
					goals = field					
				elif index == 4:
					assists = field
				elif index == 5:
					points = field
				elif index == 6:
					plus_minus = field
				elif index == 7:
					num_penalties = field
				elif index == 8:
					pim = field
				elif index == 9:
					total_minutes = field
				elif index == 10:
					num_shifts = field
				elif index == 11:
					avg_shift_length = field
				elif index == 12:
					powerplay_minutes = field
				elif index == 13:
					shorthanded_minutes = field
				elif index == 14:
					evenstrength_minutes = field
				elif index == 15:
					shots = field
				elif index == 16:
					attempts_blocked = field
				elif index == 17:
					missed_shots = field
				elif index == 18:
					hits = field
				elif index == 19:
					give_aways = field
				elif index == 20:
					take_aways = field
				elif index == 21:
					blocked_shots = field
				elif index == 22:
					faceoff_wins = field
				elif index == 23:
					faceoff_losses = field
				elif index == 24:
					faceoff_percentage = field

			playerid = Operations.get_playerid(first_name, last_name, 
				team_acronym, year,	position)
			
			roster.append (ES_Player(team_acronym, number, position,
				first_name, last_name, goals, assists, points, plus_minus,
				num_penalties, pim, total_minutes, num_shifts,
				avg_shift_length, powerplay_minutes, shorthanded_minutes,
				evenstrength_minutes, shots, attempts_blocked, missed_shots,
				hits, give_aways, take_aways, blocked_shots, faceoff_wins,
				faceoff_losses, faceoff_percentage, playerid))

		home_roster = roster

	return away_roster, home_roster


	

if __name__ == '__main__':
	year = '20142015'
	game_num = '0001'
	home, away = harvest(year, game_num)
	for item in home:
		print item