class Room:
    def __init__(self, slug, name, desc, dark=False, dark_desc="", no_mobs=False, no_drop=False, init_items=[]):
        self.slug = slug
        self.name = name
        self.desc = desc
        self.dark = dark
        self.dark_desc = dark_desc
        self.no_mobs = no_mobs
        self.no_drop = no_drop
        self.items = init_items

    def __str__(self):
        return self.name

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            if "obtainable" in item.tags:
                self.items.remove(item)
                return True
            else:
                item.screen.print("You decide to leave it there.\n")
                return False
        else:
            return False