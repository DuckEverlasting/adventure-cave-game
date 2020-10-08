from constants import text_style, half_space
import random


class Player:
    """
    Class for the player character. Location MUST be set before the game begins
    """

    def __init__(self):
        self.loc = None
        self.prev_loc = None
        self.items = []
        self.health = 10
        self.strength = 10
        self.accuracy = .9
        self.evasion = .2
        self.status = "normal"
        self.load = sum(i.weight for i in self.items)
        self.max_load = 10

    def export(self):
        return {
            "loc": self.loc.slug,
            "prev.loc": self.prev_loc.slug
        }

    def light_check(self):
        """
        Returns true if the current room is lit, false if it isn't
        """
        light_source = False
        for i in self.items:
            try:
                if i.lit:
                    light_source = True
            except AttributeError:
                pass
        for i in self.loc.items:
            try:
                if i.lit:
                    light_source = True
            except AttributeError:
                pass
        return light_source

    def move(self, direction):
        """
        Moves the player and prints
        """
        destination = None
        try:
            destination = getattr(self.loc, f"{direction}_to")
            self.prev_loc = self.loc
            self.loc = destination[0]
            return {
                "print_text": destination[1] + half_space,
                "success": True
            }
        except AttributeError:
            return {
                "print_text": text_style['error']("ERROR: MOVEMENT NOT ALLOWED" + half_space),
                "success": False
            }

    def get_item(self, item):
        if item in self.loc.items:
            result = self.loc.remove_item(item)
            if "success" in result and result["success"]:
                if self.load + item.weight > self.max_load:
                    return {
                        "print_text": f"Your pack is too full for the {item.name}." + half_space,
                        "success": False
                    }
                else:
                    self.items.append(item)
                    self.load += item.weight
                    item.on_pick_up()
                    return {
                        "print_text": f"You pick up the {item.name}." + half_space,
                        "success": False
                    }
            else:
                return result
        else:
            return {
                "print_text": "There's nothing here by that name." + half_space,
                "success": False
            }

    def drop_item(self, item, quiet=False):
        if item in self.items:
            if self.loc.no_drop:
                return {
                    "print_text": "You don't think that's a good idea here." + half_space,
                    "success": False
                }
            self.items.remove(item)
            self.load -= item.weight
            self.loc.add_item(item)
            return {
                "print_text": f"You set down the {item.name}." + half_space,
                "success": False
            } if not quiet else {
                "success": False
            }
        else:
            return {
                "print_text": "You don't have one of those in your inventory" + half_space,
                "success": False
            }

    def use_item(self, item, target):
        if item in self.items:
            return item.use(target)

        elif item in self.loc.items:
            return item.use_from_env(target)

        else:
            return {
                "print_text": "There's nothing here by that name." + half_space,
                "success": False
            }

    def attack_mob(self, weapon, target):
        target.attitude = "hostile"
        attack_text = random.choice(weapon.attack_text) + half_space
        attack_chance = self.accuracy * weapon.accuracy
        dodge_chance = target.evasion
        if random.random() < attack_chance * (1 - dodge_chance):
            return {
                "print_text": attack_text,
                "print_text_2": random.choice(target.text['dodge_fail']) + half_space
            }
        else:
            target.health -= (self.strength / 10) * weapon.damage
            if target.health > 0:
                return {
                    "print_text": attack_text,
                    "print_text_2": random.choice(target.text['dodge_success']) + half_space
                }
            else:
                target.kill()
                return {
                    "print_text": attack_text,
                    "print_text_2": random.choice(target.text["dead"]) + half_space
                }

    def eat_item(self, item):
        if item in self.items:
            return item.eat(self)

        elif item in self.loc.items:
            return item.eat(self.loc)

        else:
            return {
                "print_text": "There's nothing here by that name." + half_space,
                "success": False
            }
