def STORY():
	"""
	This is the 'STORY MODE'.
	The goal is to get to floor 1, beat the behemoth
	and just DON'T DIE. 
	Zork, this was made by Alastar S.
	This game is- free-ware.. Free to distribute,
	but please don't change and say it is your own?
	I will be making changes in the future, just contact
	me for the next versions (until' I stop development).
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
	#from datetime import datetime
	import time
	from time import sleep #To make program wait

	#This is for crediting people (like playtesters)
	# in the Special Thanks section of the credits
	def credit_in_special_thanks(msg):
		print("\t - {}".format(msg))
		sleep(1)

	#This is the player
	user = Player(input("What is your name?: "))

	startTime = time.time() #The start time

	#Makes the room, and sets up stuff for player
	room, user.pos = character_setup()

	#Draws character for first time
	room[user.pos[1]][user.pos[0]] = "@"

	skip = False #Skip movement of AI
	floor = 90 #128 #The floor that the player is on
	#For the final message, says "Damn {number} floors- they were tired"
	starting_floor_number = floor

	change_floor = -1 #Subtract 1

	mobs = {} #This dictionary contains every enemy
	objects = {} #All of the objects (like chests)

	dialog = [] #Stuff to be printed
	exit = False #If the user wants to exit

	mob_number = 0 #Number of mobs

	clear() #Clear screen at start
	print("FLOOR: {}".format(floor)) #Prints floor number
	print("HP: {}".format(user.hp)) #Prints health of player
	print("Hint: press 'h' for help") #Tell user where help is
	draw_room(room) #Draw room at start

	while True: #Keep going until user presses escape
		#For the user moving
		user.pos,room,floor,mobs,objects,dialog,skip,exit,addOnTime = mov_user('story',user,room,floor,user.char,mobs,objects, change_floor, startTime,0)

		#If we are exiting the menu
		if exit == True: break

		#This is the end of the game
		if floor == 0:
			clear()
			end = int((time.time() - startTime)/60)

			print("{} stood upon the body of the mighty beast.".format(user.name))
			sleep(2)
			print("{} looked at the Behemoth- surprised they killed that thing.".format(user.name))
			sleep(3)
			print("{} was really tired. I mean- damn, {} floors.".format(user.name, starting_floor_number))
			sleep(3)
			print("Covered in blood, {} gets off of the beast and walks".format(user.name))
			print("over to the corner of the room. There, a mighty chest lies.")
			sleep(4)
			print("Putting down {} {} pries open the chest.".format(user.inventory['primary'][1], user.name))
			sleep(3)
			print("Inside is a small blue vial containing an unknown fluid.")
			print("The color of the vial's contents slowly changes in hue.")
			sleep(4)
			print("This is why {} came here. For this mysterious vile.".format(user.name))
			print("If {}'s lover was to keep living, they would need this.".format(user.name))
			sleep(4)
			print("{} stuffed the vile into their pocket, and proceeded to the stairs.".format(user.name))
			sleep(3)
			print("It was going to be a long climb up, but it was worth it.")
			sleep(3)
			print("{} left, leaving the Behemoth behind, leaving this place behind.".format(user.name))
			sleep(3)
			print("{} went home.".format(user.name))
			sleep(3)
			print("_____________________________________________________")
			print("_____________________________________________________")
			print("\n\t\t\tThe End.")
			print("\t\t   Play time: {} mins".format(end))
			sleep(3) #Wait for credits
			
			print("\n\n\nPress anything to proceed..")
			pause()
			clear()

			print("CREDITS:")
			print("_____________\n")

			print("Lead advisor: Kieran Slater\n")
			sleep(2)
			print("Co-writer: Jacob Conrad\n")
			sleep(2)
			print("Lead programmer: Alastar's fingers\n")
			sleep(2)

			#Special thanks section
			print("Special thanks to:")
			print("_____________________")
			sleep(1.5)
			#Thank my dad
			credit_in_special_thanks("Dan S. [parental unit], [play tester]")
			#Credit my brother
			credit_in_special_thanks("Kieran S. [play tester], [lead advisor]")
			#Credit Noah T.
			credit_in_special_thanks("Noah T. [play tester]")
			#Thank Susie S.
			credit_in_special_thanks("Susie S. [play tester]")
			#Thank Alex F.
			credit_in_special_thanks("Alex F. [play tester]")
			#Thank Rowan P.
			credit_in_special_thanks("Rowan P. [play tester]")
			#Thank Paris D.
			credit_in_special_thanks("Paris D. [play tester]")
			#Thank Jacob C.
			credit_in_special_thanks("Jacob C. [play tester], [co-writer]")
			#Thank Mark Z.
			credit_in_special_thanks("Mark Z. [play tester]")

			#Wait for next section
			sleep(2)

			print("\nEnd message:")
			print("_____________________")
			sleep(1.5)
			print("\nI hoped you enjoyed! This has been a fun")
			sleep(1.5)
			print("little project of mine (mainly to see if I")
			sleep(1.5)
			print("could even do graphics like this!) and it ")
			sleep(1.5)
			print("has been.. interesting. This is formally")
			sleep(1.5)
			print("'my first game', and it was fun! The making")
			sleep(1.5)
			print("of Rouge-like's is interesting (and I actually")
			sleep(1.5)
			print("think I may make more if my brother pushes")
			sleep(1.5)
			print("me enough for it).")
			sleep(1.5)
			print("Thanks for all of the fish.")
			print("- Alastar")
			sleep(2)

			print("\n\nPress anything to win..")
			pause()
			break #Stop story mode

		#If there are any mobs
		if skip == False and len(mobs) > 0:
			#Go through every mob
			for index in mobs:
				#Gets the movement of the monster
				mov = mov_direction(user.pos, mobs[index].pos, room)
				#Moves monster
				mobs[index].pos,room,floor,mobs,objects,X,Y,skip,W = mov_user('story',mobs[index],room,floor,mobs[index].char,mobs,objects,change_floor,startTime,0,mov)

			#Allow any mobs that can, attack, attack
			user, dialog = enemy_attack(user, dialog, room, mobs)

			#If the user is dead now.
			if user.hp <= 0:
				death_time = int((time.time() - startTime)/60) #Time they died
				clear()
				#The total play-time of the player (in minutes)
				#time_of_death_minutes = abs(death_time.minute - startTime.minute)
				#The total play-time of the player (in hour)
				#time_of_death_hours = abs(death_time.hour - startTime.hour)
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
				pause()
				break #Stop game

		clear() #Clear previous frame of game
		print("FLOOR: {}".format(floor)) #Prints floor number
		print("HP: {}".format(user.hp)) #Prints health of player

		#Print hp of the boss if we are on floor 1
		if floor == 1 and len(mobs)>0: print("BEHEMOTH: {}".format(mobs[0].hp))
		
		draw_room(room) #draw current frame
		draw_dialog(dialog) #Draws response dialog
