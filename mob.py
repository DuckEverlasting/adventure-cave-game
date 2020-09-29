import random
from constants import text_style


class Mob:
    def __init__(self, screen, name, long_name, desc, text, stats, init_loc, init_att, items=[]):
        self.screen = screen
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

    def move(self, dir=None, room=None):
        if dir:
            if hasattr(self.loc, f"{dir}_to"):
                dest = getattr(self.loc, f"{dir}_to")
                self.loc = dest[0]
        elif room:
            if not room.no_mobs:
                self.loc = room
    
    def moveRand(self):
        directions = {
            "n_to": text_style['dir']("north"),
            "s_to": text_style['dir']("south"),
            "e_to": text_style['dir']("east"),
            "w_to": text_style['dir']("west")
        }

        if random.randint(0, 2) != 0:
            return False
        else:
            possibleMoves = [i for i in (directions.keys()) if hasattr(self.loc, i)]
            dir_to = random.choice(possibleMoves)
            dest = getattr(self.loc, dir_to)
            self.prev_loc = self.loc
            self.loc = dest[0]
            return directions[dir_to]

    def attack_player(self, player):
        attack_chance = self.accuracy
        dodge_chance = player.evasion
        if random.random() < attack_chance * (1 - dodge_chance):
            self.screen.print(f"{random.choice(self.text['attack_fail'])}\n")
        else:
            player.health -= self.damage
            if player.health > 0:
                self.screen.print(f"{random.choice(self.text['attack_success'])}\n")
            else:
                self.screen.print(random.choice(self.text["kill_player"]) + "\n")

    def on_look(self):
        pass

    def on_talk(self):
        self.screen.print(f"The {self.name} lets forth a series on unintelligible grunts and yips, and\nyou suddenly remember that you don't speak {self.name}.\n")

    def kill(self):
        for i in self.items:
            self.loc.add_item(i)
        self.alive = False
        self.loc = None
