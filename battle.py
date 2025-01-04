import random
from type_chart import get_type_multiplier
from moves import Move, moves
from pokemon import Pokemon

class Battle:
    def __init__(self, player_team: list[Pokemon], opponent_team: list[Pokemon]):
        self.player_team = player_team
        self.opponent_team = opponent_team

    def calculate_damage(self, attacker: Pokemon, defender: Pokemon, move):
        type_multiplier = get_type_multiplier(move.type, defender.types)
        stab = 1.5 if move.type in attacker.types else 1.0
        is_critical = random.random() < 0.0625
        critical_multiplier = 2.0 if is_critical else 1.0
        randomness = random.uniform(0.85, 1.0)

        if move.category == "Physical":
            attack_stat = attacker.attack
            defense_stat = defender.defense
        else:
            attack_stat = attacker.special_attack
            defense_stat = defender.special_defense

        damage = (
            ((2 * 50 / 5 + 2) * move.power * (attack_stat / defense_stat) / 50 + 2)
            * type_multiplier
            * stab
            * critical_multiplier
            * randomness
        )

        if is_critical:
            print("A critical hit!")
        if type_multiplier > 1:
            print("It's super effective!")
        elif type_multiplier < 1:
            print("It's not very effective...")

        return max(int(damage), 1)

    def battle_turn(self, player_pokemon: Pokemon, opponent_pokemon: Pokemon):
        print(f"\nBattle Start: {player_pokemon.name} vs {opponent_pokemon.name}!")

        while player_pokemon.hp > 0 and opponent_pokemon.hp > 0:
            # Player's turn
            print(f"\nYour turn! {player_pokemon.name}'s HP: {player_pokemon.hp}, {opponent_pokemon.name}'s HP: {opponent_pokemon.hp}")
            print(f"Moves for {player_pokemon.name}: {[move for move in player_pokemon.moves]}")

            move_name = input("Choose a move: ").strip()
            move = moves.get(move_name)
            if not move:
                print("Invalid move! Try again.")
                continue

            damage = self.calculate_damage(player_pokemon, opponent_pokemon, move)
            print(f"{player_pokemon.name} used {move.name}!")
            opponent_pokemon.hp -= damage
            opponent_pokemon.hp = max(opponent_pokemon.hp, 0)
            print(f"{opponent_pokemon.name} took {damage} damage! Remaining HP: {opponent_pokemon.hp}")

            if opponent_pokemon.hp == 0:
                print(f"{opponent_pokemon.name} fainted!")
                break

            # Opponent's turn (AI)
            print(f"\nOpponent's turn! {opponent_pokemon.name}'s HP: {opponent_pokemon.hp}, {player_pokemon.name}'s HP: {player_pokemon.hp}")
            ai_move_name = random.choice(opponent_pokemon.moves)
            ai_move = moves.get(ai_move_name)
            if not ai_move:
                print(f"AI failed to select a valid move: {ai_move_name}")
                continue

            damage = self.calculate_damage(opponent_pokemon, player_pokemon, ai_move)
            print(f"{opponent_pokemon.name} used {ai_move.name}!")
            player_pokemon.hp -= damage
            player_pokemon.hp = max(player_pokemon.hp, 0)
            print(f"{player_pokemon.name} took {damage} damage! Remaining HP: {player_pokemon.hp}")

            if player_pokemon.hp == 0:
                print(f"{player_pokemon.name} fainted!")
                break
