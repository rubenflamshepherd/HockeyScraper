def pad_game_num (game_num):
	game_num = str(game_num)
	if len (game_num) == 4:
		return game_num
	elif len (game_num) == 3:
		return "0" + game_num
	elif len (game_num) == 2:
		return "00" + game_num
	elif len (game_num) == 1:
		return "000" + game_num
	else:
		print "problem with padding game number (Operations.pad_game_num)"