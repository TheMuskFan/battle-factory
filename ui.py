import tkinter as tk
from tkinter import messagebox
from battle import Battle
from pokemon import Pokemon
from moves import moves
import json
import random

def load_pokemon_data(filepath="pokemon_data.json"):
    """
    Load Pokémon data from a JSON file and convert them to Pokemon instances.
    """
    with open(filepath, "r") as file:
        raw_pokemon = json.load(file)

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

    return [create_pokemon(p) for p in raw_pokemon]


class BattleFactoryApp:
    def __init__(self, root, battle):
        self.root = root
        self.battle = battle
        self.current_player_pokemon = self.battle.player_team[0]
        self.current_opponent_pokemon = self.battle.opponent_team[0]

        # Add `max_hp` attributes to Pokémon
        for pokemon in self.battle.player_team + self.battle.opponent_team:
            pokemon.max_hp = pokemon.hp

        # Set up window
        self.root.title("Battle Factory")
        self.create_widgets()

    def create_widgets(self):
        # Player Pokémon details
        self.player_frame = tk.Frame(self.root)
        self.player_frame.pack(pady=10)

        self.player_label = tk.Label(self.player_frame, text=f"Your Pokémon: {self.current_player_pokemon.name}")
        self.player_label.pack()

        self.player_hp_bar = tk.Canvas(self.player_frame, width=200, height=20, bg="gray")
        self.player_hp_bar.pack()
        self.update_hp_bar(self.player_hp_bar, self.current_player_pokemon.hp, self.current_player_pokemon.max_hp)

        # Opponent Pokémon details
        self.opponent_frame = tk.Frame(self.root)
        self.opponent_frame.pack(pady=10)

        self.opponent_label = tk.Label(self.opponent_frame, text=f"Opponent: {self.current_opponent_pokemon.name}")
        self.opponent_label.pack()

        self.opponent_hp_bar = tk.Canvas(self.opponent_frame, width=200, height=20, bg="gray")
        self.opponent_hp_bar.pack()
        self.update_hp_bar(self.opponent_hp_bar, self.current_opponent_pokemon.hp, self.current_opponent_pokemon.max_hp)

        # Moves
        self.moves_frame = tk.Frame(self.root)
        self.moves_frame.pack(pady=20)

        self.move_buttons = []
        for move in self.current_player_pokemon.moves:
            btn = tk.Button(self.moves_frame, text=move, command=lambda m=move: self.use_move(m))
            btn.pack(side=tk.LEFT, padx=5)
            self.move_buttons.append(btn)

    def update_hp_bar(self, canvas, current_hp, max_hp):
        """
        Updates the HP bar on the given canvas.
        """
        canvas.delete("hp_bar")  # Clear previous bar
        hp_percentage = current_hp / max_hp
        hp_width = int(200 * hp_percentage)  # Max width = 200
        color = "green" if hp_percentage > 0.5 else "yellow" if hp_percentage > 0.2 else "red"
        canvas.create_rectangle(0, 0, hp_width, 20, fill=color, tags="hp_bar")

    def use_move(self, move_name):
        # Player's turn
        move = moves[move_name]
        damage = self.battle.calculate_damage(
            self.current_player_pokemon,
            self.current_opponent_pokemon,
            move
        )
        self.current_opponent_pokemon.hp -= damage
        self.current_opponent_pokemon.hp = max(0, self.current_opponent_pokemon.hp)

        self.update_hp_bar(self.opponent_hp_bar, self.current_opponent_pokemon.hp, self.current_opponent_pokemon.max_hp)

        if self.current_opponent_pokemon.hp <= 0:
            messagebox.showinfo("Victory", f"{self.current_opponent_pokemon.name} fainted!")
            if not self.switch_opponent():
                return

        # Opponent's turn
        ai_move_name = random.choice(self.current_opponent_pokemon.moves)
        ai_move = moves[ai_move_name]
        damage = self.battle.calculate_damage(
            self.current_opponent_pokemon,
            self.current_player_pokemon,
            ai_move
        )
        self.current_player_pokemon.hp -= damage
        self.current_player_pokemon.hp = max(0, self.current_player_pokemon.hp)

        self.update_hp_bar(self.player_hp_bar, self.current_player_pokemon.hp, self.current_player_pokemon.max_hp)

        if self.current_player_pokemon.hp <= 0:
            messagebox.showinfo("Defeat", f"{self.current_player_pokemon.name} fainted!")
            if not self.switch_player():
                return

        self.update_ui()

    def update_ui(self):
        """
        Update all UI elements to reflect the current state.
        """
        self.player_label.config(text=f"Your Pokémon: {self.current_player_pokemon.name}")
        self.opponent_label.config(text=f"Opponent: {self.current_opponent_pokemon.name}")

        # Update HP bars
        self.update_hp_bar(self.player_hp_bar, self.current_player_pokemon.hp, self.current_player_pokemon.max_hp)
        self.update_hp_bar(self.opponent_hp_bar, self.current_opponent_pokemon.hp, self.current_opponent_pokemon.max_hp)
    
    def switch_opponent(self):
        """
        Switch to the next opponent Pokemon if available.
        """

        self.battle.opponent_team = [p for p in self.battle.opponent_team if p.hp > 0]
        if not self.battle.opponent_team:
            messagebox.showinfo("Game Over", "You won the battle!")
            self.root.quit()
            return False
        self.current_opponent_pokemon = self.battle.opponent_team[0]
        self.update_ui()
        self.update_move_buttons() # Refresh move buttons for the incoming pokemon 
        return True
    
    def switch_player(self):
        """
        Switch to the next available player Pokemon if the current one faints

        Returns:
            bool: True if a Pokemon was succesfully switched, False if no Pokemon are left 
        """

        #Filter out fainted Pokemon
        self.battle.player_team = [p for p in self.battle.player_team if p.hp > 0]

        if not self.battle.player_team:
            # No pokemon left, player loses the battle
            messagebox.showinfo("Game Over", "You lost the battle!") 
            self.root.quit() # Exit the game
            return False
        
        # Switch to the next Pokemon 
        self.current_player_pokemon = self.battle.player_team[0]
        self.update_ui()
        self.update_move_buttons() # Refresh move buttons for the incoming pokemon 
        return True
    
    def update_move_buttons(self):
        """
        Refresh the move buttons to match the current Pokemon's moves.
        """
        # Clear existing buttons 
        for btn in self.move_buttons:
            btn.destroy()
        self.move_buttons = []

        # Create new buttons for the current Pokemon's moves
        for move in self.current_player_pokemon.moves:
            btn = tk.Button(self.moves_frame,text=move,command=lambda m=move: self.use_move(m))
            btn.pack(side=tk.LEFT, padx=5)
            self.move_buttons.append(btn)





# Example: Initialize battle
if __name__ == "__main__":
    pokemon_pool = load_pokemon_data("pokemon_data.json")
    player_team = random.sample(pokemon_pool, 3)
    opponent_team = random.sample(pokemon_pool, 3)

    battle = Battle(player_team, opponent_team)
    root = tk.Tk()
    app = BattleFactoryApp(root, battle)
    root.mainloop()


