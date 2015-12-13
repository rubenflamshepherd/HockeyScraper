'''
Save online html reports of games to local files
'''
import Operations
from lxml import html, etree
import os
from random import randint
import requests
import time

def grabber (season, start_game, finish_game, game_type):
	'''
	Grabs all resports for games with game numbers between start_game
	and finish_game of game_type in season from nhl.com and stores them in a
	local file
	'''

	destination_path =  "C:/Users/Ruben/Projects/HockeyScraper/Reports/"
	report_types = ["GS", "ES", "FC", "FS", "PL", "TV", "TH", "RO", "SS"]
	not_found_urls = []
	start_time = time.time()
	total_delay = 0.0
	saved_counter = 0
	imported_counter = 0

	# Seeing if season being grabbed has been instantiated and if not, doing so
	season_folders = os.listdir (destination_path)
	
	if season not in season_folders:
		new_season_folder_path = destination_path + season + "/"
		os.mkdir (new_season_folder_path)
		
	# Seeing if game reports have been dowloaded, and doing so if they have not
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
				check = tree.xpath ('//head/title/text()')
				
				if check != ['404 Not Found']:
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

if __name__ == '__main__':
	grabber ('20152016', 1, 20, '02')
