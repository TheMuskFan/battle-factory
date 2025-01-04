# main.py
from pokemon import Pokemon
from moves import Move
from battle import Battle
import random

# Load Pokémon and moves
import json

with open("pokemon_data.json", "r") as file:
    rental_pool = json.load(file)

# Initialize Pokémon and moves
def create_pokemon(data):
    return Pokemon(
        name=data["name"],
        types=data["type"],
        hp=data["hp"],
        attack=data["attack"],
        defense=data["defense"],
        special_attack=data["special_attack"],
        special_defense=data["special_defense"],
        moves=data["moves"],
    )

pokemon_pool = [create_pokemon(p) for p in rental_pool]

# Team selection
player_team = random.sample(pokemon_pool, 3)
opponent_team = random.sample(pokemon_pool, 3)

# Display teams
print("Your Team:")
for p in player_team:
    print(f"- {p.name} ({', '.join(p.types)})")

print("\nOpponent Team:")
for p in opponent_team:
    print(f"- {p.name} ({', '.join(p.types)})")

# Start a battle
battle = Battle(player_team, opponent_team)
battle.battle_turn(player_team[0], opponent_team[0])