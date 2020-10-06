import random
from constants import text_style, half_space


class Mob:
    def __init__(self, game, name, long_name, desc, text, stats, init_loc, init_att, items=None):
        if items is None:
            items = []
        self.game = game
        self.name = name
        self.long_name = long_name
        self.desc = desc
        self.text = text
        self.health = stats["health"]
        self.damage = stats["damage"]
        self.accuracy = stats["accuracy"]
        self.evasion = stats["evasion"]
        self.items = items
        self.status = "normal"
        self.loc = init_loc
        self.prev_loc = None
        self.attitude = init_att
        self.alive = True

    def __str__(self):
        return self.name

    def move(self, direction=None, room=None):
        if direction:
            try:
                destination = getattr(self.loc, f"{direction}_to")
                self.loc = destination[0]
            except AttributeError:
                pass

        elif room:
            if not room.no_mobs:
                self.loc = room
    
    def move_rand(self):
        directions = {
            "n_to": text_style['dir']("north"),
            "s_to": text_style['dir']("south"),
            "e_to": text_style['dir']("east"),
            "w_to": text_style['dir']("west")
        }

        if random.randint(0, 2) != 0:
            return False
        else:
            possible_moves = [i for i in (directions.keys()) if hasattr(self.loc, i)]
            dir_to = random.choice(possible_moves)
            # noinspection SpellCheckingInspection
            dest = getattr(self.loc, dir_to)
            self.prev_loc = self.loc
            self.loc = dest[0]
            return directions[dir_to]

    def attack_player(self, player):
        attack_chance = self.accuracy
        dodge_chance = player.evasion
        if random.random() < attack_chance * (1 - dodge_chance):
            self.game.display.print_text(random.choice(self.text['attack_fail']) + half_space)
        else:
            player.health -= self.damage
            if player.health > 0:
                self.game.display.print_text(random.choice(self.text['attack_success']) + half_space)
            else:
                self.game.display.print_text(random.choice(self.text["kill_player"]) + half_space)

    def on_look(self):
        pass

    def on_talk(self):
        self.game.display.print_text(f"The {self.name} lets forth a series on unintelligible grunts and yips, "
                                     f"and\n\nyou suddenly remember that you don't speak {self.name}." + half_space)

    def kill(self):
        for i in self.items:
            self.loc.add_item(i)
        self.alive = False
        self.loc = None
