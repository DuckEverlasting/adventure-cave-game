class Room:
    def __init__(self, game, slug, name, desc, dark=False, dark_desc="", no_mobs=False, no_drop=False, init_items=None):
        if init_items is None:
            init_items = []
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.u_to = None
        self.d_to = None
        self.game = game
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
                self.game.display.print_list("You decide to leave it there.\n")
                return False
        else:
            return False
