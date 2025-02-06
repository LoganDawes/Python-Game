'''Portfolio Project: Developing a short turn-based video game in Python'''

'''Importing a custom-made module that displays text by letter instead of all at once'''
import text_display as td

'''
Defining classes to be used in the game, including variables of many different data types and methods that can be performed by each class.
'''

# Player class
class Player:
	def __init__(self) -> None:
		self.name = ""
		self.HP = 100
		self.SP = 25
		self.MaxHP = 100
		self.MaxSP = 25
		self.attack = 10
		self.defense = 0
		self.tmpdefense = 0
		self.experience = 0
		self.exp_to_next_level = 100
		self.level = 1
		self.items = []

	# Attack method
	def attack_enemy(self, enemy):
		td.text_display(f"\nYou attacked {enemy.name}!\n")
		inflict_damage(self, enemy, 1)
		if enemy.HP > 0:
			td.text_display(f"{enemy.name} HP: {Color.PURPLE}{enemy.HP}{Color.END}\n")
		else:
			td.text_display(f"{enemy.name} has been defeated!\n")

	# Special attack method
	def special_attack(self, enemy):
		td.text_display(f"\nYou used special attack on {enemy.name}!\n")
		inflict_damage(self, enemy, 1.5)
		self.SP -= 5
		if enemy.HP > 0:
			td.text_display(f"{enemy.name} HP: {Color.PURPLE}{enemy.HP}{Color.END}\n")
		else:
			td.text_display(f"{enemy.name} has been defeated!\n")

	# Defend method
	def defend(self):
		td.text_display("\nYou defended yourself!\n")
		self.tmpdefense = 3

	# Add item to player inventory
	def add_item(self, item):
		self.items.append(item)

	# Use item in battle
	def use_item(self, item_index):
		if item_index < len(self.items):
			item = self.items.pop(item_index)
			item.use(self)
		else:
			td.text_display("\nInvalid item number.\n")

# Enemy class
class Enemy:
	def __init__(self, name, description, HP=10, attack=1, defense=0, exp_reward=0):
		self.name = name
		self.description = description
		self.HP = HP
		self.MaxHP = HP
		self.attack = attack
		self.defense = defense
		self.tmpdefense = 0
		self.exp_reward = exp_reward

	# Attack method for enemy
	def attack_player(self, player):
		td.text_display(f"\n {self.name} attacked you!\n")
		inflict_damage(self, player, 1)

	def respawn(self):
		self.HP = self.MaxHP

# Item class
class Item:
	def __init__(self, name, description, hp_restore=0, sp_restore=0):
		self.name = name
		self.description = description
		self.hp_restore = hp_restore
		self.sp_restore = sp_restore

	# Use item method
	def use(self, player):
		# Health restore calculation
		if self.hp_restore > 0:
			current_hp = player.HP
			max_hp = player.MaxHP
			if current_hp < max_hp:
				restore_amount = min(self.hp_restore, max_hp - current_hp)
				player.HP += restore_amount
				td.text_display(f"\nUsed {self.name}!\n")
				td.text_display(f"Restored {Color.PURPLE}{restore_amount}{Color.END} HP\n")
			else:
				td.text_display(f"\nYour HP is already full!\n")

		# Special restore calculation
		if self.sp_restore > 0:
			current_sp = player.SP
			max_sp = player.MaxSP
			if current_sp < max_sp:
				restore_amount = min(self.sp_restore, max_sp - current_sp)
				player.SP += restore_amount
				td.text_display(f"\nUsed {self.name}!\n")
				td.text_display(f"Restored {Color.YELLOW}{restore_amount}{Color.END} SP\n")
			else:
				td.text_display(f"\nYour SP is already full!\n")


'''Defining a class that simplifies ANSI color codes'''
# Colored Text Class
class Color:
	PURPLE = '\033[95m'
	CYAN = '\033[96m'
	DARKCYAN = '\033[36m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'

'''Function that starts a gameplay loop with the player and a list of enemies'''
# Start enemy encounter
def start_encounter(player, enemies):
	td.text_display(f"You've encountered {' and '.join([enemy.name for enemy in enemies])}!\n")
	# Turn based gameplay loop
	while player.HP > 0 and any(enemy.HP > 0 for enemy in enemies):
			player_turn(player, enemies)
			if any(enemy.HP > 0 for enemy in enemies):
				enemy_turn(player, enemies)

	# End of battle
	if player.HP <= 0:
		td.text_display(f"{Color.RED}Game Over - You have been defeated.{Color.END}")
	elif all(enemy.HP <= 0 for enemy in enemies):
		td.text_display(f"{Color.GREEN}You defeated all enemies!\n{Color.END}")
		total_experience = 0

		# Calculate total experience
		for enemy in enemies:
			total_experience += enemy.exp_reward
		td.text_display(f"{Color.GREEN}{total_experience} experience gained!\n{Color.END}")
		player.experience += total_experience
		td.text_display(f"{Color.GREEN}EXP: {player.experience} / {player.exp_to_next_level}\n{Color.END}")

		# Level up
		while player.experience >= player.exp_to_next_level:
			level_up(player)
			td.text_display(f"\n{Color.GREEN}EXP: {player.experience} / {player.exp_to_next_level}\n{Color.END}")

# Player level up
def level_up(player):
	# Subtract level requirement
	player.experience -= player.exp_to_next_level
	# Increase level
	player.level += 1
	# Set next level requirement
	player.exp_to_next_level = int(player.exp_to_next_level * 1.25)
	
	td.text_display(f"{Color.GREEN}Level up! You are now level {player.level}{Color.END}\n")
	td.text_display(f"Max HP:\t{Color.PURPLE}{player.MaxHP} > {player.MaxHP + 10}{Color.END}\n")
	td.text_display(f"Max SP:\t{Color.YELLOW}{player.MaxSP} > {player.MaxSP + 5}{Color.END}\n")
	td.text_display(f"ATK:\t{Color.RED}{player.attack} > {player.attack + 1}{Color.END}\n")

	# Increase stats
	player.MaxHP += 10
	player.MaxSP += 5
	player.attack += 1
	player.HP = player.MaxHP
	player.SP = player.MaxSP

'''Functions that define the actions taken on the player or enemies turn'''

# Actions on player's turn
def player_turn(player, enemies):
	player.tmpdefense = 0
	while True:
		print("\n------------------------------")
		# Display player stats and actions
		player_stat_menu(player)
		td.text_display("1. Attack")
		td.text_display("2. Special Attack")
		td.text_display("3. Defend")
		td.text_display("4. Item")
		td.text_display("5. Check")
		
		# Accept player input
		td.text_display("Enter your action: ")
		player_choice = input("> ")
		
		# Check player input
		print("\n------------------------------")

		# Filter living enemies
		living_enemies = [enemy for enemy in enemies if enemy.HP > 0]
		
		# Attack choice
		if player_choice == "1":
			if len(living_enemies) == 1:
				player.attack_enemy(living_enemies[0])
				break
			else:
				td.text_display("\nChoose an enemy to attack:\n")
				# Display enemy options
				for i, enemy in enumerate(living_enemies):
					if enemy.HP > 0:
						td.text_display(f"{i + 1}. {enemy.name} (HP: {Color.PURPLE}{enemy.HP}{Color.END})\n")
				# Accept player input
				td.text_display("Enter enemy number: ")
				enemy_choice = input("> ")
				try:
					enemy_index = int(enemy_choice) - 1
					if 0 <= enemy_index < len(living_enemies):
						player.attack_enemy(living_enemies[enemy_index])
						break
					else:
						td.text_display("\nInvalid enemy number.\n")
				except ValueError:
					td.text_display("\nInvalid input.\n")

		# Special attack choice
		elif player_choice == "2":
			if player.SP >= 5:
				if len(living_enemies) == 1:
					player.special_attack(living_enemies[0])
					break
				else:
					td.text_display("\nChoose an enemy to attack:\n")
					# Display enemy options
					for i, enemy in enumerate(living_enemies):
						if enemy.HP > 0:
							td.text_display(f"{i + 1}. {enemy.name} (HP: {Color.PURPLE}{enemy.HP}{Color.END})\n")
					# Accept player input
					td.text_display("Enter enemy number: ")
					enemy_choice = input("> ")
					try:
						enemy_index = int(enemy_choice) - 1
						if 0 <= enemy_index < len(living_enemies):
							player.special_attack(living_enemies[enemy_index])
							break
						else:
							td.text_display("\nInvalid enemy number.\n")
					except ValueError:
						td.text_display("\nInvalid input.\n")
			else:
				td.text_display("\nInsufficient SP!\n")
			
		# Defend choice
		elif player_choice == "3":
			player.defend()
			break
			
		# Item choice
		elif player_choice == "4":
			if player.items:
				td.text_display("\nChoose an item to use:\n")
				# Display player's items
				for i, item in enumerate(player.items):
					td.text_display(f"{i + 1}. {item.name} - {item.description}\n")

				td.text_display("Enter item number (0 to cancel): ")
				item_choice = input("> ")
				
				# Check item choice
				try:
					item_index = int(item_choice) - 1
					if 0 <= item_index < len(player.items):
						player.use_item(item_index)
						break
					elif item_index == -1:
						td.text_display("\nCancelled.\n")
					else:
						td.text_display("\nInvalid item number.\n")
				except ValueError:
					td.text_display("\nInvalid input.\n")
			else:
				td.text_display("\nNo items in inventory.\n")

		# Check enemy choice
		elif player_choice == "5":
			if len(living_enemies) == 1:
				enemy_stat_menu(living_enemies[0])
			else:
				td.text_display("\nChoose an enemy to check:\n")
				# Display enemy options
				for i, enemy in enumerate(living_enemies):
					td.text_display(f"{i + 1}. {enemy.name} (HP: {Color.PURPLE}{enemy.HP}{Color.END})\n")
				# Accept player input
				td.text_display("Enter enemy number: ")
				enemy_choice = input("> ")
				try:
					enemy_index = int(enemy_choice) - 1
					if 0 <= enemy_index < len(living_enemies):
						enemy_stat_menu(living_enemies[enemy_index])
					else:
						td.text_display("\nInvalid enemy number.\n")
				except ValueError:
					td.text_display("\nInvalid input.\n")

	  # Invalid choice
		else:
			td.text_display("\nInvalid input\n")

# Actions on enemy's turn
def enemy_turn(player, enemies):
	for enemy in enemies:
		if enemy.HP > 0:
			print("\n------------------------------")
			enemy.attack_player(player)
			if player.HP <= 0:
				break
	
'''Functions that display the player and enemy stats'''

# Display player stats
def player_stat_menu(player):
	td.text_display(f"\n{Color.UNDERLINE}{player.name}{Color.END} - Lvl.{player.level}")
	td.text_display(f"{Color.PURPLE}HP: \t{player.HP:.0f} / {player.MaxHP:.0f}{Color.END}")
	td.text_display(f"{Color.YELLOW}SP: \t{player.SP:.0f} / {player.MaxSP:.0f}{Color.END}")
	td.text_display(f"{Color.RED}ATK: \t{player.attack:.0f}{Color.END}")
	if player.defense > 0:
		td.text_display(f"{Color.BLUE}DEF: \t{player.defense:.0f}{Color.END} \n")
	print()

# Display enemy stats
def enemy_stat_menu(enemy):
	td.text_display(f"\n{Color.UNDERLINE}{enemy.name}{Color.END}")
	td.text_display(f"{enemy.description}")
	td.text_display(f"{Color.PURPLE}HP: \t{enemy.HP:.0f} / {enemy.MaxHP:.0f}{Color.END}")
	td.text_display(f"{Color.RED}ATK: \t{enemy.attack:.0f}{Color.END}")
	if enemy.defense > 0:
		td.text_display(f"{Color.BLUE}DEF: \t{enemy.defense:.0f}{Color.END} \n")

# Inflict damage
def inflict_damage(attacker, defender, mult):
	damage = int((attacker.attack * mult) - (defender.defense + defender.tmpdefense))
	damage = max(damage, 0) # Ensure damage is not negative
	defender.HP -= damage
	td.text_display(f"Dealt {Color.RED}{damage}{Color.END} damage!")

# Starting Game
def main():
	player = Player()

	# Naming Player
	td.text_display("Welcome, What is your name? ")
	player.name = input("> ")
	while len(player.name) > 20 or player.name == "":
		if len(player.name) > 20:
			td.text_display("Name is too long! Please enter a name with 20 characters or less.")
		else:
			td.text_display("Name can't be empty! Please enter a name.")
		player.name = input("> ")
	player.name = player.name[:20]
	td.text_display(f"Welcome, {player.name}!")

	# Initialize Items
	healing_potion = Item("Healing Potion", "Restores 20 HP", hp_restore=20)
	ether = Item("Ether", "Restores 10 SP", sp_restore=10)

	# Setup test battle
	player.add_item(healing_potion)
	player.add_item(ether)

	rat = Enemy("Rat", "Basic and weak enemy", 10, 2, 0, 20)
	knight1 = Enemy("Knight", "Valiant and strong knight", 20, 3, 1, 40)
	knight2 = Enemy("Knight", "Valiant and strong knight", 20, 3, 1, 40)

	start_encounter(player, [rat, knight1, knight2])

# Run main function
if __name__ == "__main__":
	main()