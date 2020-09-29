from constants import text_style
import random

class Player:
    """
    Class for the player character. There should only be one instance at a time!
    """
    def __init__(self, game, init_loc, init_items=[]):
        self.game = game
        self.loc = init_loc
        self.prev_loc = None
        self.items = init_items
        self.health = 10
        self.strength = 10
        self.accuracy = .9
        self.evasion = .2
        self.status = "normal"
        self.load = sum(i.weight for i in self.items)
        self.max_load = 10

    def light_check(self):
        """
        Returns true if the current room is lit, false if it isn't
        """
        light_source = False
        for i in self.items:
            try:
                if i.lit: light_source = True
            except:
                pass
        for i in self.loc.items:
            try:
                if i.lit: light_source = True
            except:
                pass
        return light_source

    def move(self, dir):
        """
        Moves the player and prints
        """
        if hasattr(self.loc, f"{dir}_to"):
            dest = getattr(self.loc, f"{dir}_to")
            self.prev_loc = self.loc
            self.loc = dest[0]
            self.game.screen.print(f"{dest[1]}\n")
            return True
        else:
            self.game.screen.print(text_style['error']("ERROR: MOVEMENT NOT ALLOWED\n"))
            return False

    def get_item(self, item):
        if item in self.loc.items:
            result = self.loc.remove_item(item)
            if result:
                if self.load + item.weight > self.max_load:
                    self.game.screen.print(f"Your pack is too full for the {item.name}.\n")
                    return False
                else:
                    self.items.append(item)
                    self.load += item.weight
                    self.game.screen.print(f"You pick up the {item.name}.\n")
                    item.on_pick_up()
                    return True
            else:
                return False
        else:
            self.game.screen.print("There's nothing here by that name.\n")
            return False

    def drop_item(self, item, quiet=False):
        if item in self.items:
            if self.loc.no_drop:
                self.game.screen.print("You don't think that's a good idea here.\n")
                return False
            self.items.remove(item)
            if quiet == False:
                self.game.screen.print(f"You set down the {item.name}.\n")
            self.load -= item.weight
            self.loc.add_item(item)
            return True
        else:
            self.game.screen.print("You don't have one of those in your inventory\n")
            return False
    
    def use_item(self, item, target):
        if item in self.items:
            return item.use(target)
        
        elif item in self.loc.items:
            return item.use_from_env(target)
                
        else:
            self.game.screen.print("There's nothing here by that name.\n")
            return False
    
    def attack_mob(self, weapon, target):
        target.attitude = "hostile"
        self.game.screen.print(random.choice(weapon.attack_text) + "\n")
        attack_chance = self.accuracy * weapon.accuracy
        dodge_chance = target.evasion
        if random.random() < attack_chance * (1 - dodge_chance):
            self.game.screen.print(f"{random.choice(target.text['dodge_fail'])}\n")
        else:
            target.health -= (self.strength / 10 ) * weapon.damage
            if target.health > 0:
                self.game.screen.print(f"{random.choice(target.text['dodge_success'])}\n")
            else:
                self.game.screen.print(random.choice(target.text["dead"]) + "\n")
                target.kill()

    def eat_item(self, item):
        if item in self.items:
            return item.eat(self)
        
        elif item in self.loc.items:
            return item.eat(self.loc)
                
        else:
            self.game.screen.print("There's nothing here by that name.\n")
            return False