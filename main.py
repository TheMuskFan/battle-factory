from pokemon import Pokemon
from battle import Battle
from moves import moves
import random
from tkinter import Tk
from ui import BattleFactoryApp

# Load Pokémon and moves
import json

with open("pokemon_data.json", "r") as file:
    rental_pool = json.load(file)

# Initialize Pokémon
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

# Start the Tkinter application
root = Tk()
battle = Battle(player_team, opponent_team)
app = BattleFactoryApp(root, battle)
root.mainloop()