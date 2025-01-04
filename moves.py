import json

class Move:  # Change class name from Moves to Move
    def __init__(self, name, move_type, power, category, accuracy):
        self.name = name
        self.type = move_type
        self.power = power
        self.category = category
        self.accuracy = accuracy

    def __repr__(self):
        return f"Move({self.name}, {self.type}, {self.power}, {self.category}, {self.accuracy})"

def load_moves(filepath="moves.json"):
    """
    Load moves from a JSON file and convert them to Move instances.
    """
    with open(filepath, "r") as file:
        raw_moves = json.load(file)
    return {
        name: Move(name, details["type"], details["power"], details["category"], details["accuracy"])
        for name, details in raw_moves.items()
    }

# Load all moves at runtime
moves = load_moves()
