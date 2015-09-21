'''
Save online reports of games to local files
'''


from lxml import html
import sqlite3
import os
import requests
import Operations
import time
from Objects import Event
from random import randint
from dateutil.parser import parse

def grabber (season, start_game, finish_game, game_type):
	'''
	Grabs all resports for games with game numbers between start_game
	and finish_game of game_type in season
	'''

	destination_path =  "C:/Users/Ruben/Projects/HockeyScraper/Reports/"
	report_types = ["GS", "ES", "FC", "FS", "PL", "TV", "TH", "RO", "SS"]
	not_found_urls = []
	start_time = time.time()
	total_delay = 0.0
	saved_counter = 0
	imported_counter = 0

	# Seeing if season being grabbed has been instantaited and if not, doing so
	season_folders = os.listdir (destination_path)
	
	if season not in season_folders:
		new_season_folder_path = destination_path + season + "/"
		os.mkdir (new_season_folder_path)
		
	# Seeing if game reports have been dowloaded, and doing so if they have

	files_path = destination_path + season + "/"
	alreadY_saved_files = os.listdir (files_path)

	for game_num in range (start_game,finish_game):
		game_padded = Operations.pad_game_num (game_num)

		for report_type in report_types:
			file_name = report_type + game_type + game_padded + ".HTM"
			url = "http://www.nhl.com/scores/htmlreports/" + season + "/" + file_name
			
			if file_name in alreadY_saved_files:
				print file_name + " - Already Saved"
				saved_counter += 1
			else:
				report = requests.get(url)
				tree = html.fromstring (report.text)

				if real_report:
					temp_file = open (files_path + file_name, 'w')
					temp_file.write (report.text)
					temp_file.close()
					delay = randint(1,15)/60.0
					total_delay += delay
					time.sleep (delay)
					print file_name + " - Imported - %0.2fs Delay" %delay
					imported_counter += 1
				else:
					not_found_urls.append (url)
					print file_name + " - 404 ERROR, NOT FOUND"

	
	total_time = time.time() - start_time
	print str(imported_counter), " - files imported"
	print str(saved_counter), " - files already saved"
	print str(saved_counter + imported_counter) + " - total files - %0.1f games" %((saved_counter + imported_counter)/9.0)
	print "%0.2fs - total time taken" %total_time
	print "%0.2fs - time taken per file imported" %(total_time/imported_counter)
	print "%0.2fs - time taken per game imported" %(total_time/imported_counter*9)
	print "%0.2fs - time spend in delays - %0.2f percent of total time" %(total_delay, total_delay/total_time*100)
	print "The following reports were not found: "
	for item in not_found_urls:
		print item



def real_report (tree):
	'''
	Checks that a link does not point to a 404 page (not found on server, etc.)
	Returns 'True' is the link has a report, 'False' if it points to a 404 page
	'''
	
	check = tree.xpath('//head/title/text()') [0]
	
	if check == '404 Not Found':
		return False
	else:
		return True


def game_info_scraper (year, game_num):

	file_path = "C:/Users/Ruben/Projects/HockeyScraper/Reports/" + year + "/PL02" + game_num + ".HTM"
	with open (file_path, 'r') as temp_file:
		read_data = temp_file.read()
		
	tree = html.fromstring(read_data)
	
	away_info_raw = tree.xpath('//tr/td[@valign="top"]/table[@id="Visitor"]')[0]
	away_score = away_info_raw.xpath('.//td[@style="font-size: 40px;font-weight:bold"]/text()')[0]
	away_team = away_info_raw.xpath('.//td[@style="font-size: 10px;font-weight:bold"]/text()')[0]
	away_team_game_nums = away_info_raw.xpath('.//td[@style="font-size: 10px;font-weight:bold"]/text()')[1]

	home_info_raw = tree.xpath('//tr/td[@valign="top"]/table[@id="Home"]')[0]
	home_score = home_info_raw.xpath('.//td[@style="font-size: 40px;font-weight:bold"]/text()')[0]
	home_team = home_info_raw.xpath('.//td[@style="font-size: 10px;font-weight:bold"]/text()')[0]
	home_team_game_nums = home_info_raw.xpath('.//td[@style="font-size: 10px;font-weight:bold"]/text()')[1]

	game_info_raw = tree.xpath('//tr/td/table[@id="GameInfo"]')[0]
	game_date = game_info_raw.xpath('.//td[@style="font-size: 10px;font-weight:bold"]/text()')[0]
	attendance_arena = game_info_raw.xpath('.//td[@style="font-size: 10px;font-weight:bold"]/text()')[1]
	game_start_end = game_info_raw.xpath('.//td[@style="font-size: 10px;font-weight:bold"]/text()')[2]
	game_num = game_info_raw.xpath('.//td[@style="font-size: 10px;font-weight:bold"]/text()')[3]
	report_type = game_info_raw.xpath('.//td[@style="font-size: 10px;font-weight:bold"]/text()')[4]
	
	print game_date, attendance_arena, game_start_end, game_num, report_type
	print away_score, away_team, away_team_game_nums
	print home_score, home_team, home_team_game_nums
	

def playbyplay_scraper (year, game_num):
	
	file_path = "C:/Users/Ruben/Projects/HockeyScraper/Reports/" + year + "/PL02" + game_num + ".HTM"
	with open (file_path, 'r') as temp_file:
		read_data = temp_file.read()
	tree = html.fromstring(read_data)

	events = []
	
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
			
	    #print away_on_ice
	    #print home_on_ice

	    event = Event(num, per_num, strength, time, event_type, description, away_on_ice, home_on_ice)
	    #print num , per_num , strength , time, event_type, description
	    
	    events.append (event)	    
	return events
	

if __name__ == '__main__':
	grabber ("20142015", 1, 110, '02')
	# print checker ('http://www.nhl.com/scores/htmlreports/20142015/PL021230.HTM')
	#game_info_scraper ("20142015", "0001")
	'''
	events = playbyplay_scraper ("20142015", "0001")
	for x in range (0,20):
		print events[x]
	'''

