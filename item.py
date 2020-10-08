from constants import half_space


class Item:
    """
    Base item class
    """

    def __init__(self, slug, name, long_name, desc, weight=None, tags=None):
        if tags is None:
            tags = []
        self.slug = slug
        self.name = name
        self.long_name = long_name
        self.desc = desc
        self.weight = weight
        self.tags = tags

    def __str__(self):
        return self.name

    def use(self):
        """
        Default behavior for the "use" command. Overwrite to specify a use.
        """
        return {
            "print_text": f"You don't see a way to use the {self.name}." + half_space,
            "success": False
        }

    def use_from_env(self):
        """
        Default behavior for the "use" command if the item is in the room, but not in inventory. Overwrite to specify.
        """
        if "obtainable" in self.tags:
            return {
                "print_text": "Try picking it up first." + half_space,
                "success": False
            }
        else:
            return {
                "print_text": "You can't use that." + half_space,
                "success": False
            }

    def on_eat(self):
        """
        Effect to be triggered upon eating item. Overwrite to specify. (Default = no effect)
        """
        pass

    def on_look(self):
        """
        Effect to be triggered upon looking at item. Overwrite to specify. (Default = no effect)
        """
        pass

    def on_pick_up(self):
        """
        Effect to be triggered upon picking up item. Overwrite to specify. (Default = no effect)
        """
        pass

    def eat(self, container):
        """
        Handles the "eat" command for most items. Can overwrite to specify, of course.
        """
        if "food" in self.tags:
            self.on_eat()
            container.items.remove(self)
            return {
                "print_text": f"You wolf down the {self.name}. Yum." + half_space,
                "success": True
            }
        elif "corpse" in self.tags:
            return {
                "print_text": "What? No. That's just... no.\n\n" + half_space + "Gross." + half_space,
                "success": False
            }
        else:
            return {
                "print_text": "That's... not food." + half_space,
                "success": False
            }

    def get_data(self):
        pass

    def load_data(self):
        pass


class LightSource(Item):
    """
    Subclass for items that provide light
    """

    def __init__(self, slug, name, long_name, desc, lit=False, weight=None, tags=None):
        super().__init__(slug, name, long_name, desc, weight, tags)
        self.lit = lit
        self.tags += ["light_source"]


class Weapon(Item):
    """
    Subclass for items that can be used as weapons
    """

    def __init__(self, slug, name, long_name, desc, stats, attack_text, weight=None, tags=None):
        super().__init__(slug, name, long_name, desc, weight, tags)
        self.damage = stats["damage"]
        self.accuracy = stats["accuracy"]
        self.attack_text = attack_text
        self.tags += ["weapon"]
