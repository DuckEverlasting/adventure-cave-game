class Item:
    """
    Base item class
    """
    def __init__(self, screen, name, long_name, desc, weight=None, tags=[]):
        self.screen = screen
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
        self.screen.print(f"You don't see a way to use the {self.name}.\n")
        return False
    
    def use_from_env(self):
        """
        Default behavior for the "use" command if the item is in the room, but not in inventory. Overwrite to specify.
        """
        if "obtainable" in self.tags:
            self.screen.print("Try picking it up first.\n")
            return False
        else:
            self.screen.print("You can't use that.\n")
            return False
    
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
            self.screen.print(f"You wolf down the {self.name}. Yum.\n")
            self.on_eat()
            container.items.remove(self)
            return True
        elif "corpse" in self.tags:
            self.screen.print("What? No. That's just... no.\n\nGross.\n")
            return False
        else:
            self.screen.print(f"That's... not food.\n")
            return False

class Light_Source(Item):
    """
    Subclass for items that provide light
    """
    def __init__(self, screen, name, long_name, desc, weight=None, lit=False, tags=[]):
        super().__init__(screen, name, long_name, desc, weight, tags)
        self.lit = lit
        self.tags = tags + ["light_source"]

class Weapon(Item):
    """
    Subclass for items that can be used as weapons
    """
    def __init__(self, screen, name, long_name, desc, stats, attack_text, weight=None, tags=[]):
        super().__init__(screen, name, long_name, desc, weight, tags)
        self.damage = stats["damage"]
        self.accuracy = stats["accuracy"]
        self.attack_text = attack_text
        self.tags = tags + ["weapon"]
