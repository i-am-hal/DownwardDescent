def ENDLESS():
	"""
	This is the ENDLESS mode for Zork.
	The objective for this is to get as much money
	as possible, and to live the longest.
	Your 'score' is effected by your Gold Per Minute, 
	(how much gold you get in a minute) and your play-time.
	"""
	from os import system
	#Important classes
	from tools import Player, Zombie, Chest
	#Important functions
	from tools import character_setup, mov_user, draw_room, clear, mov_direction
	from tools import draw_dialog, enemy_attack, pause
	#For tests
	from tools import user_pos_setup, mk_room, Getch
	#SO we can tell the user how long they played for
	import time
	from time import sleep #To make program wait
	#Converts as much gold that the player has 
	# This will be usedd to calculate high score
	from tools import convert_coin_to_gold
	#Used for encrypting and decrypting the save
	from tools import decrypt_save, encrypt_save

	#This is the player
	user = Player(input("What is your name?: "))

	startTime = time.time() #The start time

	#The number of health potions that they start off with
	user.inventory['health potions'] = 5

	#Makes the room, and sets up stuff for player
	room, user.pos = character_setup()

	#Draws character for first time
	room[user.pos[1]][user.pos[0]] = "@"

	skip = False #Skip movement of AI
	floor = 1 #The floor that the player is on
	change_floor = 1 #Add 1


	mobs = {} #This dictionary contains every enemy
	objects = {} #All of the objects (like chests)

	dialog = [] #Stuff to be printed

	mob_number = 0 #Number of mobs
	exit = False #IF we want to leave
	add_on_time = 0 #The amount of time that we'll add at the very end
	
	clear() #Clear screen at start
	print("FLOOR: {}".format(floor)) #Prints floor number
	print("HP: {}".format(user.hp)) #Prints health of player
	print("Hint: press 'h' for help") #Tell user where help is
	draw_room(room) #Draw room at start

	while True: #Keep going until user presses escape
		#For the user moving
		user.pos,room,floor,mobs,objects,dialog,skip,exit,W = mov_user('endless',user,room,floor,user.char,mobs,objects, change_floor, startTime, add_on_time)

		add_on_time += W #Add on w amount of minutes to total time

		#If we want to exit
		if exit == True: break

		#If there are any mobs
		if skip == False and len(mobs) > 0:
			#Go through every mob
			for index in mobs:
				#Gets the movement of the monster
				mov = mov_direction(user.pos, mobs[index].pos, room)
				#Moves monster
				mobs[index].pos,room,floor,mobs,objects,X,Y,exit,W = mov_user('story',mobs[index],room,floor,mobs[index].char,mobs,objects,change_floor,startTime,add_on_time,mov)

			#Allow any mobs that can, attack, attack
			user, dialog = enemy_attack(user, dialog, room, mobs)

			#If the user is dead now.
			if user.hp <= 0:
				#Time they died (in mins, includes any time from past save)
				death_time = int(((time.time() - startTime)/60)+add_on_time)
				#Converts as much money into gold
				user = convert_coin_to_gold(user)

				#Calculates the user's score
				if death_time > 0 and user.inventory['gold'] > 0:
					high_score = int((user.inventory['gold'] / death_time) + (death_time / 2))
				
				#High score is 0 if death time is 0 and gold is 0
				else: high_score = 0

				clear()
				#Rest in piece <user>
				death_message = "Rest in piece {}".format(user.name)
				#Bumper to center the gravestone
				bumper = (len(death_message)//2-1)*' '

				#Shows death screen
				print(bumper+"  ______")
				print(bumper+" /      \\")
				print(bumper+"|        |")
				print(bumper+"| R.I.P. |")
				print(bumper+"|        |")
				print(bumper+"|________|")
				print(death_message)
				#Prints out play time in hours and minutes
				print(" Play time: {} mins".format(death_time))
				#Shows user their high score
				print(" Score: ", high_score)
				input()
				#Get the information about the highscore
				highScore = open('DownwardDescent_Highscore.txt', 'r').read()
				#Decrypt the information
				highScore = eval(decrypt_save("DownwardDescent", eval(highScore)))

				#If the user's score is greater than the last high score
				if high_score > highScore[1]:
					#Clear out the file
					open('DownwardDescent_Highscore.txt', 'w').close()
					#Tell the player that they've beat the last highscore
					print("\nYou've beat {}'s High Score!".format(highScore[0]))
					print("Please enter a 7 letter name for your highscore!:")
					new_highscore_name = input()[0:7] #Only 7 letters long

					#Record the new high score
					File = open('DownwardDescent_Highscore.txt', 'w')
					#Make the information
					new_high_score_info = "('{}', {})".format(new_highscore_name, high_score)
					#Encrypt the info
					File.write(str(encrypt_save("DownwardDescent", new_high_score_info)))
					File.close()

				break #Exit

		clear() #Clear previous frame of game
		print("FLOOR: {}".format(floor)) #Prints floor number
		print("HP: {}".format(user.hp)) #Prints health of player
		
		draw_room(room) #draw current frame
		draw_dialog(dialog) #Draws response dialog

#ENDLESS() #Runs endless mode