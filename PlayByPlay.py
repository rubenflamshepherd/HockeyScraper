import Operations

class Event:

	def __init__ (self, num, per_num, strength, time,event_type, description, away_on_ice, home_on_ice):
		self.num = num
		self.per_num = per_num
		self.strength = strength
		self.time = time
		self.event_type = event_type
		self.description = description
		self.away_on_ice = away_on_ice
		self.home_on_ice = home_on_ice

	def __str__ (self):

		return self.num.encode('utf-8') + ' ' + self.per_num.encode('utf-8') + ' ' + \
		 self.strength.encode('utf-8') + ' ' + self.time.encode('utf-8') + ' ' + \
		 self.event_type.encode('utf-8') + ' ' + self.description.encode('utf-8')

def playbyplay_extractor (year, game_num):
	"""
	Extract play-by-play information from a html file on the
	local machine (in the form of events)
	"""

	tree = Operations.germinate_report_seed(year,game_num,'PL','02')

	events = [] # empty list for holding unspecified events
	
	for item in tree.xpath('//table/tr[@class="evenColor"]'):
	#for x in range (116, 120):
	#   item = tree.xpath('//table/tr[@class="evenColor"]') [x]
					
		event_raw = item.xpath('./td/text()')

		num = unicode(event_raw[0])
		per_num = unicode(event_raw[1])
		strength = unicode(event_raw[2])
		time = unicode(event_raw[3])
		event_type = unicode(event_raw[5])
		description = unicode(event_raw[6])

		# Goals have an additional row in the description cell for assists
		if event_type == 'GOAL' and event_raw[7].find('Assist') != -1:
			description = unicode(" ".join(event_raw[6:8]))

		players_on_ice = item.xpath('./td/table')

		home_on_ice = []
		away_on_ice = []
			
		if len (players_on_ice) == 2:

			away_players_raw = players_on_ice[0].xpath ('.//font')
			for away_player in away_players_raw:
				position_name = away_player.xpath ('./@title')
				number = away_player.xpath ('./text()') [0]

				position, name = position_name[0].split(' - ')

				away_on_ice.append ([position, name, number])
			
			home_players_raw = players_on_ice[1].xpath ('.//font')
			for home_player in home_players_raw:
				position_name = home_player.xpath ('./@title')
				number = home_player.xpath ('./text()') [0]

				position, name = position_name[0].split(' - ')

				home_on_ice.append ([position, name, number])

		event = Event(
			num, per_num, strength, time, event_type, description,\
			away_on_ice, home_on_ice
			)
		
		events.append (event)	    
	return events

if __name__ == '__main__':
	playbyplay_extractor ('20152016', '0003')
