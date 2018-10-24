def DownwardDescent():
	#Get the things needed to make the main menu
	from tools import clear, pause, Getch
	from Story_mode import STORY #Story mode
	from Endless_mode import ENDLESS #Endless mode
	from tools import check_highscore_saves #Check if save / highscore files exist

	title ="""
 ____    _____   __    __   __   __   __    __   _____   ____   ____
|  _ \  |  _  | |  |  |  | |  \ |  | |  |  |  | |  _  | |    | |  _ \\
| | \ \ | | | | |  |  |  | |   \|  | |  |  |  | | |_| | | |  | | | \ \\
| | | | | | | | |  |__|  | |       | |  |__|  | |  _  | |   /  | | | |
| |_/ / | |_| | |   __   | |  |\   | |   __   | | | | | |   \  | |_/ /
|____/  |_____| |__/  \__| |__| \__| |__/  \__| |_| |_| |_|\_\ |____/
 ____    _____   ____      ____    _____   __   __   __________
|  _ \  |  ___| /  __\    / __ \  |  ___| |  \ |  | |          |
| | \ \ | |__   \  \__   / /  \_\ | |__   |   \|  | |___    ___|
| | | | |  __|   \___ \  | |   _  |  __|  |       |     |  |
| |_/ / | |___    ___\ \ \ \__/ / | |___  |  |\   |     |  |
|____/  |_____|  \_____/  \____/  |_____| |__| \__|     |__|
	"""
	#border = "====================================================================="
	option = "" #Option for game

	#Makes sure that highscore file and save file exists
	check_highscore_saves()

	while True:
		clear()
		#print(title) #Print title
		#print(border) #Print border

		print(" _________________________________")
		print("| \"Downward Descent\"")
		print("|_________________________________")
		print("| Exit: Press escape\n|")
		print("| Story mode: Press Q")
		print("| Endless mode: Press E")
		print("| In-depth Information: Press I")
		print("| Version: Press D")
		print("|_________________________________")

		try:
			option = Getch()
		except:
			#Keep from explosion
			option = ""

		#Exit the program
		if option == "\x1b":
			print("\nPress anything to quit")
			pause()
			raise SystemExit

		#Show user the information about what version this is
		elif option.lower() == "d":
			print("Version: 1.2")
			print("Developed by: Alastar S.")
			print("\nFound a bug? Please contact me (with the email below)")
			print("with a screen-shot of the error message (if there is one),")
			print("as well as a description of what caused the error (if you remember).")
			print("\nOtherwise, have any questions, complaints, or suggestions?")
			print("Email me at: lettherebebasic@gmail.com")
			pause()

		#Run the story mode
		elif option.lower() == "q":
			clear() #Clear screen before starrtin story mode
			STORY()

		#Run the endless mode
		elif option.lower() == "e":
			clear() #Clear screen before endless mode startss
			ENDLESS()

		#Makes a text document giving information about the game
		elif option.lower() == "i":
			#Lines for the file
			lines = [
			"IN DEPTH INFORMATION ABOUT DOWNWARD DESCENT",
			"===========================================",
			"",
			"Section 1: Controls",
			"______________________",
			" Movement:",
			"  W -> Up",
			"  A -> Left",
			"  S -> Down",
			"  D -> Right",
			"",
			" Help: H",
			"  When playing the game, and not in a menu.",
			"  You can press the 'h' key for the help menu.",
			"  The help menu gives (generally) the same information",
			"  that is being given here, but not in as much depth."
			"",
			" Exit: Escape key",
			"  This is fairly straight forward.. If you are in a menu,",
			"  it exits out of the menu. If you are in the main menu, it",
			"  stops the program in its entirety. Amazing right?"
			"",
			" Interact: E",
			"  When pressing the 'E' key when beside a ",
			"  (P)riest, chest, or (M)erchant, you will",
			"  interact with them. For a chest this means",
			"  looking through whatever 'goodies' might be",
			"  contained within. But for (M)erchants, it allows",
			"  you to sell or buy items. For (P)riests, you can",
			"  get talked AT, or be healed if your health is below 100.",
			"",
			" Attack: Q",
			"  When you press the 'Q' key, and are directly",
			"  beside an enemy, you will attack it (ot attempt to)!",
			"  Below the 'display' of the room, some dialog should appear",
			"  which will tell you if you hit any sort of monster around you.",
			"  But of course, you can miss! So the dialog will also tell you",
			"  if your attack failed to hit your foe.",
			"",
			" Inventory: I",
			"  You can access your inventory with the 'I' key. Please",
			"  note that you can only access your inventory if you are",
			"  not already inside of any other sort of menu. Here's a ",
			"  quick tip to new players, whenever you get to a new menu,",
			"  always look at the top, for there are usually some 'simple'",
			"  bits of text which tell you what keys do what inside of the menu.",
			"  An example would be how pressing the 'F' key when inside of your",
			"  inventory allows you to use any health potions that you have.",
			"",
			" Descend a floor: Enter",
			"  When there are no more monsters on your floor, you may press the",
			"  'enter' key to descent a floor. The player (the '@' sign) will",
			"  always be spawned as close to the middle of the room as possible.",
			"",
			" Save options: P",
			"  During 'Endless mode' you can save your game by bringing up the",
			"  save menu with the 'P' key. Here, the game gives you options to",
			"  Save (your game), Load (a saved game) and Delete (a saved game).",
			"  Please note that at any given moment, you only have 5 save slots!",
			"  Also remember that this 'mechanic' only works when in the endless mode!",
			"",
			"",
			"Section 2: Enemies",
			"______________________",
			"These are the following monsters:",
			"",
			" Character             Name",
			"___________      ________________",
			"    Z                 Zombie",
			"    K                   Ker",
			"    N                  Nymph",
			"    M                 Minotaur",
			"    B                 Behemoth",
			"",
			"",
			"Section 3: NPC's",
			"__________________",
			"",
			" Character            Name",
			"___________        __________",
			"     P               Priest",
			"     S               Mechant",
			"",
			"Section 4: Objects",
			"___________________",
			" Walls:",
			"  Walls are represented by 3 different",
			"  characters inside of Downward Descent:",
			"    |",
			"    _",
			"    -",
			"   Are all of the 'different' walls.",
			"",
			" Unoccupied space: .",
			"  Any, and all unused (open space) in the game",
			"  is represented with periods ('.'). So any spot",
			"  that you as the player can move to, will be any",
			"  spot that has a period on it!",
			"",
			" Chests: #",
			"  Inside of the game, all chests are represented",
			"  with the '#' (hash) symbol. When your player is",
			"  standing right beside one, you can look through it",
			"  by pressing 'E'.",
			"",
			"",
			"Section 5: Game modes",
			"_______________________",
			" Story Mode:",
			"  In the 'story mode', you start on floor 128, and",
			"  are supposed to go down to floor 1. Prepare yourself,",
			"  as you'll have to fight a Behemoth at the bottom!",
			"  During story mode, the only type of.. any sort of story",
			"  mostly comes from Priests (when they talk at you), and the",
			"  ending of the game.. Which honestly isn't that grand.",
			"",
			" Endless Mode",
			"  Unlike Story Mode, you start on floor 1 and work your way up",
			"  floor by floor.. until you die. This mode (if you hadn't guessed)",
			"  is ENDLESS. The only way the game stops is by either quitting, or",
			"  by dying. The objective of this game mode, however, is to live as",
			"  long as possible, and to acquire as much gold as possible!",
			"  When you die, you get a score, and if you get the High score, it gets",
			"  saved in a file, then EVERYONE ELSE gets to try to beat YOUR SCORE!",
			"  This is personally my favorite mode.",
			]
			#Get ready to write the file
			m = open('DownwardDescent_Information.txt', 'w')
			#Write all of the lines
			for line in lines:
				m.write(line+"\n")
			m.close()

DownwardDescent() #Run game