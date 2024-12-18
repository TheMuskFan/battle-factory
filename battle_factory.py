import random 
import json 

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
def calculate_damage(attacker, defender, move_power):
   return int ((attacker["attack"] / defender["defense"]) * move_power)



def battle(player_pokemon, opponent_pokemon):
   print(f"\nBattle: {player_pokemon['name']} vs {opponent_pokemon['name']}!")
   
   while player_pokemon['hp'] > 0 and opponent_pokemon['hp'] > 0:
      # Player's turn
      print(f"\nYour Moves: {player_pokemon['moves']}")
      move = input("Choose a move: ").strip()
      damage = calculate_damage(player_pokemon, opponent_pokemon, 60)  # Simplified damage
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