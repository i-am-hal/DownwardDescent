"""
This is the main 'bulk' of the game. It has most of the back-end stuff.
Feel free to browse through to see how I did everything!
Don't 'touch' anything please?
"""

#To randomly generate rooms
from random import randint
from os import system #To talk to the 'system'
from functools import reduce #Reduce list -> single value
from platform import system as get_system #To see what system this is
from time import time
from time import sleep

#Takes the raw information for a save file, and a password and encrypts it w/ password
def encrypt_save(password, info):
	#Make the information into a set of integers
	info = [ord(char) for char in str(info)]
	#Make the password into a set of integers
	password = [ord(char) for char in password]

	#Encrypted information, has to stay as a bunch of numbers
	result = []
	i = 0 #Stupid iterator variable
	for char in info: #Goes through ascii val of a number and encrypts it
		#If we go over the last part of the 'key', loop back to the start of it
		if i == len(password): i = 0
		#Adds that one value part of the key
		char += password[i]
		#then divides by the length, fully scrambling it
		char /= len(password)
		#Add result
		result.append(char)
		#Go onto next part of the key
		i += 1

	#Return the encrypted result
	return result

#Uses the password, and list of numbers (the encrypted information)
# and decrypts it and returns the result
def decrypt_save(password, info):
	#Makes the password into a list of numbers
	password = [ord(char) for char in password]

	#Resulting decrypted stuff
	result = []
	i = 0 #Stupid iterator variable
	for char in info: #Go through every number and decrypt it
		if i == len(password): i = 0 #Loop back to first value in key
		#Multiply by password length to get closer to original number
		char *= len(password)
		#Subtract individual value in key to get back to original value
		char -= password[i]
		#Add the resulting character
		try:
			result.append(chr(int(char)))

		#If an error occurs, then the file hasn't been decoded correctly
		except:
			result.append("_")
		#Move onto next value
		i += 1

	#The decrypted information
	original_info = ""
	for char in result:
		original_info += char

	return original_info #Return original information

#This will take in a password, and checks to see if the password would correctly
# encrypt / decrypt the given information. If it doesn't 'cooperate', then
# we should tell the user to pick a new password
# RETURNS 'TRUE' if password works, 'FALSE' otherwise
def check_password(password):
	#Return false, a password can't be nothing
	if password == "": return False

	#The test information, used to see if the password will work
	test = {'name':"Jimbo", "floor":9271, "time":47,
	'health potions':15, 'mobs':{1:('zombie', (5, 9), 6, 40, 32),
	2:('minotaur', (0, 4), 8, 26, 12), 3:('ker', (7, 2), 6, 5, 99)},
	'objects':{1:('priest', (18, 7))},
	#If this is even one character off, then it won't work
	'final':"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()~`-_=+\\|]}[{'\";:/?.>,<"}
	#Turn it into a string for comparison
	test = str(test)
	#Encrypts, then decrypts the information with the password, this
	# is so we can test to see if this password will work for encryption and decryption
	encoded_decoded_result = decrypt_save(password, encrypt_save(password, test))

	#If the encoded (then decoded) string is exactly the same as
	# the starting information, then this password should work fine
	if test == encoded_decoded_result:
		return True

	#If the password failed in decrypting the info..
	# then tell the user that this can't be used as a password
	return False

#This checks to see if the saves file and highscore file exists.
# if they do, then we're fine, otherwise, make them
def check_highscore_saves():
	#If the saves file doesn't exist, then make it
	try:
		FILE = open('DownwardDescent_Saves.txt', 'r').read()
	except FileNotFoundError:
		FILE = open('DownwardDescent_Saves.txt', 'w')
		FILE.write("{}")
		FILE.close()

	#If the highscore file doesn't exist, then make it
	try:
		FILE = open('DownwardDescent_Highscore.txt', 'r').read()
	except FileNotFoundError:
		FILE = open('DownwardDescent_Highscore.txt', 'w')
		start_highscore = "('none', 0)" #Initial high score
		#Encrypt it
		encrypted_highscore = encrypt_save("DownwardDescent", start_highscore)
		FILE.write(str(encrypted_highscore)) #Write in highscore
		FILE.close()

#Generates random number
rand = lambda MIN, MAX: randint(MIN, MAX)

#The function used to get 1 char input from character
#If the system is windows.. return relevent getch function
def mk_GETCH():
	if get_system() == "Windows":
		from msvcrt import getch
		return (lambda: getch().decode('utf-8'))

	#If the system is instead Linux
	elif get_system() == "Linux":
		import sys, tty, termios
		#The getch function for linux
		def GETCH_FUNCTION():
			fd = sys.stdin.fileno()
			old_settings = termios.tcgetattr(fd)
			try:
				tty.setraw(sys.stdin.fileno())
				ch = sys.stdin.read(1)
			finally:
				termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
			return ch

		return GETCH_FUNCTION

#Gets single character from user (without enter being pressed)
Getch = mk_GETCH()

#Just waits for input from the user
def pause():
	try:
		Getch()
	except:
		pass

#Makes clear function so it works on Linux + Windows
def mk_CLEAR():
	#Use the 'cls' command to clear the screen
	# if the system is Windows
	if get_system() == "Windows":
		return (lambda: system('cls'))

	#Use the 'clear' command to clear the screen
	# if the system is a Linux System
	elif get_system() == "Linux":
		return (lambda: system('clear'))

#Clears the screen
clear = mk_CLEAR()

#'Rolls' a d20 to see if the player (or anything else)
# can get past the armor class of the other thing
d20_roll = lambda: randint(1, 20)

#'Rolls' a d5 (for randomly getting a health potion)
d5_roll = lambda: randint(1, 5)

#Applies a function f to every value in x
map = lambda f, x: [f(y) for y in x]

#For a list of booleans, uses or on all values
Or = lambda lst: reduce(lambda x,y: x or y, lst)

#Makes a room, h and w are Height and Width
def mk_room(h, w):
	new_room = [[]] * h #Make a list of 'h' tall room
	i = 0
	for line in new_room:
		new_room[i] = ['.'] * w #make each room 'w' wide
		i += 1

	#Adds walls + 'celing' and 'floor'
	new_room = [['|']+x+['|'] for x in new_room]
	return [[' ']+['_']*w+[' ']]+new_room+[[' ']+['-']*w+[' ']]

#prints out returned dialog (like if the player missed)
def draw_dialog(lst):
	for line in lst:
		print(line)

#Randomly generates the room
def gen_room():
	#The random height and width of the new room
	height = randint(3, 10)
	width = randint(2, 20)
	#Makes the room
	return mk_room(height, width)

#Gets the middle-most position of the user
user_pos_setup = lambda ROOM: (len(ROOM[0])//2, len(ROOM)//2)

#Sets up the player for the room
def character_setup():
	R = gen_room() #Makes the room
	pos = user_pos_setup(R) #Position of player
	return R, pos

#Draws the new frame of the room
def draw_room(space):
	#Draws room
	for line in space: #Go through every line
		x = "" #The entire line
		for char in line: #Collect the line
			x += char
		print(x) #Print line

#Return's true on if the space above is a ceiling (another wall)
def ceiling_above(obj_pos, space):
		#The tile just above the character
		above_tile = space[obj_pos[1]-1][obj_pos[0]]
		#Immovable objects (includes enemies)
		immovables = ['_', '-', '|', 'Z', 'M', 'K', 'N', 'B', '#', 'S', 'P']

		#If the tile above is not an immovable obejct
		if not above_tile in immovables:
			return False
		return True

#Returns true if a floor/ceiling is below the character
def floor_below(obj_pos, space):
	#The tile below the character
	below_tile = space[obj_pos[1]+1][obj_pos[0]]
	#Immovable objects (includes enemies)
	immovables = ['_', '-', '|', 'Z', 'M', 'K', 'N', 'B', '#', 'S', 'P']

	#Checks if an immovable object is below
	if not below_tile in immovables:
		return False
	return True

#Returns a true if there is a wall to the right of the player
def wall_right(obj_pos, space):
	#The tile to the right of the player
	right_tile = space[obj_pos[1]][obj_pos[0]+1]
	#Immovable objects (includes enemies)
	immovables = ['_', '-', '|', 'Z', 'M', 'K', 'N', 'B', '#', 'S', 'P']

	#Checks if an obstacle is to the right of the player
	if not right_tile in immovables:
		return False
	return True

#Returns true if there is a wall to the left of the player
def wall_left(obj_pos, space):
	#The tile to the left of the user
	left_tile = space[obj_pos[1]][obj_pos[0]-1]
	#Immovable objects (includes enemies)
	immovables = ['_', '-', '|', 'Z', 'M', 'K', 'N', 'B', '#', 'S', 'P']

	#Checks if any wall tile is to the left of the player
	if not left_tile in immovables:
		return False
	return True

#Returns a list of all of the spaces around the player
spaces_around_player = lambda pos: [(pos[0]-1, pos[1]), (pos[0]+1, pos[1]), (pos[0], pos[1]-1), (pos[0], pos[1]+1)]

#This returns the mobs that are in position for
# the player to attack them
def get_enemies_in_attack_area(mobs, player_pos):
	#Gets all of the areas around the player
	areas = spaces_around_player(player_pos)
	mob_list = [] #List of mobs in range

	for mob_index in mobs:
		#Gets the version of the mob
		current_mob = mobs[mob_index]

		#If the mob's position is any of the areas around the player
		# then we should keep track of the index of the mob (etc).
		if current_mob.pos in areas:
			mob_list.append((mob_index, current_mob))

	#Now return those values- of the index- of the monsters around them
	return mob_list

#Gives a list of all of the chests around the player
def chests_in_area(objs, player_pos):
	#Get all of the areas around the player
	areas = spaces_around_player(player_pos)
	chest_list = [] #Get all of the chests around player

	for chest_index in objs:

		#If the chest is in one of the areas
		# around the player
		if objs[chest_index].pos in areas:
			chest_list.append((chest_index, objs[chest_index]))

	return chest_list

#Prints saves a correct sentence for what has been saved
def gained_coin(name, gold, silver, bronze):
	#If all of the values are equal to 0
	if gold == silver == bronze == 0:
		return "{} gained nothing.".format(name)

	#If there is only gold
	elif gold > 0 and silver == bronze == 0:
		return "{} gained {} gold!".format(name, gold)

	#If there is only silver
	elif silver > 0 and gold == bronze == 0:
		return "{} gained {} silver!".format(name, silver)

	#If there is only bronze
	elif bronze > 0 and gold == silver == 0:
		return "{} gained {} bronze!".format(name, bronze)

	#If there is only gold and silver
	elif gold > 0 and silver > 0 and bronze == 0:
		return "{} gained {} gold and {} silver!".format(name, gold, silver)

	#if there is only gold and bronze
	elif gold > 0 and bronze > 0 and silver == 0:
		return "{} gained {} gold and {} bronze!".format(name, gold, bronze)

	#If there is only bronze and silver
	elif bronze > 0 and silver > 0 and gold == 0:
		return "{} gained {} silver and {} bronze!".format(name, silver, bronze)

	#If there is gold, silver and bronze
	elif gold > 0 and silver > 0 and bronze > 0:
		return "{} gained {} gold, {} silver, and {} bronze!".format(name, gold, silver, bronze)

#This is the gui for the bag selection in the inventory
# It shows all of the weapons / armor that the user
# has in their bag, as well as which one is selected
def inventory_bag_gui(obj, selection):
	bag = obj.inventory['bag'] #Get the bag
	len_index = lambda i, d: len(d[i]) #Returns length of value in that index of d
	
	bag_print = {}
	#Go through and make a string corresponding
	# to what will be printed out of those items
	for index in bag: bag_print[index]="| {}: {} ({})".format(index, bag[index], (lambda i,v: '*' if i==v else '')(index, selection))

	hang_int = 0 #Used for the number of underscores we need
	#Add up the lengths for all items
	for index in bag: hang_int += len_index(index, bag_print)
	hang_int = (hang_int // 6) + 10 #Finish off the average, and add 10
	#The string of underscores that is 'hang_int' long
	hangover = "_" * int(hang_int)

	print(" "+hangover)
	print("| INVENTORY | BAG: ")
	print("|"+hangover)
	print("| ESC - Exit bag")
	print("| W / S - Move through items")
	print("| D - Destroy item")
	print("| Enter - Pick item\n|")
	#Show the user the armor that they have on currently
	print("| Equipped armor:")
	print("|  {} (mod: {})".format(obj.inventory['armor'][1], obj.inventory['armor'][0]))
	#Show the user the weapon they are using currently
	print("| Equipped weapon:")
	print("|  {} (mod: {})\n|".format(obj.inventory['primary'][1], obj.inventory['primary'][0]))
	#Go through and print every item, show which one is picked
	for index in bag: print(bag_print[index])
	print("|"+hangover)

#Lets user manage things in their bag, i.e
# put armor / weapons into the bag, or equip stuff
# that is in the bag.
def inventory_bag(obj):
	#a list of all armor
	armors_list = [
		'Chain mail', 'Leather armor',
		'Plate mail', 'Mystic armor',
		'Cursed armor', 'Useless armor',
		'Paper armor', 'Super cursed armor',
		'Armor of nonexistence', 'Bare-flesh armor', 
		'Scale mail', "Richard's Mask"
		]
	#A list of all of the weapons
	weapons_list = [
		'Knife', 'Short sword',
		'Blade of honor', 'Blade of the warrior',
		'Excaliber', 'Cursed knife',
		'Useless knife', 'Healer of the enemy',
		'Toothpick',
		'Super toothpick', 
		'Kitchen knife', 'Sacrificial dagger',
		'Scimitar', 'Sledgehammer', 
		'Excalilame', "Richard's Bat"
		]

	key_press = "" #Keypress option of the player
	selected_item = 1 #The item selected to equip

	while key_press != "\x1b": #While the key isn't escape
		clear() #Clear screen
		#Print the gui, show what item is selected
		inventory_bag_gui(obj, selected_item)

		try:
			key_press = Getch()
		except:
			key_press = "" #So we don't blow up

		#Exit out of the bag part of the inventory
		if key_press == "\x1b":
			break

		#If their key-press is to move up / down through bag items 
		elif key_press.lower() == "w" or key_press.lower() == "s":
			#If the user wants to move up one item for selection
			if key_press.lower() == "w" and selected_item > 1:
				selected_item -= 1 #Sub 1 from selection variable

			#If the user wants to move down one item for selection 
			elif key_press.lower() == "s" and selected_item < 6:
				selected_item += 1 #Add 1 to selected variable

		#If the user made their selection..
		elif key_press == "\r":

			#If the item that they have selected is 'None'..
			# ask if the user wants to equip it as armor or as a weapon
			if obj.inventory['bag'][selected_item][1] == "None":
				print(" ____________________________________________")
				print("| Do you want to remove your Armor or Weapon?")
				print("|\n| A - Remove armor \n| W - Remove weapon\n| C - Cancel")
				print("|____________________________________________")

				#This is so we can check if they either want to remove
				# their armor, remove their weapon, or to cancel
				answers_we_will_accept = ['a', 'w', 'c']

				query_answer = "" #The answer of the user
				#Keep getting input for their answer until we have an
				# acceptable answer that we can actually use
				while not query_answer.lower() in answers_we_will_accept:
					try:
						query_answer = Getch()
					except:
						query_answer = "" #Set it to nothing so we don't explode

				#If they want to cancel, and didn't want this, stop this
				if query_answer.lower() == "c":
					pass

				#If they want to remove their armor, let them.
				elif query_answer.lower() == "a":
					#Put their armor into their bag, in the given position
					obj.inventory['bag'][selected_item] = obj.inventory['armor']
					#Remove the user's armor
					obj.inventory['armor'] = (0, 'None')

				#If the user wants to remove their weapon, let them
				elif query_answer.lower() == "w":
					#Stores the user's weapon into the spot in their bag
					obj.inventory['bag'][selected_item] = obj.inventory['primary']
					#Remove the user's weapon
					obj.inventory['primary'] = (0, 'None')

			#If the thing that they are selecting is a weapon, then
			# switch out the user's weapon, with the weapon in that bag slot
			elif obj.inventory['bag'][selected_item][1] in weapons_list:
				#The weapon of the user
				users_weapon = obj.inventory['primary']
				#Give the user the weapon in their bag
				obj.inventory['primary'] = obj.inventory['bag'][selected_item]
				#Put the user's previous weapon in the bag slot
				obj.inventory['bag'][selected_item] = users_weapon

			#If the thing that they (the user) is selecting armor,
			# switch the armor that is equipped for the selected armor
			elif obj.inventory['bag'][selected_item][1] in armors_list:
				#The armor of the user
				users_armor = obj.inventory['armor']
				#Give the user the armor they selected 
				obj.inventory['armor'] = obj.inventory['bag'][selected_item]
				#Put the user's armor into the bag slot that they pulled from
				obj.inventory['bag'][selected_item] = users_armor

		#If the user wants to destroy the selected item
		elif key_press.lower() == "d":
			answers = ['y', 'n'] #Answers we accept
			users_answer = ""

			print(" ____________________________________________")
			print("| Are you sure you want to destroy this item?\n|")
			print("|             Y - yes | N - No")
			print("|____________________________________________")

			#While the user doesn't give us an answer we allow
			while not users_answer.lower() in answers:
				try:
					users_answer = Getch()
				except:
					users_answer = "" #So we don't explode

			#If the user doesn't want to destroy the item
			if users_answer.lower() == "n":
				pass

			#If the user does want to destroy the item
			elif users_answer.lower() == "y":
				#remove the item
				obj.inventory['bag'][selected_item] = (0, 'None')

	return obj #Return object

#The inventory gui-thingy
def inventory(obj):
	option = "" #Character option

	#keep going until 'escape'
	while option != "\x1b":
		#Gets the number of gold
		GOLD = obj.inventory['gold']
		#Gets silver
		SILVER = obj.inventory['silver']
		#Gets bronze
		BRONZE = obj.inventory['bronze']
		#Armor class
		Armor_Class = obj.armor_class
		#Armor class with Armor 
		AC_with_armor = obj.armor_class + obj.inventory['armor'][0]
		#Weapon name
		weapon_name = obj.inventory['primary'][1]
		#Weapon damadge
		weapon_dmg = obj.inventory['primary'][0]
		#Health potions
		health_potions = obj.inventory['health potions'] 

		clear() #Clear screen
		print(" _____________________________________")
		print("| INVENTORY:")
		print("|_____________________________________")
		print("| ESC - Exit Inventory\n| E - Look through bag\n| F - Use health potion\n|")
		#Give player name
		print("| Player: {}".format(obj.name))
		#Print player health
		print("| Health: {}".format(obj.hp))
		#Prints out the gold, silver and bronze
		print("| Gold: {}\n| Silver: {}\n| Bronze: {}".format(GOLD, SILVER, BRONZE))
		#Prints the weapon name, and damadge it deals
		print("| Weapon: {} (modifier: {})".format(weapon_name, weapon_dmg))
		#Shows to the user the armor that they have on
		print("| Armor: {} (modifier: {})".format(obj.inventory['armor'][1], obj.inventory['armor'][0]))
		#Prints out the armor class (and armor class w/ armor)
		print("| Armor class: {} (with armor {})".format(Armor_Class, AC_with_armor))
		#Shows how many potions that the player has
		print("| Health potions: {}".format(health_potions))
		print("|_____________________________________")

		#In case the input was unable to be used (arrow keys)
		try:
			option = Getch()
		except:
			option = "\x1b"

		#If a potion is being used
		if option.lower() == "f" and health_potions > 0:
			#If the hp + 5 is exactly 100
			if obj.hp + 5 < 100:
				#Add 5 hp to the player
				obj.hp += 5			
				#Subtraacts 1 from the number of potions
				obj.inventory['health potions'] -= 1

			#If exactly 100
			elif obj.hp + 5 == 100:
				obj.hp += 1
				obj.inventory['health potions'] -= 1

			#Make the hp equal exactly 100
			elif obj.hp + 5 > 100 and obj.hp < 100:
				obj.hp = 100				
				#Subtraacts 1 from the number of potions
				obj.inventory['health potions'] -= 1

		#If the user wants to go through their bag
		elif option.lower() == "e":
			#Enter the bag interface
			obj = inventory_bag(obj)

	#make sure changes to object are saved
	return obj

#Generates a number of potions for chests
def gen_potions():
	#The number of potions
	n = randint(-3, 5)

	#If n is <= 0, we'll have 0 potions
	if n <= 0:
		return 0
	#Return n, as the number of potions
	else:
		return n

#Selects a piece of armor that will be returned
def pick_armor():
	#THe armor that we will return
	armor = {
		0:(2, 	'Chain mail'), 1:(4, 	'Leather armor'),
		2:(7, 'Plate mail'), 3:(9, 'Mystic armor'),
		4:(rand(-5, -1), 'Cursed armor'), 5:(0.5,	'Useless armor'),
		6:(1, 'Paper armor'), 7:(rand(-10*10**5, -1), 'Super cursed armor'),
		8:(0, 'Armor of nonexistence'), 9:(-10, 'Bare-flesh armor'),
		10:(0, 'None'), 11:(8, 'Scale mail'), 12:(0, 'None'), 13:(0, 'None'),
		14:(0, 'None'), 15:(0, 'None')
		}.get(randint(0, 15))
	return armor

#Selects a weapon randomly and returns it
def pick_weapon():
	#Pick out a weapon to return
	weapon = {
		0:(2, 'Knife'), 1:(5, 'Short sword'),
		2:(8, 'Blade of honor'), 3:(10, 'Blade of the warrior'),
		4:(16, 'Excaliber'), 5:(rand(-5,-1), 'Cursed knife'),
		6:(0.5, 'Useless knife'), 7:(rand(-10*10**5,-1), 'Healer of the enemy'),
		8:(0.01, 'Toothpick'), 9:(0, 'None'), 10:(0, 'None'), 11:(0, 'None'),
		12:(0, 'None'), 13:(0, 'None'), 14:(0.1, 'Super toothpick'), 
		15:(3, 'Kitchen knife'), 16:(7, 'Sacrificial dagger'),
		17:(7, 'Scimitar'), 18:(12, 'Sledgehammer'), 
		19:(rand(0, 13), 'Excalilame')
	}.get(rand(0,19))
	return weapon

#This is the class of every chest instance
class Chest:
	def __init__(self):
		#Position of chest
		self.pos = (0,0)
		#Character that represents this object
		self.char = "#"
		#Index of this chest
		self.index = 0
		#The random number of health potions contained
		self.health_potions = gen_potions()
		#Generates a random amount of coins
		# that will be stored in the chest
		self.coins = {
			'gold':rand(0, 10), #Number of gold
			'silver':rand(0, 15), #Number of silver
			'bronze':rand(0, 20) #Number of bronze
		}
		#Randomly generates an amount of potions
		self.hp_potions = rand(0, 5)
		#The armor contained in the chest
		self.armor = pick_armor()
		#Primary weapons
		self.weapon = pick_weapon()

		#If there is mystic armor, and the weapon is Excaliber,
		# then re-pick the weapon, so that there isn't Excaliber
		if self.armor[1]=="Mystic armor" and self.weapon[1]=="Excaliber":
			self.weapon = {
			0:(2, 'Knife'), 1:(5, 'Short sword'),
			2:(8, 'Blade of honor'), 3:(10, 'Blade of the warrior'),
			4:(rand(-5,-1), 'Cursed knife'),
			5:(0.5, 'Useless knife'), 6:(rand(-10*10**5,-1), 'Healer of the enemy'),
			7:(0.01, 'Toothpick'), 8:(0, 'None'), 9:(0, 'None'), 10:(0, 'None'),
			11:(0, 'None'), 12:(0, 'None'), 13:(0.1, 'Super toothpick'), 
			14:(3, 'Kitchen knife'), 15:(7, 'Sacrificial dagger'),
			16:(7, 'Scimitar'), 17:(12, 'Sledgehammer'), 
			18:(rand(0, 13), 'Excalilame')
			}.get(rand(0,18))

		#If the roll to get "Richard's Mask" is 1, then
		# see if this chest spawns "Richard's Mask"
		if self.armor[1]=="Mystic armor" and randint(1, 100)==1:
			#Okay, so if 42 is 'rolled' out of 0 -> 1 (50-50 chance)
			# then that means that the user get's "Richard's Mask"
			self.armor = {1:(10, "Richard's Mask")}.get(rand(0,1), self.armor)

		#If the roll to get "Richard's Bat" is 1,
		# then see if this chest spawns "Richard's Bat"
		elif self.weapon[1]=="Excaliber" and randint(1,100)==1:
			#If 42 is rolled randomly from 0 -> 1 (50-50 chance)
			# then the player gets "Richard's Bat", otherwise, just Excaliber
			self.weapon = {1:(10, "Richard's Bat")}.get(rand(0,1),self.weapon)

	#This will 'open' the chest, allowing
	# the player to take any coins, potions,
	# or to put on some armor
	def open_chest(self, obj):
		#The option for this chest
		option = ""

		msg_list = [] #List of messages to user
		#Keeping going until escape is pressed
		while option != "\x1b":
			#Prepare statement for the armor owned
			owned_armor = "| Contained Armor: {} (modifier: {})".format(self.armor[1], self.armor[0])

			clear()
			#These are the label thing
			print(" "+('_'*len(owned_armor)))
			print("| CHEST {}".format(self.index + 1))
			print("|"+('_'*len(owned_armor)))
			#Give the options to the players
			print("| ESC - Stop looting chest\n| F - Take potions")
			print("| E - Take coins\n| R - Equip armor\n| C - Equip weapon")
			print("| B - Put weapon / armor in bag\n| ")
			#Prints the name of weapon and damage
			print("| Weapon: {} (modifier: {})".format(self.weapon[1], self.weapon[0]))
			#Shows to the player the armor 
			print(owned_armor)
			#Shows the amount of health potions contained
			print("| Health potions: {}".format(self.hp_potions))
			#Shows all of the GOLD, SILVER and BRONZE
			print("| Coins:")
			print("|    Gold: {}".format(self.coins['gold']))
			print("|    Silver: {}".format(self.coins['silver']))
			print("|    Bronze: {}".format(self.coins['bronze']))
			print("|"+('_'*len(owned_armor)))
			#Print out message
			for msg in msg_list: print(msg)

			#Make sure that the user doesn't fuck up
			try:
				option = Getch()
			except:
				option = ""

			#Gets all of the coins
			GOLD = self.coins['gold']
			SILVER = self.coins['silver']
			BRONZE = self.coins['bronze']

			#Give the player all of the coins
			if option.lower() == "e":
				#Give the player all of the gold coins
				obj.inventory['gold'] += self.coins['gold']
				#Give the player all of the silver coins
				obj.inventory['silver'] += self.coins['silver']
				#Give the player all of the bronze coins
				obj.inventory['bronze'] += self.coins['bronze']

				#Make all of the coins equal 0
				self.coins['gold']=0
				self.coins['silver']=0
				self.coins['bronze']=0

			#Give the player all of the potions
			elif option.lower() == "f":
				#Give the player all of the health potions
				obj.inventory['health potions'] += self.hp_potions

				#Set the number of potions to 0
				self.hp_potions = 0

			#Equip armor onto player
			elif option.lower() == "r":
				#Switches the chest's armor and the player's armor
				self.armor, obj.inventory['armor'] = obj.inventory['armor'], self.armor

			#Give player the weapon
			elif option.lower() == "c":
				self.weapon, obj.inventory['primary'] = obj.inventory['primary'], self.weapon

			#If the option is to put the contained armor / weapon into bag
			elif option.lower() == "b":
				#Asks user if they want to try to put the armor or weapon
				# into their inventory
				print(" ________________________________________________________")
				print("| Would you like to put the armor or weapon in your bag?\n|")
				print("|                 A - Armor | W - Weapon")
				print("|________________________________________________________")

				#Answers acceptable in this instance
				acceptable_answers = ['a', 'w']
				user_input = "" #Response from user
				#While the response isn't something we 'like'
				while not user_input.lower() in acceptable_answers:
					try:
						user_input = Getch()
					except:
						#So we don't explode
						user_input = ""

				#Get the bag slots that are empty
				empty_bag_slots = [index for index in obj.inventory['bag'] if obj.inventory['bag'][index][1] == "None"]

				#Attempts to put the armor into an empty inventory slot
				if user_input.lower() == "a":
					#If there are empty bag slots
					if len(empty_bag_slots) > 0:
						#Puts the armor in the smallest unused bag slot
						obj.inventory['bag'][sorted(empty_bag_slots)[0]] = self.armor
						self.armor = (0, 'None') #Remove armor from chest

					#If there are no empty slots
					elif len(empty_bag_slots) == 0:
						msg_list.append("Sorry, your inventory is full.")

				#Attempts to put hte weapon into an empty inventory slot
				elif user_input.lower() == "w":
					#If there are empty bag slots to use
					if len(empty_bag_slots) > 0:
						#Puts weapon into the smallest unused bag slot
						obj.inventory['bag'][sorted(empty_bag_slots)[0]] = self.weapon
						self.weapon = (0, 'None') #Remove weapon from chest

					#If there are no empty slots in the bag
					elif len(empty_bag_slots) == 0:
						msg_list.append("Apologies, your inventory is full.")

		#Return the object
		return obj

#Generates a name out of random symbols and letters
def gen_gibberish_name():
	#The length of the name
	length = randint(3, 7)
	#All acceptable names
	chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789?><~?!@#$%^&"
	name = "" #Returned name
	while length > 0:
		#Add a random character
		name += chars[rand(0, len(chars)-1)]
		length -= 1 #Decrease number of characters
	return name

#Takes all of the coins in the player's possestion, 
# and converts as much as possible into gold
# 100 bronze = 1 silver
# 100 silver = 1 gold
def convert_coin_to_gold(obj):
	#Number of gold coins
	GOLD = obj.inventory['gold']
	#Number of silver coins
	SILVER = obj.inventory['silver']
	#Number of bronze coins
	BRONZE = obj.inventory['bronze']

	#If the silver and bronze is 0
	# (stop so we don't get an error)
	if SILVER == BRONZE == 0: 
		return obj #Prematurely stop

	#           Adds new silver to total silver | The remaining bronze
	SILVER, BRONZE = SILVER + int(BRONZE / 100), BRONZE % 100
	#          Adds new gold to total gold | The remaining silver
	GOLD, SILVER = GOLD + int(SILVER / 100), SILVER % 100
	#Now give the user the total number of gold
	obj.inventory['gold'] = GOLD
	#Now give the user the remaining silver
	obj.inventory['silver'] = SILVER
	#Now give the user the reamining bronze
	obj.inventory['bronze'] = BRONZE

	return obj #Now return the object

#This will tell the user if there is any sort of change 
# the the amount of currency that they have
def show_convert(obj):
	#Gets the gold and silver before the transaction
	before_silver, before_gold = obj.inventory['silver'], obj.inventory['gold'] 
	#Converts currency
	obj = convert_coin_to_gold(obj)
	#Gets the amount of silver and gold after transaction
	after_silver, after_gold = obj.inventory['silver'], obj.inventory['gold']

	#IF the amount of gold and silver isn't the same, then tell the user
	# how much silver was converted into gold
	if before_silver != after_silver and before_gold != after_gold:
		print("{} silver was converted into {} gold pieces!".format((after_gold - before_gold)*100, after_gold - before_gold))
		pause()

	return obj

#This method is for buying things from the shop-keep 
def buy_func(name, sold_armor, sold_weapon, hp_price, weapon, weapon_price, armor, armor_price, obj):
	#Gonna have the gui be simular to the shop entry
	buy_list = [
		#Show the price of health potions
		'| Health potions: {} gold (per potion)'.format(hp_price),
		#Show the name and modifier of the armor
		'| Armor: Name: {}, Mod: {} ({} gold)'.format(armor[1], armor[0], armor_price),
		#Show the name and modifier of the armor
		'| Weapon: Name: {}, Mod: {} ({} gold)'.format(weapon[1], weapon[0], weapon_price)
	]
	select = 0 #Selected item to buy
	choice = "" #The character option
	log = [] #Log feedback
	while True:
		clear() #Clear the screen
		#The thing for hte top and bottom border
		len_bottom = '_'*(len(buy_list[1])+int(len(buy_list[2])//2))

		#GUI THINGY for the shop
		print(' '+len_bottom)
		print('| SHOP | BUY SECTION')
		print('|'+len_bottom)
		print('| ESC - Exit shop (buying section)')
		print('| W / S - Go through options')
		print('| Enter - Make purchase\n|')
		#Shows the user their gold
		print("| Your Gold: {}".format(obj.inventory['gold']))
		x = 0 #Index
		for item in buy_list:
			show_select = lambda index, sel: '*' if index==sel else ''
			#Prints out items and shows which one is selected
			print(item + " ({})".format(show_select(x, select)))
			x += 1 #Move onto next 
		print("|"+len_bottom)
		#Prints out all of the messages to the user
		for msg in log: print(msg)
		log = [] #Clear out the log list

		try:
			choice = Getch()
		except UnicodeDecodeError:
			#In the case that the value can't be used
			choice = ""

		#If the user is done with the shop (BUY SELECTION)
		if choice == "\x1b": break

		#If the choice is to go up / down through options
		elif choice == "w" or choice == "s":
			#If we are to move up in options, subtract 1 from select
			if choice == "w" and select > 0:
				select -= 1

			#If we are to move down in options, add 1 from select
			elif choice == "s" and select < 2:
				select += 1

		#If the user made a select choice
		elif choice == "\r":
			#If the user is buying potions
			if select == 0:
				#If the user has enough gold to buy a potion, give user one
				if obj.inventory['gold'] >= hp_price:
					#Give the user an additional potion
					obj.inventory['health potions'] += 1
					#Subtracts the payment amount from the gold the user has
					obj.inventory['gold'] -= hp_price
					#Give the user feedback, a 'thank you' for using money
					log.append("{}: Thank you for your business!".format(name))
				
				#If the user doesn't have enough money
				else:
					#Tell the user that they don't have enough money
					log.append("{}: I'm sorry, you don't have enough money.".format(name))

			#If the user is trying to buy the armor, and it hasn't been bought
			elif select == 1:
				#If the armor has been sold, tell the user 
				if sold_armor == True:
					log.append("{}: I'm sorry, you already bought this item.".format(name))

				#If the user can buy the armor, store it in their bag
				elif obj.inventory['gold'] >= armor_price and sold_armor==False:
					#Spaces that are not occupied
					unusable_spaces = [index for index in obj.inventory['bag'] if obj.inventory['bag'][index][1] == "None"]

					#If there are spaces that can be used
					if len(unusable_spaces) > 0:
						#Sort from smallest to largest index that is unused
						unusable_spaces = sorted(unusable_spaces)
						#Store the armor away into the user's inventory
						obj.inventory['bag'][unusable_spaces[0]] = armor
						sold_armor = True #The armor has now been used
						armor = (0, 'None') #Set the armor to nothing
						#Subtract the price of the armor from the user's things
						obj.inventory['gold'] -= armor_price

					else:
						#Ask the user if they want to put on their armor, and remove their current armor
						print("{}: You do not have space in your bag for this item.".format(name))
						print("{}: If you like, I can take your armor, and you can put on your new armor.".format(name))
						print("{}: But.. you can't take back your old armor, just so you know.")
						print("{}: Does that sound good though?\n")
						print(" __________________ ")
						print("| Y - yes | N - No")
						print("|__________________")

						#The answers that are accepted by us
						answers_we_accept = ['y', 'n']
						answer = "" #Answer from the user 
						#While they don't give us a response we can use
						while not answer.lower() in answers_we_accept:
							try:
								answer = Getch()
							except:
								#Stop error
								answer = ""

						#If the user is fine with this
						if answer.lower() == "y":
							#Give the user their new armor
							obj.inventory['armor'] = armor
							#Take away the amount of coin that is the price
							obj.inventory['gold'] -= armor_price
							armor = (0, 'None') #Remove armor from merchant
							sold_armor = True #Make sure that they can't buy nothing

				#Alert the player that they do not have enough funds
				elif obj.inventory['gold'] < armor_price and sold_armor==False:
					log.append("{}: You do not have enough to buy this item.".format(name))

			#If the user is trying to buy the weapon, and it hasn't been bought
			elif select == 2:
				#Tell the user that they cannot buy this item
				if sold_weapon == True:
					log.append("{}: I'm sorry, but you have already bought this item.".format(name))

				#If the user has enough gold to buy the weapon, and it hasn't been sold
				elif obj.inventory['gold'] >= weapon_price and sold_weapon == False:
					#Spaces that are not occupied
					unusable_spaces = [index for index in obj.inventory['bag'] if obj.inventory['bag'][index][1] == "None"]

					#If there are spaces that can be used
					if len(unusable_spaces) > 0:
						#Sort from smallest to largest index that is unused
						unusable_spaces = sorted(unusable_spaces)
						#Store the weapon away into the user's inventory
						obj.inventory['bag'][unusable_spaces[0]] = weapon
						sold_weapon = True #The weapon has now been used
						weapon = (0, 'None') #Set the weapon to nothing
						#Subtract the price of the armor from the user's things
						obj.inventory['gold'] -= weapon_price

					else:
						#Ask the user if they want to put on their armor, and remove their current armor
						print("{}: You do not have space in your bag for this item.".format(name))
						print("{}: If you like, I can take your weapon, and you can equip your new weapon.".format(name))
						print("{}: But.. you can't take back your old weapon, just so you know.")
						print("{}: Does that sound good though?\n")
						print(" __________________ ")
						print("| Y - yes | N - No")
						print("|__________________")

						#The answers that are accepted by us
						answers_we_accept = ['y', 'n']
						answer = "" #Answer from the user 
						#While they don't give us a response we can use
						while not answer.lower() in answers_we_accept:
							try:
								answer = Getch()
							except:
								#Stop error
								answer = ""

						#If the user is fine with this
						if answer.lower() == "y":
							#Give the user their new weapon
							obj.inventory['primary'] = weapon
							#Take away the amount of coin that is the price
							obj.inventory['gold'] -= weapon_price
							weapon_price = 0 #Reset price to 0
							weapon = (0, 'None') #Remove weapon from merchant
							sold_weapon = True #Make sure that they can't buy nothing

				else:
					log.append("{}: Sorry, you don't have enough for this item.".format(name))

	return sold_armor, sold_weapon, weapon, armor, obj

#The gui for selling stuff from the users 
# there is an option to sell everything in the bag at once
def sell_stuff_from_bag(obj, merchant_name):
	bag = obj.inventory['bag'] #Gets the items in the bag
	msg_log = [] #Msg list between merchant and player
	selection = 1 #To tell what's selected
	user_input = "" #Chatacter input from user
	while user_input != "\x1b": #While the user doesn't press escape
		bag_item = [] #Things to be printed
		x = 0 #Throw away variable
		for index in bag:
			#The string that will be shown to the user
			bag_item.append("| {}: {} (mod: {})".format(x+1, bag[index][1], bag[index][0]))
			x += 1

		sum_of_value_lengths = 0 #Will be the sum of all item lengths
		for value in bag_item: #Go through every index in the bag
			sum_of_value_lengths += len(value)//2
		#The underscore character so it makes the gui look nice
		hangover = "_" * (int(sum_of_value_lengths/6) + 27)

		clear() #Clear the screen
		print(" "+hangover)
		print("| SHOP | SELL")
		print("|"+hangover)
		print("| W / S - Move up/down through items")
		print("| E - Sell everything")
		print("| enter - Make selection\n|")
		x = 1 #Throw away variable
		for item in bag_item: #Show selection
			#Print it out and show what's selected
			print(item + ' (' + (lambda i, v: '*)' if i==v else ')')(selection, x))
			x += 1 #Next item
		print("|"+hangover)
		#Print all messages from the merchant in the msg log
		for msg in msg_log: print(msg)
		msg_log = [] #Clear msg list

		#Get input from user
		try:
			user_input = Getch()
		except:
			#Keep program from exploding
			user_input = ""

		#If the user is trying to go up / down through options
		if user_input.lower() == "w" or user_input.lower() == "s":
			#If the selection being made is to go up, and they can go up.. let them
			if user_input.lower() == "w" and selection > 1:
				selection -= 1 #Subtract one to go up

			#If the user wants to go down through selection, and they can, let them
			elif user_input.lower() == "s" and selection < 6:
				selection += 1 #Add one to go down

		#IF the user is selecting a value to sell to the mechant
		elif user_input == "\r":
			#If the name of the armor / weapon is NOTHING..
			# obviously don't let the user sell NOTHING.
			if bag[selection][1] == "None":
				msg_log.append("{}: Don't sell me nothing, cheap-skate.".format(merchant_name))

			#Let the user sell that item
			else:
				ADD_SILVER = randint(10, 50) #Random number of silver coins from 10 -> 50
				#Tell the user how much silver they got
				msg_log.append("{}: Here's {} silver for that.".format(merchant_name, ADD_SILVER))
				obj.inventory['silver'] += ADD_SILVER #give the user the silver
				#Remove that item from the user
				obj.inventory['bag'][selection] = (0, 'None')
				bag = obj.inventory['bag'] #remake the bag variable (keep it up to date)
		
		#If the user wants to sell everything in their inventory
		elif user_input.lower() == "e":
			#Make sure that the user is serious 
			print(" ____________________________________________")
			print("|  Are you sure you want to sell everything?\n|")
			print("|             Y - Yes | N - No")
			print("|____________________________________________")

			#Answers we will accept
			acceptable_answers = ['y', 'n']
			make_sure_answer = "" #Answer from the user
			#While the user's input isn't an answer we accept
			while not make_sure_answer.lower() in acceptable_answers:
				try:
					make_sure_answer = Getch()
				except:
					#Keep from exploding
					make_sure_answer = ""

			#If the user IS sure of themselves on wanting to sell everything
			if make_sure_answer.lower() == "y":
				#Only use the indexes that are not NOTHING
				bag_indexes = [index for index in bag if bag[index][1] != "None"]

				#If there is stuff to sell, sell it
				if len(bag_indexes) > 0:
					ADD_SILVER = 0
					#Go through every item in the bag and pay the user
					# a random amount of silver for each thing
					for index in bag_indexes:
						#Add onto the silver
						ADD_SILVER += randint(10, 50)

					#Remove every item in the users inventory
					for index in bag_indexes: obj.inventory['bag'][index] = (0, 'None')
					#update bag variable
					bag = obj.inventory['bag']
					#Give the user the silver they aquired from selling their things
					obj.inventory['silver'] += ADD_SILVER
					#Tell the user how much silver they got
					msg_log.append("{}: Here's {} silver for your things.".format(merchant_name, ADD_SILVER))

				#Tell the user that they can't sell NOTHING
				else:
					msg_log.append("{}: Don't sell me nothing, cheap-skate.".format(merchant_name))

	return obj

#This is the class of every vender instance
class Vendor:
	def __init__(self):
		#Name of this instance
		self.name = {
			0:'Vincent',
			1:'Jacob',
			2:'Jamie',
			3:'Richard',
			4:'Dominic',
			5:'<NULL>',   #Joke name based on programming
			6:'Carlos',
			7:gen_gibberish_name(), #Totally random name
			8:gen_gibberish_name(), #Totally random name
			9:"Hal",    #Easter-egg, joke name
			10:gen_gibberish_name() #Totally random name
		}.get(rand(0, 10)) #Randomly pick a name
		self.pos = (0, 0) #Position of instance
		self.char = "S" #Symbol to represent Vendor
		#The things this person sells.
		#(<name>, value in gold pieces)
		self.wares = {
			#Hp potions,     cost of a potion
			'Health potions':randint(5, 15),
			#[<Armor>, <price>]
			'Armor':[pick_armor(), randint(10, 25)],
			#[<Weapon>, <price>]
			'Weapon':[pick_weapon(), randint(10, 30)]
		}
		self.sold_armor = False #If the armor has been sold
		self.sold_weapon = False #If the weapon has been sold

		#If the armor is Nothing, make the price 0
		if self.wares['Armor'][0][1] == 'None':
			self.wares['Armor'][1] = 0
			self.sold_armor = True #Don't let them buy nothning

		#If the weapon is nothing, make the price 0, make them not be able to buy it
		if self.wares['Weapon'][0][1] == "None":
			self.wares['Weapon'][1] = 0
			self.sold_weapon = True #Don't let them buy nothing

	#Lets user choose between buying, selling and
	# converting as much coin into gold
	def shop(self, obj):
		buy = lambda self, player: buy_func(player)
		#List of things to do
		option_list = ['| Buy items', '| Sell items', '| Convert currency']
		selection = 0 #Selected thing out of option list
		choice  = "" #The character option
		while True:
			clear() #Clear screen
			#This is the SHOP GUI thingy.
			print(" _________________________________")
			print("| SHOP")
			print("|_________________________________")
			print("| ESC - Exit shop")
			print("| H - For help (about the shop)")
			print("| W / S - Go through options")
			print("| Enter - Make selection\n|")
			x = 0 #Index of option
			for option in option_list:
				#Adds on '*' if the option is selected
				add_on = lambda index, sel: '*' if index==sel else ''
				#Print option and shows the index that is selected
				print(option + " ({})".format(add_on(x, selection)))
				x += 1 #move onto next value
			print("|_________________________________")

			#Gets the input from the user
			try:
				choice = Getch()
			except:
				#In that case, make the choice nothing if error
				choice = ""

			#If the user is done with the shop
			if choice == "\x1b": 
				print("{}: Thank you for your buisness!".format(self.name))
				pause()
				return obj

			#if the user wants help
			elif choice.lower() == "h":
				print(" _____________________________________________________________")
				print("| HELP")
				print("|_____________________________________________________________")
				print("| Buy items: This option lets you buy stuff from the merchant")
				print("| Sell items: Lets you sell stuff in your bag")
				print("| Convert currency: Converts as much of your money into gold")
				print("|_____________________________________________________________")
				print("Press anything to continue..")
				pause()

			#If the user is moving up and down through options
			elif choice == "w" or choice == "s":
				#Move up on the selection
				if choice == "w" and selection > 0:
					selection -= 1 #Move up on selection

				#Move down on the selection
				elif choice == "s" and selection < 2:
					selection += 1 #Move down on selection

			#If the user makes the selection 
			# on what they want to do
			elif choice == "\r":
				#If the selection is to convert currency
				if selection == 2:
					#Converts as much money as possible
					# to convert the money into gold
					obj = show_convert(obj)

				#The selection is to sell items in one's bag
				elif selection == 1:
					obj = sell_stuff_from_bag(obj, self.name)

				#If the selection is to buy stuff
				elif selection == 0:
					#Allow the user to buy stuff
					self.sold_armor, self.sold_weapon, self.wares['Weapon'][0], self.wares['Armor'][0], obj = buy_func(self.name, self.sold_armor, self.sold_weapon, self.wares['Health potions'], self.wares['Weapon'][0], self.wares['Weapon'][1], self.wares['Armor'][0], self.wares['Armor'][1], obj)

#This has it so that the Priest basically TALKS AT
# the player about their religion, and some parts of the world
def talk(game_mode, exposistion):
	#If this isn't the story mode,
	# give a default answer
	if game_mode == False:
		exposistion = ["The priest looks at you in disgust."]

	clear() #Clear the screen
	#Prints out the dialog
	print(" ____________________________________________________________________________")
	for line in exposistion:
		print("| ", line)
	print("|____________________________________________________________________________")
	print("\nPress enter to continue..")
	pause()

#Will heal the player by 10 or 15 hp if their health is < 100
# and if they already haven't been healed
def heal_player(player_been_healed, obj):
	#If the player can be healed..
	if player_been_healed == False and obj.hp < 100:
		#Makes it so that the player is either healed
		# by either 10 or 15 hp points
		heal_factor = 10 + (rand(0, 1) * 5)

		#If when healed by the given number of hp points
		# it is greater than 100, just make their hp 100
		if (obj.hp + heal_factor) > 100: obj.hp = 100

		#Otherwise, just add heal factor
		else: obj.hp += heal_factor

		player_been_healed = True #Set to true

		#Give a message basically saying "Your healed now bitch"
		print("Your skin starts to feel warmer, you can feel")
		print("millions of needles dig deep into your flesh.")
		print("But, the intense pain quickly subsides.")
		print("You feel more calm now, but you aren't sure why.")
		pause()

	else:
		print("Praying to Thrymm couldn't help you.\n")
		pause()

	return player_been_healed, obj

#This is the class for every Priest instance
class Priest:
	def __init__(self):
		#Randomly pick a name
		self.name = {
			1:"Carter",
			2:"John",
			3:"<Unknown>",
			4:"William",
			5:"George",
			6:"Matthew",
			7:gen_gibberish_name(), #Totally random name
			8:gen_gibberish_name(), #Totally random name
			9:gen_gibberish_name(), #Totally gibbersih name
			10:"Doug",
			11:"Isaac",
			12:"<Forgotten>"
		}.get(rand(1, 12))
		self.pos = (0,0) #Position of preist
		self.char = "P" #Character that represents the priest
		self.have_healed_player = False #Says if they have healed the player
		#List of exposistions they can use
		self.dialog_list = [
			#This will be about the Priest's religion
				["{}:\n|  If you believe in Thrymm, then he will protect you.".format(self.name),
				"He will watch over you, as one of his kin."
				"Defy him, or distrust him, and he will do with you",
				"as he does to those who betray him."],
			#This is another bit on on the Priest's religion
				["{}:\n|  He watches over us, even when we deny him.".format(self.name),
				"He is interested in all of us, even those who defy him.",
				"Those who defy him, although interesting, will meet a terrible fate."],
			#More religious stuff of course
				["{}:\n|  His only companions live alone.".format(self.name),
				"They stand tall, unwavering.",
				"With their arms outstretched, they too watch.",
				"Ever silent, ever faithful."],
			#Did someone say more religious garble? I did
				["{}:\n|  If we stay faithful, and stay true to Thrymm, we will be rewarded.".format(self.name),
				"After we cannot move, nor breathe, we will become one of his companions.",
				"We will live strong, and free from our past mistakes."],
			#Religious garble
				["{}:\n|  Thrymm demands payment, he demands the blood of those who defy him.".format(self.name),
				"As a priest, I too must help Thrymm in getting his payment.",
				"I pass on Thrymm's payment by consumung the flesh, bone and blood.",
				"Would you like to aid me, in giving Thrymm his payment?"],
			#This about the day of 'giving'
				["{}:\n|  When the day of giving comes, we ourselves must give to Thrymm.".format(self.name),
				"He accepts our own blood, but our flesh and our pain soothes him most.",
				"Sometimes, those most thankful might give themselves whole to Thrymm.",
				"To those, they are greatly rewarded by Thrymm."],
			#Religious garble, relating to the end of the world
				["{}:\n|  We didn't think we'd make it, when the dark clouds made the world cold.".format(self.name),
				"The sun burned us harshly, punishment for the sins of the human race.",
				"But then, when all seemed to be at an end, Thrymm came.",
				"He saved us, we are forever indebted to him."],
			#A bit more about the actual world
				["{}:\n|  Blinding bursts of light.".format(self.name),
				"Blistering heat, they couldn't even scream.",
				"Their forms, their silenced screams are forever burned into the world.",
				"We should have seen the signs, we shouldn't have doubted it.",
				"Even Thrymm cannot answer why we were so ignorant."],
			#Garble garble garble
				["{}:\n|  Thrymm made things better.".format(self.name),
				"He made life better.",
				"I'll never be able to see my family again.",
				"They took my family away from me.",
				"I only have Thrymm now."],
			#Smaller garble
				["{}:\n|  Do you accept Thrymm?".format(self.name),
				"When you do, Thrymm will forgive your unwillingness."],
			#Small garble
				["{}:\n|  Why are you even here?".format(self.name)],
			#Small comment
				["{}:\n|  I hope that Thrymm can forgive my past mistakes.".format(self.name),
				"To be one of Thrymm's companions would be an honor."],
			#Last comment
				["{}:\n|  Take what you want and leave.".format(self.name),
				"If you cannot accept Thrymm, I cannot accept you.",
				"Just go."]
		]
		#Randomly pick a piece of dialog to use
		self.dialog = self.dialog_list[rand(0, len(self.dialog_list)-1)]

	#Allows the player to be healed or to talk to the priest
	def heal_or_talk(self, current_game_mode, obj):
		option = "" #Option from the player
		selection = 1 #Selected option
		msg = [] #Message thing
		while option != "\x1b":
			clear() #Clear screen
			print(" ________________________________________")
			print("| PRIEST:")
			print("|________________________________________")
			print("| ESC - Exit")
			print("| W / S - Move up / down through options")
			print("| enter - Make selection\n|")
			#Show if the first value is selected
			print("| Pray (heal) (" + (lambda v: '*)' if v==1 else ')')(selection))
			#Shows if second value is selected
			print("| Talk (" + (lambda v: '*)' if v==2 else ')')(selection))
			print("|________________________________________")
			for message in msg: print(message) #Print out the messages
			msg = [] #Clear message list

			try:
				option = Getch()
			except:
				#Make sure it doesn't explode
				option = ""

			#If the user is going up / down through options
			if option.lower() == "w" or option.lower() == "s":
				#Move up one through selection
				if option.lower() == "w" and selection > 1:
					selection -= 1

				#Move down through selection
				elif option.lower() == "s" and selection < 2:
					selection += 1

			#If the selection is made
			elif option == "\r":
				#Heals player if possible
				if selection == 1:
					self.have_healed_player, obj = heal_player(self.have_healed_player, obj)

				#If the selection is to instead talk
				elif selection == 2:
					talk(current_game_mode, self.dialog)
		return obj

#This is the class of the player
class Player:
	def __init__(self, name):
		self.name = name
		self.char = "@" #Character that rep. this object
		self.hp = 25 #Health points
		self.dmg = 5 #Regular hand-hand damadge
		self.armor_class = 10 #What other needs to 'get' to hit you 
		self.inventory = {'primary':(0, 'None'), 
		'health potions':2, 'armor':(0, 'None'), 
		'gold':0, 'silver':0, 'bronze':0, 
		'bag':{ #Random items that the user has
			1:(0, 'None'),
			2:(0, 'None'),
			3:(0, 'None'),
			4:(0, 'None'),
			5:(0, 'None'),
			6:(0, 'None')
			}
		}
		self.pos = (0,0) #Position of player (X, Y)

#Class for every zombie instance
class Zombie:
	def __init__(self, name = "Zombie"):
		self.name = name
		self.char = "Z" #Char. that rep. this object
		self.hp = 11 #The hp
		self.dmg = 5 #Damadge that it deals
		self.armor_class = 9 #AC
		self.pos = (0,0) #Position of zombie (X, Y)

#Class for every Monster instance
class Minotaur:
	def __init__(self, name = "Minotaur"):
		self.name = name
		self.char = "M" #Char. that rep. this object
		self.hp = 16
		self.dmg = 9 #Damadge that it deals
		self.armor_class = 8 #AC
		self.pos = (0,0) #Positin of monster (X, Y) 

#Class for every Ker instance
class Ker:
	def __init__(self, name = "Ker"):
		self.name = name
		self.char = "K" #Char. that rep. this object
		self.hp = 6
		self.dmg = 2 #Damadge it deals
		self.armor_class = 11 #AC
		self.pos = (0,0) #Position of Ker (X, Y)

#Class for every Nymph instance
class Nymph:
	def __init__(self, name = "Nymph"):
		self.name = name
		self.char = "N" #Char. that rep. this object
		self.hp = 6
		self.dmg = 2 #Damadge it deals
		self.armor_class = 13 #AC
		self.pos = (0,0) #Position of Nymph (X, Y)

#The class for every Boss instance
class Behemoth:
	def __init__(self, name = "Behemoth"):
		self.name = name
		self.char = "B" #char. that rep. this object
		self.hp = 400 #Hp
		self.dmg = 15 #Damadge it deals
		self.armor_class = 15 #AC
		self.pos = (0,0) #Position of Boss (X, Y)

#This lets any enemies around the player, attack the player
def enemy_attack(obj, dialog_list, space, mob_dict):
	#Get all of the areas around the player
	areas = spaces_around_player(obj.pos)
	not_usable = list("|-_# ") #stuff we can't use
	#Use areas not occupied by wall or chest
	areas = [val for val in areas if not space[val[1]][val[0]] in not_usable]

	#Get the armor class of the user
	user_armor_class = obj.armor_class + obj.inventory['armor'][0]

	#list of the mob index's (the mobs that can attack)
	enemys_to_attack = []

	#get the enemies that can attack
	for index in mob_dict:
		#If the monster is in range to attack
		if mob_dict[index].pos in areas:
			#Add their index so they can attack
			enemys_to_attack.append(index)

	#Go through enemies that can attack-
	# and make them 'attempt' to attack
	for index in enemys_to_attack:
		#If the enemy's 'roll' passes- allow them to strike
		if d20_roll() >= user_armor_class:
			#Add that the monster struck the human
			dialog_list.append("{} attacked!".format(mob_dict[index].name))
			#Deal damage to the player
			obj.hp -= mob_dict[index].dmg
	
		#The monster missed
		else:
			#tell user that they missed
			dialog_list.append("{} missed!".format(mob_dict[index].name))

	#Return player
	return obj, dialog_list

#Sees if we can use tha value
def try_pos(pos, space):
	#Attempts to use a position that is usable
	try:
		if space[pos[1]][pos[0]] == ".":
			return True
		return False #Can't be used

	#Return false, can't be used
	except IndexError:
		return False

#Returns a mob (besides boss for story mode)
# based on a number from 1 -> 5
def select_mob(n):
	if n == 1: return Zombie()
	elif n == 2: return Minotaur()
	elif n == 3: return Ker()
	elif n == 4: return Nymph()
	elif n == 5: return Behemoth()

#Selects a few positions, and makes X amount of monsters
def randomly_get_monster(all_pos, times, mob_dict, end=4):
	# if end == 4, then it is for story mode, otherwise
	# that means that it is a part of endless mode

	pos_selection = []

	times_1 = times #Number of times to run
	#Randomly generate positions to use
	while times_1 > 0:
		#The index to select from
		index = randint(0, len(all_pos)-1)
		#use that selected position
		pos_selection.append(all_pos[index])
		#Remove that position
		del all_pos[index]
		#To keep us from an error, just say that this is enough
		if len(all_pos)==0: break

		times_1 -= 1

	x = 0 #Index number
	while x < times:
		#Prematurely stop if there are no more positions we can use
		if len(pos_selection) == 0: break

		#Makes a monster (randomly)
		mob_dict[x] = select_mob(randint(1, end))

		#Gives the monster one of the positions
		mob_dict[x].pos = pos_selection.pop()

		x += 1 # Move onto next index

	#Remove the positions that were taken up
	for index in mob_dict:
		#Remove used up positions
		all_pos = [x for x in all_pos if x != mob_dict[index].pos]

	#Return the number of total positions + mobs
	return all_pos, mob_dict

#We will use this to generate monsters into the new room
def generate_monsters(space, floor, obj, mob_dict):
	end_select = 4 #Select monsters, not including Behemoth

	#All of the positions available
	pos = [(x, y) for x in range(1, len(space)-1) for y in range(1, len(space[0])-1)]
	#Don't use user's position
	pos = [val for val in pos if val != obj.pos]

	#Keep all positions that aren't a problem
	p = [enemy_pos for enemy_pos in pos if try_pos(enemy_pos,space)==True]

	#The number of monsters to make
	monsters = randint(1, 4)

	#Makes the monsters, and all of the positions not used up
	all_pos, mob_dict = randomly_get_monster(p, monsters, mob_dict, end_select)

	return all_pos, mob_dict

#Generates chests, using positions from generating monsters
def generate_chests(all_pos, space, obj, mob_dict, obj_dict):
	room_h = len(space)-2 #Height of room
	room_w = len(space[0])-2 #Width of room

	#All four corners of the room..
	room_corners = [(1, 1), (1, room_h), (room_w, room_h), (room_w, 1)]

	#Extra precaution- makes it so monsters
	# cannot be trapped in corners because of chests
	for index in mob_dict:
		#Position of each mob
		mob_pos = mob_dict[index].pos

		#If the mob is in one of the four corners..
		#Remove the spaces around it from being used
		if mob_pos in room_corners:
			#Areas around the mob
			areas_off_limits = spaces_around_player(mob_pos)
			#Get rid of those areas that might block the mob
			all_pos = [pos for pos in all_pos if not pos in areas_off_limits]

	#Number of chests, 2/4 times there'll be 0 chests,
	# 1/4 times there is 1 chest, 1/4 times there are 2 chests
	n = randint(-2, 2)
	#The number of chests we'll make
	chest_number = (lambda n: 0 if n < 0 else n)(n)

	#Only do this if there actually are mobs
	if len(mob_dict) > 0:
		#Uses positions that aren't already taken
		for index in mob_dict:
			#Goes through, getting rid of the mob's positions
			all_pos = [value for value in all_pos if value != mob_dict[index].pos]

	#Remove previous chests
	index_list = range(0, len(obj_dict))
	for index in index_list: del obj_dict[index]

	#If there are no positions to use..
	# then just return the list of objects
	if len(all_pos)==0: return obj_dict

	x = 0
	#Keep goin' till we have all the chests needed
	while x < chest_number:
		#If there are no positions in all of the positions..
		# just stop, and say that is good enough
		if len(all_pos)==0:break

		#Turn that index into a new chest index
		obj_dict[x] = Chest()
		#Give that chest it's index
		obj_dict[x].index = x

		Pos = (100, 100) #trigger it, can't be used
		#get a new position
		while True:
			#If we can't use that position
			if try_pos(Pos, space)==False:
				#Get a new position
				Pos = all_pos[randint(0, len(all_pos)-1)]
			
			else:
				#Get rid of the position that we got as a 'solution'
				all_pos = [val for val in all_pos if val != Pos]
				break

		obj_dict[x].pos = Pos

		x += 1 #Move onto next chest

	return obj_dict

#Generate all of the spots around the room that we can use
def gen_spots(space, mob_dict, obj):
	#All of the positions available
	pos = [(x, y) for x in range(1, len(space)-1) for y in range(1, len(space[0])-1)]
	#Don't use user's position
	pos = [val for val in pos if val != obj.pos]

	#Keep all positions that aren't a problem
	positions = [chest_pos for chest_pos in pos if try_pos(chest_pos,space)==True]

	return positions

#Gives every space around the item including corners
all_spaces_around_item = (lambda pos: 
	[(pos[0]-1, pos[1]), (pos[0]-1, pos[1]-1), (pos[0]-1, pos[1]+1),
	(pos[0]+1, pos[1]), (pos[0]+1, pos[1]-1), (pos[0]+1, pos[1]+1),
	(pos[0], pos[1]-1), (pos[0], pos[1]+1)])

#Generate all of the spots that can be used for preists and vendors
def gen_spots_for_preist_and_vendor(space, mob_dict, obj_dict, obj):
	p = gen_spots(space, mob_dict, obj) #Get all positions

	#Remove all positions relating to the objects (chests)
	for index in obj_dict:
		#Remove each coordinate that a chest is using
		p = [pos for pos in p if pos != obj_dict[index].pos]
		#Remove any coordinates around the chests
		p = [pos for pos in p if not pos in all_spaces_around_item(obj_dict[index].pos)]

	return p

#This is just chests in a room, no mobs
def generate_lonely_chest(space, mob_dict, obj_dict, obj):
	#Get the positions
	p = gen_spots(space, mob_dict, obj)

	#Generate chests
	return generate_chests(p, space, obj, mob_dict, obj_dict)

#FOR ENDLESS MODE:
# Takes in the 'stats' of an enemy and
# randomizes it (might make them tougher)
def randomize_enemy_stats(obj):
	#This will be the health of the mob
	health = randint(obj.hp, obj.hp * 2)
	#This will be the damage that the mob deals
	damage = randint(obj.dmg, obj.dmg * 2)
	#Give object it's new health
	obj.hp = health
	#Give the object how much damage it will deal now
	obj.dmg = damage

	return obj

#Takes the obj (player) and room and generates
# a bunch of positions that can be used by behemoths.
def mk_behemoth_pos(obj, space):
	#The boss cannot spawn right next to the player
	areas = spaces_around_player(obj.pos)
	height = len(space)-1 #height of room
	width = len(space)-2 #width of room
	
	#Give all of the positions that the boss could be 
	spaces = [(x,y) for x in range(1, height) for y in range(1, width)]
	#Use positions that will work
	spaces = [pos for pos in spaces if try_pos(pos,space)==True]
	#Boss not alowwed to spawn by player
	spaces = [pos for pos in spaces if not pos in areas]

	return spaces

roll_for_monster_filled_room = lambda: randint(0, 2)

# This deals with the actions of the player (and mobs)
def mov_user(mode, obj, space, floor, symbol, mobs, obj_dict, chg_floor, start_time,addTime,char=""):
	story_mode = False #If the game is in story mode
	add_time = 0 #how much time we should add to current time (for endless mode)

	exit = False

	#If this IS the story mode
	if mode == "story": story_mode = True

	skip_ai = False #Skip turn of ai

	#Feedback from say attacking that will be printed
	dialog = []

	#If char isn't a pre-defined value (i.e. the user is moving)
	# then get one-character input
	if char == "":
		try:
			char = Getch() #Get character
		except:
			char = ""
			return obj.pos, space, floor, mobs, obj_dict, dialog, True, False, add_time

	new_pos = list(obj.pos)

	#Move up one position (collide w/ ceiling)
	if char == "w" or char == "W":
		#If the player can move
		if not ceiling_above(obj.pos, space):
			new_pos[1] = obj.pos[1] - 1

	#Move down one position (collide w/ wall)
	elif char == "s" or char == "S":
		#If the player can move
		if not floor_below(obj.pos, space):
			new_pos[1] = obj.pos[1] + 1

	#Moves right one position (collide w/ wall)
	elif char == "d" or char == "D":
		#If the user can move
		if not wall_right(obj.pos, space):
			new_pos[0] = obj.pos[0] + 1

	#Moves left one position (collide w/ floor)
	elif char == "a" or char == "A":
		#If the player can move
		if not wall_left(obj.pos, space):
			new_pos[0] = obj.pos[0] - 1

	#If the user is trying to attack any nearby enemies
	elif char == "q" or char == "Q":
		#This gets a list of all of the enemies around the player.
		surrounding_enemies = get_enemies_in_attack_area(mobs, obj.pos)

		#If there are actually monsters to attack
		if len(surrounding_enemies) > 0:
			#Go through every monster around the player
			for value in surrounding_enemies:
				#If the player's attack actually hit the monster
				if d20_roll() >= mobs[value[0]].armor_class:
					#Get the damadge that the user will deal
					damadge = obj.dmg + obj.inventory['primary'][0]
					#deals damadge to the mob
					mobs[value[0]].hp -= damadge

					dialog.append("{}'s attack hit!".format(obj.name))

				#If the player's attack missed
				else:
					dialog.append("{}'s attack missed!".format(obj.name))

			death_list = [] #List of monsters that were killed
			loot = {'gold':0, 'silver':0, 'bronze':0}#Loot gained

			#Checks through all the monsters
			for value in surrounding_enemies:
				#If any of the monsters were killed
				if mobs[value[0]].hp <= 0:
					#Gets position of the mob
					mob_pos = mobs[value[0]].pos
					#Makes the monster disappear
					space[mob_pos[1]][mob_pos[0]] = "."

					#If the mob isn't a behemoth
					if mobs[value[0]].name != "Behemoth":
						#Adds to the number of gold
						loot['gold'] += randint(0, 5)
						#Adds to the number of silver
						loot['silver'] += randint(0, 5)
						#Adds to the number of bronze
						loot['bronze'] += randint(0, 5)

					#If the mob is a Behemoth, then the payload
					# should be much more
					elif mobs[value[0]].name == "Behemoth":
						#Adds to the amount of gold
						loot['gold'] = randint(10, 20)
						#Adds to the number of silver
						loot['silver'] = randint(10, 25)
						#Adds to the number of bronze
						loot['bronze'] = randint(10, 25)

					#Adds index to monsters that are dead
					death_list.append(value[0])

			#If monsters were killed
			if len(death_list) > 0:
				#Gets rid of the dead mobs
				for index in death_list:
					#make sure program doesn't explode
					try:
						del mobs[index]
					except:
						pass

				GOLD, SILVER, BRONZE = loot['gold'],loot['silver'],loot['bronze']
				
				#Prints out the additional gold, silver, bronze that the player got				
				dialog.append(gained_coin(obj.name, GOLD, SILVER, BRONZE))

				#Add the new gold to number of gold that the player has
				obj.inventory['gold'] += loot['gold']
				#Add the new silver to the silver that the player has
				obj.inventory['silver'] += loot['silver']
				#Add bronze the number of bronze owned by the player
				obj.inventory['bronze'] += loot['bronze']

				#If the player randomly got a health potion!
				if d5_roll() == 1:
					#Adds 1 to the number of potions that the player has
					obj.inventory['health potions'] += 1
					#Tells player that they got a health potion randomly!
					dialog.append("{} gained a health potion!".format(obj.name))

		#If there are no monsters to attack, do nothing
		else:
			pass

	#If the user wants to look at their inventory
	elif char == "i" or char == "I":
		#Does inventory gui thing
		obj = inventory(obj)

		#Skips ai's turn so the user isn't screwed
		skip_ai = True

	#Help for the user
	elif char == "h" or char == "H":
		clear()
		#Help header
		help_head = "\n _   _   ______   _        ____\n| | | | |  ____| | |      | _  \\\n| |_| | | |___   | |      |  __/\n|  _  | |  ___|  | |      | |\n| | | | | |____  | |____  | |\n|_| |_| |______| |______| |_|\n__________________________________\n__________________________________"
		print(help_head) #Print 'help' header
		print("@ -> Player ({})".format(obj.name))
		#Only print thid out if a part of story mode
		if story_mode==True: 
			print("FLOOR: {} -> The floor number currently on (get to floor 1)".format(floor))
		#Tell user what their objective is
		else:
			print("OBJECTIVE: Get as much gold as possible, live as long as possible")

		#Shows that this is keybindings
		print("\nKEY BINDINGS:\n______________")
		print("ESC (Escape key) -> Exit game")
		print("W -> UP")
		print("A -> LEFT")
		print("S -> DOWN")
		print("D -> RIGHT")
		print("Q -> ATTACK (monsters to left, right, up and down)")
		print("E -> INTERACT (open chests)")
		print("H -> Brings up help menu (this)")
		print("I -> Brings up inventory menu")
		#Tell user about save option in the endless mode
		#if story_mode == False:
		print("P -> Save game (as well as load save, and delete save)")
		print("enter -> Descend a floor (given that there are no mobs)")
	
		print("\nPress anything to continue..")
		pause()
		clear()

		print(help_head)
		print("OBJECTS:\n_________")
		print(". -> Empty space")
		print("| - _   ->   Walls") 
		print("# -> Chest")

		print("\nENEMIES:\n_________")
		print("Z -> Zombie")
		print("M -> Minotaur")
		print("K -> Ker")
		print("N -> Nymph")
		print("B -> Behemoth")

		print("\nNPCs:\n__________")
		print("S -> Shopkeep / Merchant")
		print("P -> Priest (healer)")

		print("\nPress anything to continue..")
		pause()

		print(help_head)

		print("CURRENCY EXCHANGERATE:")
		print("________________________________")
		print("100 bronze coins = 1 silver coin")
		print("100 silver coints = 1 gold coins")

		print("Press anything to continue..")
		pause()

		skip_ai = True #Skip ai's turn

	#If the user wants to load / save a game and its endless mode
	elif char.lower() == "p": #and story_mode == False:
		#Make it so monsters do attack the player after they are
		# in this menu.. cause I think that it is nice personally
		skip_ai = True

		dialog_save = [] #List of dialog for saves
		option = "" #Option from the player
		selection = 1 #Which option was picked out
		while option != "\x1b": #While they don't press escape
			clear() #Clear screen for animation
			
			print(" _____________________________")
			print("| Save / Load Game")
			print("|_____________________________")
			print("| ESC - Exit")
			print("| W / S - Go through options")
			print("| Enter - pick option\n|")
			# shows if the save game option was picked
			print("| Save game ("+(lambda v: '*)' if v==1 else ')')(selection))
			# Shows if we picked the load game option
			print("| Load game ("+(lambda v: '*)' if v==2 else ')')(selection))
			#If the user wants to delete a save
			print("| Delete save ("+(lambda v: '*)' if v==3 else ')')(selection))
			print("|_____________________________")
			#Print out each message in message list
			for msg in dialog_save: print(msg)

			try:
				option = Getch()
			except:
				#So we don't explode
				option = ""

			dialog_save = [] #Clear out list


			# If the user wants to go up / down through options
			if option.lower() == "w" or option.lower() == "s":
				#If the user wants to go up by one option
				if option.lower() == "w" and selection > 1:
					selection -= 1

				#If the user wants to go down by one option
				elif option.lower() == "s" and selection < 3:
					selection += 1

			#When the player makes selection
			elif option == "\r":

				#Returns string representing object type of x
				def object_type(x):
					#Return string saying that it is a chest
					if type(x) == type(Chest()): return "chest"
					#Return string saying that it is a priest
					elif type(x) == type(Priest()): return "priest"
					#Return string saying that it is a vendor
					elif type(x) == type(Vendor()): return "vendor"

				#Returns a string telling what type of monster is it (it being x)
				def monster_type(x):
					#Zombie, Minotaur, Ker, Nymph, Behemoth
					#If x is a zombie
					if type(x) == type(Zombie()): return "zombie"
					#If x is a minotaur
					elif type(x) == type(Minotaur()): return "minotaur"
					#If x is a ker
					elif type(x) == type(Ker()): return "ker"
					#If x is a nymph
					elif type(x) == type(Nymph()): return "nymph"
					#If x is a behemoth
					elif type(x) == type(Behemoth()): return "behemoth"

				#With the info about the monster, spits back an object with the info used
				def define_monster(info):
					spawned_mob = 0 #Return object

					#Make the object based on what it is
					if info[0] == "zombie": spawned_mob = Zombie()
					elif info[0] == "minotaur": spawned_mob = Minotaur()
					elif info[0] == "ker": spawned_mob = Ker()
					elif info[0] == "nymph": spawned_mob = Nymph()
					elif info[0] == "behemoth": spawned_mob = Behemoth()

					#Update the position
					spawned_mob.pos = info[1]
					#Update health
					spawned_mob.hp = info[2]
					#Update how much damage it deals
					spawned_mob.dmg = info[3]
					#Update armor class
					spawned_mob.armor_class = info[4]

					return spawned_mob

				#Given the info about the object, spawns the object and returns it
				def define_object(info):
					#If it is simply a chest
					if info[0] == "chest":
						Object = Chest() #Spawn chest
						Object.index = info[1] #Update index
						Object.pos = info[2] #Update position
						#Update weapon and armor
						Object.weapon, Object.armor = info[3], info[4] 
						#Update the number of health potions
						Object.hp_potions = info[5]
						#Update coins
						Object.coins = info[6]
						return Object #All done

					#If it is a priest
					elif info[0] == "priest":
						Object = Priest() #Spawn priest
						Object.name = info[1] #Give it it's name
						Object.pos = info[2] #Update position
						Object.have_healed_player = info[3] #If they have healed the player
						Object.dialog = info[4] #Dialog

						return Object #All done

					#If this is a vendor
					elif info[0] == "vendor":
						Object = Vendor() #Spawn a vendor
						Object.name = info[1] #Give name
						Object.pos = info[2] #Update position
						Object.wares = info[3] #Update wares
						Object.sold_armor = info[4] #Has armor been sold
						Object.sold_weapon = info[5] #Has weapon been sold

				#If the user is making a save, and there are only like 4 saves
				if selection == 1 and len(eval(open('DownwardDescent_Saves.txt', 'r').read())) < 5:
					Time = int((time() - start_time)/60) #Time in mins
					#The name that the save will be saved as
					save_name = input("\nName of save?: ")
					while True:
						#If the the name has already been used
						if save_name in eval(open('DownwardDescent_Saves.txt', 'r').read()):
							#Gets a new save name
							save_name = input("\nApologies, that save name was already used.\nPlease enter a different name:\n")

						#Otherwise, we're all good
						else:
							break

					room_height = len(space)-2 #Height of room
					room_width = len(space[0])-2 #Width of room
					#All of the information from the player
					player_info = {
						'hp':obj.hp, 'primary':obj.inventory['primary'],
						'armor':obj.inventory['armor'], 'pos':obj.pos,
						'health potions':obj.inventory['health potions'], #Hp potions
						'bag':obj.inventory['bag'], #'time':time, #The time (in mins) from last time
						'gold':obj.inventory['gold'],
						'silver':obj.inventory['silver'], 'bronze':obj.inventory['bronze'],
						'char':'@', 'floor':floor,'time':Time #Floor number + time (in mins)
					}
					#Information on all of the objects
					objects_info = {}
					#Go through every object
					for index in obj_dict:
						#If the object is a chest
						if object_type(obj_dict[index]) == "chest":
							chest = obj_dict[index] #Particular chest
							#INDEX ARMOR, WEAPON, POTIONS, GOLD, SILVER, BRONZE
							chest_info = (
								"chest", chest.index, #index
								chest.pos, #Postition
								chest.weapon, chest.armor, #Contained armor + weapon
								chest.hp_potions, #Potions
								chest.coins #The coins that the chest has
							)
							#Add info on chest into the objects dictionary
							objects_info[index] = chest_info

						#If the object is a priest
						elif object_type(obj_dict[index]) == "priest":
							priest_i = obj_dict[index] #Particular priest
							#All of the info for the priest
							priest_info = (
								"priest", #Denote that this is a priest
								priest_i.name, priest_i.pos, #Name and posistion
								priest_i.have_healed_player, #If they have healed player
								priest_i.dialog #Dialog
							)
							#Saves all of the information about the priest info
							objects_info[index] = priest_info

						#If the object is a vendor (shop)
						elif object_type(obj_dict[index]) == "vendor":
							vendor_i = obj_dict[index] #This vendor instance
							#All information about this vendor instance
							vendor_info = (
								"vendor", #Denotes that this is a vendor
								vendor_i.name, 
								vendor_i.pos, vendor_i.wares, #Wares and position of instance
								vendor_i.sold_armor, #If armor has been sold
								vendor_i.sold_weapon #If weapon has been sold
							)
							#Saves the information about this item
							objects_info[index] = vendor_info

					#Information any any / all monsters
					monster_info = {}
					#Go through every monster
					for index in mobs:
						mob = mobs[index] #This particular mob
						mob_info = ( #Info on this mob
							monster_type(mob), #type of monster
							mob.pos, #Posistion of monster
							mob.hp, mob.dmg, #Health + damage they deal
							mob.armor_class #Armor class
						)
						#Add on the information on this monster
						monster_info[index] = mob_info

					#All of the information about the room, etc.
					save_info = {'height':room_height, 'width':room_width, #Size of room..
					'player':player_info, 'objects':objects_info, #Player info + object info!
					'mobs':monster_info, #Information about the monsters at that moment
					}

					_password = "" #The password
					#Warn the user
					#print("Warning: Some  passwords won't work for")
					#print("encrypting and decrypting the information")
					#print("relating to the save.\n")
					while _password == "": #While the password is nothing
						#Password for the file
						_password = input("Password?: ")

						#If the password doesn't work
						if check_password(_password) == False:
							_password = "" #Clear out password
							print("Apologies, this password will not work for")
							print("encrypting / decrypting your save,")
							print("please give a different password.\n")

					#Using the password, we encrypt all of the info
					encrypted_info = encrypt_save(_password, save_info)

					#Open up the saves from the saves file
					saves = eval(open('DownwardDescent_Saves.txt', 'r').read())
					#Clear out the file
					open('DownwardDescent_Saves.txt', 'w').close()
					#Add the save info to the list of saves under the given name
					saves[save_name] = encrypted_info
					#Set up everything to write the info. of the new / past saves
					new_save_file = open('DownwardDescent_Saves.txt', 'w')
					#Write the save file into the file again
					new_save_file.write(str(saves))
					new_save_file.close() #Stop using file

				#If there are like 5 saves, say that the user can't make
				# any more saves unless they delete a save
				elif selection == 1 and len(eval(open('DownwardDescent_Saves.txt', 'r').read())) == 5:
					dialog_save.append("You have used the max 5 save slots.\nTo make a new one, delete a previous save.")

				#If a save is being loaded
				elif selection == 2:
					#Get the save files so we can load up one
					saves = open('DownwardDescent_Saves.txt', 'r').read()
					saves = eval(saves) #Evaluate the save files
					save_choice = "" #Save chosen by the user
					skip_save_proc = False #Tells us if we aren't loading a save
					while True:
						clear() #Clear out screen
						print(" ________________________________")
						print("| Load save (selection)")
						print("|________________________________")
						print("| Enter 'quit' or 'exit' to stop\n|")
						#Show each save file
						for save_file in saves: print("| ", save_file)
						print("|________________________________")
						#Get the file wanted to be loaded
						save_choice = input("Enter the name of the save that you want to load\n(Please note that this is case sensitive)\n: ")

						if save_choice == "quit" or save_choice == "exit":
							skip_save_proc = True
							break

						#If the save file actually exists
						if save_choice in saves:
							break

					#If we have not been told to skip this
					if not skip_save_proc:
						_password = "" #The 'password' given by user 

						#Get password
						_password = input("\nPassword?: ")

						#Tries to decrypt the info wanted, then loads the game
						try:
							save_data = eval(decrypt_save(_password, saves[save_choice]))

							#PLAYER STUFF:
							#__________________
							#Makes the room based on its size
							space = mk_room(save_data['height'], save_data['width'])
							#Makes life easier for accessing this data
							player_info = save_data['player']
							obj.hp = player_info['hp'] #Change hp
							#Update the primary weapon
							obj.inventory['primary'] = player_info['primary']
							#Updates the armor
							obj.inventory['armor'] = player_info['armor']
							#Update the posistion
							obj.pos = player_info['pos']
							#Updates the bag of the player
							obj.inventory['bag'] = player_info['bag']
							#Update number of health potions
							obj.inventory['health potions'] = player_info['health potions']
							#Update gold
							obj.inventory['gold'] = player_info['gold']
							#Update silver
							obj.inventory['silver'] = player_info['silver']
							#Update bronze
							obj.inventory['bronze'] = player_info['bronze']
							#Change the floor number
							floor = player_info['floor']
							#Add onto the total time
							addTime += player_info['time']

						#Tell the user that it was the wrong password
						except SyntaxError:
							print("Incorrect password.")
							pause()

						#Tell the user that it was the wrong password
						except TypeError:
							print("Incorrect password.")
							pause()

						#Tell the user if the password was invalid,
						# as the info. was unacceptable to the program
						except ValueError:
							print("Incorrect password.")
							pause()

						else:
							#Loads the game!
							#==================							

							#Monster stuff:
							#_________________
							mobs = {} #Clear out mobs dict
							i = 0 #Stupid iterator value
							for index in save_data['mobs']:
								#Spawn monster
								mobs[index] = define_monster(save_data['mobs'][i])
								i += 1

							#Object stuff:
							#_________________
							obj_dict = {} #Clear out object dict
							i = 0 #Stupid iterator value
							for index in save_data['objects']:
								#Spawns the object
								obj_dict[index] = define_object(save_data['objects'][index])

								#If this isn't a freaking mob, remove it
								if obj_dict[index] == None:
									del obj_dict[index]

							#Draw in the player
							space[obj.pos[1]][obj.pos[0]] = "@"

							#Draw in every mob
							for index in mobs:
								#Gets position of the monster
								mob_pos = mobs[index].pos
								#Draws in that monster
								space[mob_pos[1]][mob_pos[0]] = mobs[index].char

							#Draw in every object
							for index in obj_dict:
								#Gets position of that object
								object_pos = obj_dict[index].pos
								#Draw in that object
								space[object_pos[1]][object_pos[0]] = obj_dict[index].char

							skip_ai = True #Skip the ai's turn

							#Finally, spit back everything so we start up
							return obj.pos, space, floor, mobs, obj_dict, dialog, skip_ai, exit,player_info['time']

				#If the user wants to delete a save file
				elif selection == 3:
					#Opens up and reads the file
					saves = eval(open('DownwardDescent_Saves.txt', 'r').read())
					save_name = "" #Name of save file to be deleted
					dont_delete = False
					while True:
						clear() #Clear the screen
						print(" ______________________________")
						print("| Save Files:")
						print("|______________________________")
						print("| type 'quit' or 'esc' to stop\n|")
						#Print each save name
						for save_name in saves: print("| ", save_name)
						print("|______________________________")
						print("Enter the save file you want to load\n(Note that this is case sensitive)")
						save_name = input(": ")

						if save_name.lower() == "quit" and not "quit" in saves or save_name.lower() == "esc" and not "esc" in saves:
							dont_delete = True
							break

						#Exit out if it is an existing save name
						if save_name in saves:
							break

					#If we are deleting something
					if dont_delete == False:
						#Delete that save file
						del saves[save_name]
						#Clear out the file
						open('DownwardDescent_Saves.txt', 'w').close()
						#Write the new versions of the saves
						save_file = open('DownwardDescent_Saves.txt', 'w')
						#Write the save file
						save_file.write(str(saves))
						save_file.close()

	#Interect (open) chests 
	elif char == "e" or char == "E":
		#Give the objects around the player
		surrounding_objects = chests_in_area(obj_dict, obj.pos)
		#Only get the instances that are ACTUALLY CHESTS
		surrounding_chests = [x for x in surrounding_objects if type(obj_dict[x[0]])==type(Chest())]
		#Only gets the Merchants that are around the player
		surrounding_merchant = [x for x in surrounding_objects if type(obj_dict[x[0]])==type(Vendor())]
		#Only gets the Priests that are around the player
		surrounding_priests = [x for x in surrounding_objects if type(obj_dict[x[0]])==type(Priest())]

		#If there are chests around the player
		if len(surrounding_chests) > 0:
			#Goes and opens each and every chest
			for index in surrounding_chests:
				obj = obj_dict[index[0]].open_chest(obj)

		#If instead, there is a merchant by the player, 
		# let the player interact with the merchant
		if len(surrounding_merchant) > 0:
			#Let the player interact with the merchant(s)
			for index in surrounding_merchant:
				obj = obj_dict[index[0]].shop(obj)

		#If if instead that 
		if len(surrounding_priests) > 0:
			#Lets player to interact with the priest
			for index in surrounding_priests:
				obj = obj_dict[index[0]].heal_or_talk(story_mode, obj)

	#If the user is done (exit)
	elif char == "\x1b":
		print("Do you want to stop?")
		print("Y / N") 
		while True:
			#get input from the user
			choice = Getch()
			#Then stop the game
			if choice == "y" or choice == "Y":
				print("You have retired.")
				pause()
				return obj.pos, space, floor, mobs, obj_dict, dialog, skip_ai, True, addTime
			
			#If the game should continue
			elif choice == "n" or choice == "N":
				#Skip the ai so that the user can continue
				skip_ai = True
				break

	#If the user wants to go onto next floor
	elif char == "\r" and len(mobs) == 0:
		#Generate the new room
		space, new_pos = character_setup()
		new_pos = tuple(new_pos)
		space[new_pos[1]][new_pos[0]] = symbol #Draws character
		floor += chg_floor #Add chng_floor to the floor number
		
		#If we are doing story mode and not endless mode
		if story_mode == True:
			#If we are on the last floor
			if floor == 1:
				#Gets positions that the behemoth can use
				all_pos = mk_behemoth_pos(obj, space)

				mobs[0] = Behemoth()
				#Randomly pick a position
				mobs[0].pos = all_pos[rand(0, len(all_pos)-1)]
				#Position of boss
				boss_pos = mobs[0].pos
				#Draws in the boss
				space[boss_pos[1]][boss_pos[0]] = mobs[0].char

			#If we aren't on the first floor
			elif floor > 1:
				#If there is '1', then there'll be monsters
				if roll_for_monster_filled_room():
					#Gives back all of positions that can be used
					# and also the mobs that have been modified
					all_pos, mobs = generate_monsters(space, floor, obj, mobs)

					#Draw the monsters
					for index in mobs:
						mob_pos = mobs[index].pos #position of monster
						#Draws the monster at their position
						space[mob_pos[1]][mob_pos[0]] = mobs[index].char

					#The new objects
					obj_dict = generate_chests(all_pos, space, obj, mobs, obj_dict)

					#Draws the chests
					for index in obj_dict:
						#Gets position of the chest
						chest_pos = obj_dict[index].pos
						#Draws the current chest
						space[chest_pos[1]][chest_pos[0]] = obj_dict[index].char

				#Else, a room with out any mobs..
				# will spawn a random number of chests though
				else:
					#Randomly generate mobs
					obj_dict = generate_lonely_chest(space, mobs, obj_dict, obj)

					#Draws the chests
					for index in obj_dict:
						#Gets position of the chest
						chest_pos = obj_dict[index].pos
						#Draws the current chest
						space[chest_pos[1]][chest_pos[0]] = obj_dict[index].char

					chest_positions = []
					#Collect positions of all the chests
					for index in obj_dict:
						#Get all of the positions of the monsters
						chest_positions.append(obj_dict[index].pos)

					#The positions that the Vendor and Priest can use
					positions_for_else = gen_spots_for_preist_and_vendor(space, mobs, obj_dict, obj)

					#If a merchant is spawned, and there is enough room
					# for a merchant instance.. then spawn one
					if randint(0, 1) and len(positions_for_else) > 0:
						#Make a vendor instance
						obj_dict[len(obj_dict)] = Vendor()
						#Randomly select a space for the merchant to be at
						obj_dict[len(obj_dict)-1].pos = positions_for_else[rand(0, len(positions_for_else)-1)]

						#These are all of the points we will filter out..
						#those being spots around the vendor, or used by the vendor
						exclude_spaces = all_spaces_around_item(obj_dict[len(obj_dict)-1].pos) + [obj_dict[len(obj_dict)-1].pos]
						#Exclude spaces used up
						positions_for_else = [pos for pos in positions_for_else if not pos in exclude_spaces]

						#Draw in the merchant
						POS_FOR_MERCH = obj_dict[len(obj_dict)-1].pos
						space[POS_FOR_MERCH[1]][POS_FOR_MERCH[0]] = obj_dict[len(obj_dict)-1].char

					#If the Priest spawns, and there are spaces for
					# the priest to occupy, let the priest spawn
					elif randint(1, 3)==1 and len(positions_for_else) > 0:
						#Make a priest instance
						obj_dict[len(obj_dict)] = Priest()
						#Randomly selects a spot for the priest
						obj_dict[len(obj_dict)-1].pos = positions_for_else[rand(0, len(positions_for_else)-1)]

						POS_FOR_PRIEST = obj_dict[len(obj_dict)-1].pos
						#Draw in the priest
						space[POS_FOR_PRIEST[1]][POS_FOR_PRIEST[0]] = obj_dict[len(obj_dict)-1].char

			skip_ai = True #Skip Ai's turn in the next room
		
		#For endless mode
		elif story_mode == False:

			#If it is time to spawn some Behemoths
			if (floor % 50)==0:
				#Decides how many behemoths they'll fight
				Behemoth_number = randint(1, 3)

				#Gets positions that the behemoth(s) can use
				all_pos = mk_behemoth_pos(obj, space)
				#Filter out positions that won't work
				all_pos = [pos for pos in all_pos if try_pos(pos, space)==True]

				#If we don't have any positions, then don't make monsters
				if len(all_pos)==0: Behemoth_number = 0

				x = 0 #Iterator for making behemoth(s)
				while x < Behemoth_number:
					#Make behemoth instance
					mobs[x] = Behemoth()
					#Reduce minimum hp by half so the max is 400, and not 800
					mobs[x].hp = 200
					#Randomize stats of monster
					mobs[x] = randomize_enemy_stats(mobs[x])
					#Generates a position
					mobs[x].pos = all_pos[randint(0, len(all_pos)-1)]
					#Get position of that monster
					mob_pos = mobs[x].pos
					#Draw in the character
					space[mob_pos[1]][mob_pos[0]] = mobs[x].char

					x += 1 #Onto next Behemoth

			#Otherwise, a room not for Behemoths
			else:
				#Sees if we'll have monsters in the next room
				if roll_for_monster_filled_room():
					#Gives back all of positions that can be used
					# and also the mobs that have been modified
					all_pos, mobs = generate_monsters(space, floor, obj, mobs)

					#Draws out the enemies
					for index in mobs:
						#Get position of monster
						mob_pos = mobs[index].pos
						#Draw in monster
						space[mob_pos[1]][mob_pos[0]] = mobs[index].char

					#The new objects
					obj_dict = generate_chests(all_pos, space, obj, mobs, obj_dict)

					#Draws the chests
					for index in obj_dict:
						#Gets position of the chest
						chest_pos = obj_dict[index].pos
						#Draws the current chest
						space[chest_pos[1]][chest_pos[0]] = obj_dict[index].char

				#Mobless room
				else:
					#Randomly generate mobs
					obj_dict = generate_lonely_chest(space, mobs, obj_dict, obj)

					#Draws the chests
					for index in obj_dict:
						#Gets position of the chest
						chest_pos = obj_dict[index].pos
						#Draws the current chest
						space[chest_pos[1]][chest_pos[0]] = obj_dict[index].char


					#The positions that the Vendor and Priest can use
					positions_for_else = gen_spots_for_preist_and_vendor(space, mobs, obj_dict, obj)

					#If a merchant is spawned, and there is enough room
					# for a merchant instance.. then spawn one
					if randint(0, 2) == 0 and len(positions_for_else) > 0:
						#Make a vendor instance
						obj_dict[len(obj_dict)] = Vendor()
						#Randomly select a space for the merchant to be at
						obj_dict[len(obj_dict)-1].pos = positions_for_else[rand(0, len(positions_for_else)-1)]

						#These are all of the points we will filter out..
						#those being spots around the vendor, or used by the vendor
						exclude_spaces = all_spaces_around_item(obj_dict[len(obj_dict)-1].pos) + [obj_dict[len(obj_dict)-1].pos]

						#Draw in the merchant
						POS_FOR_MERCH = obj_dict[len(obj_dict)-1].pos
						space[POS_FOR_MERCH[1]][POS_FOR_MERCH[0]] = obj_dict[len(obj_dict)-1].char


					#If the Priest spawns, and there are spaces for
					# the priest to occupy, let the priest spawn
					elif randint(1, 3)==1 and len(positions_for_else) > 0:
						#Make a priest instance
						obj_dict[len(obj_dict)] = Priest()
						#Randomly selects a spot for the priest
						obj_dict[len(obj_dict)-1].pos = positions_for_else[rand(0, len(positions_for_else)-1)]

						POS_FOR_PRIEST = obj_dict[len(obj_dict)-1].pos
						#Draw in the priest
						space[POS_FOR_PRIEST[1]][POS_FOR_PRIEST[0]] = obj_dict[len(obj_dict)-1].char

		#Start up everything
		return new_pos, space, floor, mobs, obj_dict, dialog, skip_ai, False, addTime

	#Skip turn of the ai
	else:
		return obj.pos, space, floor, mobs, obj_dict, dialog, True, exit, add_time

	#Replace previous tile w/ period
	space[obj.pos[1]][obj.pos[0]] = "."
	#Spawn chacacter on next tile
	space[new_pos[1]][new_pos[0]] = symbol 

	return tuple(new_pos), space, floor, mobs, obj_dict, dialog, skip_ai, exit,add_time

#Checks if the two values in a list are positive
both_pos = lambda lst: True if lst[0] > 0 and lst[1] > 0 else False

#If one of the values is a 'priority', return True
priority_value = lambda lst: True if lst[0]==0 or lst[1]==0 and lst[0]!=lst[1] else False

#Takes the position of the player, and the position of an enemy,
# and returns the position around the player w/ the shortest
# distance between the player and the enemy.
# >>> y_pos == Player, z_pos == position of enemy, space == current room <<<
def short_distance_2Player(y_pos, z_pos, space):
	#All of the points around the player (LEFT OF, ABOVE, BELOW, RIGHT OF)
	x = spaces_around_player(y_pos)

	#If the enemy is in one of the 'attack zones'
	for value in x:
		if value == z_pos:
			return (z_pos, (0,0))

	#Only use spaces around the player that are not occupied
	x_prime = [y for y in x if space[y[1]][y[0]] == "."]

	#Monster can't move- all positions are taken up
	if len(x_prime) == 0:
		return (z_pos, (0,0))

	#Gets (basically vectors) between enemy and player
	x_prime_prime = [(y[0]-z_pos[0], y[1]-z_pos[1]) for y in x_prime]

	results = {} #Holds results
	i = 0
	for thing in x_prime_prime: #Binds results to 'vectors'
		results[thing] = (x_prime[i], thing)
		i += 1
	
	#If 1 (or 2) values has 1 or 2 zeros for the vectors, 
	# then they are a 'priority' (shortest distances)
	if Or(map(priority_value, x_prime_prime)):
		#List of 'priority values'
		values = [x for x in x_prime_prime if priority_value(x)]

		#There is only one priority value.. then return it
		if len(values) == 1:
			return results[values[0]]

		#if there are two though- randly pick between the two
		elif len(values) == 2:
			#randomly pick the first or second value
			return results[values[randint(0,1)]]

	#Returns the result
	return results[sorted(x_prime_prime)[0]]

#Returns the character corresponding to what direction
# the monster should move in (if blocked by an object downards)
def mov_down_around_obj(mob_pos, space):
	#If the monster is walking into an object, and there is a wall to the
	# left of the monster, then move to the right
	if floor_below(mob_pos, space) and wall_left(mob_pos, space) and not wall_right(mob_pos, space):
		return 'd' #Move right

	#If the monster is blocked from below, and they cannot move right, 
	# then they will move one space to the left
	elif floor_below(mob_pos, space) and not wall_left(mob_pos, space) and wall_right(mob_pos,space):
		return 'a' #Move left

	#Otherwise, monster isn't blocked, move down
	elif not floor_below(mob_pos, space):
		return 's' #Move down

	#Otherwise-- if is blocked, and they can move in either direction,
	# randomly pick between up or down
	return {0:'a',1:'d'}.get(rand(0,1))

#Returns character corresponding to movement
# taking into consideration if the monster is blocked by something
def mov_up_around_obj(mob_pos, space):
	#If the mob is blocked from above, and they cannot move right, but can 
	# move right, then the monster will move to the left
	if ceiling_above(mob_pos, space) and not wall_left(mob_pos, space) and wall_right(mob_pos, space):
		return 'a'

	#If the mob is blocked from above, and they cannot move left, but
	# can move right, then the monster will move to the right
	elif ceiling_above(mob_pos, space) and wall_left(mob_pos, space) and not wall_left(mob_pos, space):
		return 'd'

	#if we aren't blocked, move up
	elif not ceiling_above(mob_pos, space):
		return 'w'

	#Otherwise, we are blocked, and we can move lef or right
	# then randomly pick between the two
	return {0:'a',1:'d'}.get(rand(0,1))

#Returns character for the monster to move in (the direction)
# takes into consideration if it needs to go around something
def mov_left_around_obj(mob_pos, space):
	#If the monster is moving to the left (and is blocked)
	# and is blocked from below, then move up
	if wall_left(mob_pos,space) and not ceiling_above(mob_pos, space) and floor_below(mob_pos,space):
		return 'w'

	#If the monster is moving to the left and is blocked,
	# and they cannot move up, then move down
	elif wall_left(mob_pos,space) and ceiling_above(mob_pos,space) and not floor_below(mob_pos, space):
		return 's'

	#Otherwise, not blocked, move left
	elif not wall_left(mob_pos, space):
		return 'a'

	#Otherwise, we are blocked and can move left or right,
	# then randomly pick between the two
	return {0:'w',1:'s'}.get(rand(0,1))

#Returns character of directional movement, if blocked,
# this makes the monster TRY to go around obsticle
def move_right_around_obj(mob_pos, space):
	#If the monster is blocked from moving right, and they can move up
	# then the monster will move up to continue
	if wall_right(mob_pos,space) and not ceiling_above(mob_pos,space) and floor_below(mob_pos,space):
		return 'w'

	#If the monster is blocked from moving right, and they can
	# move down, then it will move down to continue chase
	elif wall_right(mob_pos,space) and ceiling_above(mob_pos,space) and not floor_below(mob_pos,space):
		return 's'

	#Otherwise, the monster can move without being blocked
	elif not wall_right(mob_pos, space):
		return 'd'

	#If the monster is blocked, and can move up or down
	# then randomly pick between the two directions
	return {0:'w', 1:'s'}.get(rand(0,rand(1,2)), (lambda: 'w' if randint(0,1)==0 else 's')())

#Returns a character W/A/S/D for the direction in which the AI
# will move one of the enemies (toward player)
def mov_direction(user_pos, enemy_pos, space):
	#gets target spot, as well as 'vertex' function
	target, vertex = short_distance_2Player(user_pos, enemy_pos, space)
	#Get inverse of Y (so it translates)
	vertex = (vertex[0], -vertex[1])

	positive = lambda n: True if n > 0 else False

	x = y = 0 #X,Y coordinates after we're done

	#Deal with the x-coordinate
	if vertex[0] > 0 or vertex[0] < 0:
		#If moving to the right
		if vertex[0] > 0:
			x = 1
		#Moving left
		else:
			x = -1

	#Deal with the y-coordinate
	if vertex[1] > 0 or vertex[1] < 0:
		#If moving down
		if vertex[1] > 0:
			y = 1
		#If moving up
		else:
			y = -1

	#Use the new x,y coordinates for movement
	new_vertex = (x,y)

	#If the creature doesn't move at all
	if new_vertex[0] == new_vertex[1] and new_vertex[1] == 0:
		return '~' #The character movement (nothing)

	#If we move along Y-axis
	elif new_vertex[0] == 0 and new_vertex[1] != 0:

		#If the number is positive (move down)
		if new_vertex[1] < 0:
			#Return the character that the monster should move in
			# (takes into consideration if mob is being blocked)
			return mov_down_around_obj(enemy_pos, space)

		#If instead we are going up
		elif new_vertex[1] > 0:
			#Get character for movement (on if we move up, or around object)
			return mov_up_around_obj(enemy_pos, space)

	#If we move along X-axis
	elif new_vertex[0] != 0 and new_vertex[1] == 0:

		#If we are moving to the right (positive)
		if positive(new_vertex[0]):
			#Gives directional movement of monster,
			#If blocked, tries to get around obsticle
			return move_right_around_obj(enemy_pos, space)

		#If we are moving left (negative)
		elif not positive(new_vertex[0]) and new_vertex[0] != 0:
			#Gives character of directional movement,
			# if blocked, tries to go around object
			return mov_left_around_obj(enemy_pos, space)

	#Otherwise- randomly choose between the two
	# If both are not 0
	use_x = randint(0, 1) #50 / 50 chance if we move along x-axis

	#Move along X-axis
	if use_x:
		#If we are moving to the right (positive)
		if positive(new_vertex[0]):
			#Gives directional input for monster,
			#If blocked, tries to get around monster
			return move_right_around_obj(enemy_pos, space)

		#If we are moving left (negative)
		elif not positive(new_vertex[0]) and new_vertex[0] != 0:
			#Gives left directional movement, unless blocked.
			# In which case, it attempts to go around obsticle
			return mov_left_around_obj(enemy_pos, space)

	#Move along Y-axis
	else:
		#If the number is positive (move down)
		if positive(new_vertex[1]):
			#Moves mob down, or around an object blocking it
			return mov_down_around_obj(enemy_pos, space)

		#If instead we are going up
		elif not positive(new_vertex[1]) and new_vertex[1] != 0:
			#Get character of movement, also chooses if they need 
			# to move around some blocking object
			return mov_up_around_obj(enemy_pos, space)
