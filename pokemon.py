class Pokemon:
    def __init__(self, name, types, hp, attack, defense, special_attack, special_defense, moves):
        self.name = name
        self.types = types
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.moves = moves

    def is_fainted(self):
        return self.hp <= 0

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def reset_hp(self):
        self.hp = self.max_hp