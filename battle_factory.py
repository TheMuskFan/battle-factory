import random 
import json 
import type_chart

moves = {
    # Physical Moves
    "Earthquake": {"type": "Ground", "power": 100, "category": "Physical", "accuracy": 100},
    "Stone Edge": {"type": "Rock", "power": 100, "category": "Physical", "accuracy": 80},
    "Dragon Claw": {"type": "Dragon", "power": 80, "category": "Physical", "accuracy": 100},
    "Close Combat": {"type": "Fighting", "power": 120, "category": "Physical", "accuracy": 100},
    "Iron Tail": {"type": "Steel", "power": 100, "category": "Physical", "accuracy": 75},
    "Shadow Claw": {"type": "Ghost", "power": 70, "category": "Physical", "accuracy": 100},
    "Crunch": {"type": "Dark", "power": 80, "category": "Physical", "accuracy": 100},
    "Waterfall": {"type": "Water", "power": 80, "category": "Physical", "accuracy": 100},
    "Ice Punch": {"type": "Ice", "power": 75, "category": "Physical", "accuracy": 100},
    "Thunder Punch": {"type": "Electric", "power": 75, "category": "Physical", "accuracy": 100},
    "Body Slam": {"type": "Normal", "power": 85, "category": "Physical", "accuracy": 90},

    # Special Moves
    "Flamethrower": {"type": "Fire", "power": 90, "category": "Special", "accuracy": 100},
    "Thunderbolt": {"type": "Electric", "power": 90, "category": "Special", "accuracy": 100},
    "Ice Beam": {"type": "Ice", "power": 90, "category": "Special", "accuracy": 100},
    "Hydro Pump": {"type": "Water", "power": 110, "category": "Special", "accuracy": 80},
    "Psychic": {"type": "Psychic", "power": 90, "category": "Special", "accuracy": 100},
    "Shadow Ball": {"type": "Ghost", "power": 80, "category": "Special", "accuracy": 100},
    "Dragon Pulse": {"type": "Dragon", "power": 85, "category": "Special", "accuracy": 100},
    "Sludge Bomb": {"type": "Poison", "power": 90, "category": "Special", "accuracy": 100},
    "Energy Ball": {"type": "Grass", "power": 90, "category": "Special", "accuracy": 100},
    "Air Slash": {"type": "Flying", "power": 75, "category": "Special", "accuracy": 95},

}

# load pokemon data
with open("pokemon_data.json", "r") as file:
  rental_pool = json.load(file)

  # validation check
  print(f"Number of Pokémon in pool: {len(rental_pool)}")

# random team selection
def select_random_team(pool, size = 3):
  return random.sample(pool, size)

# select teams
player_team = select_random_team(rental_pool)
opponent_team = select_random_team(rental_pool)

# display teams
print("Your Team:")
for pokemon in player_team:
  print(f"- {pokemon['name']} ({', '.join(pokemon['type'])})")

print("\nOpponent Team:")
for pokemon in opponent_team:
    print(f"- {pokemon['name']} ({', '.join(pokemon['type'])})")

# battle functions

# This function calculates the damage to done to a Pokemon given the attacker, defender and move power
def calculate_damage(attacker, defender, move):
   """
   Calculates damage dealt to a defender by an attacker using a specific move.

   Paramteters: 
   - attacker: dict, the attacking Pokemon (includes stats and types)
   - defender: dict, the defending Pokémon (includes stats and type).
   - move: dict, the move being used (includes power, type, category).
    
    Returns:
    - int, the calculated damage.
   """

   # Extract move details
   move_type = move["type"]
   move_power = move["power"]
   move_category = move["category"] # Physical or Special 
   move_accuracy = move["accuracy"]  # Accuracy percentage (e.g., 100, 80)

   # Check for move accuracy
   if random.uniform(0, 100) > move_accuracy:
      print(f"{attacker['name']} missed!")
      return 0

   # Determine Relevant Stats
   if move_category == "Physical":
      attack_stat = attacker["attack"]
      defense_stat = defender["defense"]
   elif move_category == "Special":
      attack_stat = attacker["special_attack"]
      defense_stat = defender["special_defense"]
   else:
      return 0
   
   # Ensure defense is not zero to avoid division by zero
   defense_stat = max(defense_stat, 1)
   
   # Calculate type effectiveness
   type_multiplier = type_chart.get_type_multiplier(move_type, defender["type"])

   # If immune, no damage is dealt
   if type_multiplier == 0:
      print(f"{defender['name']} is immune to {move_type}!")
      return 0

   # Calculate STAB (Same Type Attack Bonus)
   stab = 1.5 if move_type in attacker["type"] else 1.0

   # Add critical hit chance
   is_critical = random.random() < 0.0625  # 6.25% chance
   critical_multiplier = 2.0 if is_critical else 1.0
   if is_critical:
        print(f"A critical hit!")

   # Add randomness for attack damage 
   randomness = random.uniform(0.85, 1.0)

   # Final damage formula
   damage = int(
      (attack_stat / defense_stat)
      * move_power
      * type_multiplier
      * stab
      * critical_multiplier
      * randomness
   )
   return max(damage, 1)  # Ensure at least 1 damage is dealt

def battle(player_pokemon, opponent_pokemon):
   print(f"\nBattle: {player_pokemon['name']} vs {opponent_pokemon['name']}!")
   
   while player_pokemon['hp'] > 0 and opponent_pokemon['hp'] > 0:
      # Player's turn
      print(f"\nYour Moves: {player_pokemon['moves']}")
      move = input("Choose a move: ").strip()

      damage = calculate_damage(player_pokemon, opponent_pokemon, move)  
      print(f"{player_pokemon['name']} used {move}!")
      opponent_pokemon['hp'] -= damage
      if opponent_pokemon['hp'] < 0:
         opponent_pokemon['hp'] = 0
      print(f"{opponent_pokemon['name']} took {damage} damage! Remaining HP: {opponent_pokemon['hp']}")

      # Opponent Pokemon fainted
      if opponent_pokemon['hp'] <= 0:
          print(f"{opponent_pokemon['name']} fainted!")
          break
      
       # AI Turn
      print(f"\nOpponent's Turn!")
      damage = calculate_damage(opponent_pokemon, player_pokemon, 60)
      player_pokemon['hp'] -= damage
      if player_pokemon['hp'] < 0:
         player_pokemon['hp'] = 0
      print(f"{player_pokemon['name']} took {damage} damage! Remaining HP: {player_pokemon['hp']}")

      # Player Pokemon fainted
      if player_pokemon['hp'] <= 0:
          print(f"{player_pokemon['name']} fainted!")
          break

# Step 4: Main Logic
player_team = select_random_team(rental_pool)
opponent_team = select_random_team(rental_pool)

print("\nYour Team:")
for pokemon in player_team:
    print(f"- {pokemon['name']} ({', '.join(pokemon['type'])})")

print("\nOpponent Team:")
for pokemon in opponent_team:
    print(f"- {pokemon['name']} ({', '.join(pokemon['type'])})")

# Example: Start a battle
battle(player_team[0], opponent_team[0])