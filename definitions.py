from room import Room
from player import Player
from item import Item, LightSource, Weapon
from mob import Mob
from action import Action
from action_run import run
from constants import text_style


def create(game):
    """
    Sets game objects at initial state and returns them.
    """
    # Declare the actions
    action = {
        "attack": Action(
            name="attack",
            grammar={
                "d_obj_required": True,
                "preps_accepted": ("with", "using"),
            },
            run=run["attack"]
        ),
        "die": Action(
            name="die",
            grammar={
                "d_obj_prohibited": True,
                "i_obj_prohibited": True,
            },
            run=run["die"]
        ),
        "drop": Action(
            name="drop",
            grammar={
                "d_obj_required": True,
                "i_obj_prohibited": True,
            },
            run=run["drop"]
        ),
        "eat": Action(
            name="eat",
            grammar={
                "d_obj_required": True,
                "i_obj_prohibited": True,
            },
            run=run["eat"]
        ),
        "get": Action(
            name="get",
            grammar={
                "d_obj_required": True,
                "i_obj_prohibited": True,
            },
            run=run["get"]
        ),
        "go": Action(
            name="go",
            grammar={
                "adv_required": True,
            },
            run=run["go"]
        ),
        "help": Action(
            name="help",
            grammar={
                "d_obj_prohibited": True,
                "i_obj_prohibited": True,
            },
            run=run["help"]
        ),
        "inventory": Action(
            name="inventory",
            grammar={
                "d_obj_prohibited": True,
                "i_obj_prohibited": True,
            },
            run=run["inventory"]
        ),
        "load": Action(
            name="load",
            grammar={
                "d_obj_prohibited": True,
                "i_obj_prohibited": True,
            },
            run=run["load"]
        ),
        "look": Action(
            name="look",
            grammar={
                "d_obj_prohibited": True,
                "preps_accepted": ("at", "in", "into", "inside", "beneath", "underneath", "under", "below",)
            },
            run=run["look"]
        ),
        "quit": Action(
            name="quit",
            grammar={
                "d_obj_prohibited": True,
                "i_obj_prohibited": True,
            },
            run=run["quit"]
        ),
        "save": Action(
            name="save",
            grammar={
                "d_obj_prohibited": True,
                "i_obj_prohibited": True,
            },
            run=run["save"]
        ),
        "talk": Action(
            name="talk",
            grammar={
                "d_obj_prohibited": True,
                "i_obj_required": True,
                "preps_accepted": ("to", "with", "at",)
            },
            run=run["talk"]
        ),
        "use": Action(
            name="use",
            grammar={
                "d_obj_required": True,
                "preps_accepted": ("with", "on",)
            },
            run=run["use"]
        ),
        "wait": Action(
            name="wait",
            grammar={},
            run=run["wait"]
        ),
    }

    # Declare the items
    item = {
        "fists": Weapon(
            game=game,
            name=text_style['item']("fists"),
            long_name=f"your {text_style['item']('fists')}",
            desc=None,
            stats={
                "damage": 1,
                "accuracy": 0.9
            },
            attack_text=(
                f"You pretend you're a boxer and attempt a left hook with your {text_style['item']('fists')}.",
                f"You leap forward, putting your {text_style['item']('fists')} in front of you in the hope that they "
                f"do some damage.",
                f"You swing your {text_style['item']('fists')} around in your best imitation of a helicopter."
            ),
            tags=["obtainable"]
        ),
        "knife": Weapon(
            game=game,
            name=text_style['item']("knife"),
            long_name=f"a {text_style['item']('knife')}",
            desc=text_style['desc'](
                "It's a knife. Like for cutting your steak with, except designed for steak that is actively trying to "
                "kill you. "
            ),
            weight=2,
            stats={
                "damage": 2,
                "accuracy": 0.95
            },
            attack_text=(
                f"Gripping your {text_style['item']('knife')} in a {text_style['item']('knife')}-like manner, you "
                f"stab with the stabby part.",
                f"You slash forward with your {text_style['item']('knife')}, praying for a hit.",
            ),
            tags=["obtainable"]
        ),
        "sword": Weapon(
            game=game,
            name=text_style['item']("sword"),
            long_name=f"a {text_style['item']('sword')}",
            desc=text_style['desc'](
                "This sword has seen better days, but it's probably got one or two good swings left in it."
            ),
            weight=3,
            stats={
                "damage": 3,
                "accuracy": 0.8
            },
            attack_text=(
                f"You swing wildly with your {text_style['item']('sword')}.",
            ),
            tags=["obtainable"]
        ),
        "lantern": LightSource(
            game=game,
            name=text_style['item']("lantern"),
            long_name=f"an extinguished {text_style['item']('lantern')}",
            desc=text_style['desc'](
                "The lantern is unlit. It has fuel though; you imagine you could get it lit if you had some matches."
            ),
            weight=1,
            tags=["obtainable"]
        ),
        "amulet_of_yendor": Item(
            game=game,
            name=text_style['item']("Amulet of Yendor"),
            long_name=f"the {text_style['item']('Amulet of Yendor')}",
            desc=text_style['desc'](
                "This amulet is said to contain unimaginable power."
            ),
            weight=0.5,
            tags=["obtainable"]
        ),
        "cheese": Item(
            game=game,
            name=text_style['item']("cheese"),
            long_name=f"a hunk of {text_style['item']('cheese')}",
            desc=text_style['desc'](
                "It is a hunk of cheese. Looks all right."
            ),
            weight=0.25,
            tags=["obtainable", "food"]
        ),
        "goblin_corpse": Item(
            game=game,
            name=text_style['item']("goblin corpse"),
            long_name=f"a {text_style['item']('goblin corpse')}",
            desc=text_style['desc'](
                f"It's a dead goblin. You turn it over, looking for valuables, but all you can find is "
                f"a\\crumpled {text_style['item_in_desc']('matchbook')}, which falls to the floor next to the corpse. "
            ),
            tags=["corpse"]
        ),
        "lever": Item(
            game=game,
            name=text_style['item']("lever"),
            long_name=f"a {text_style['item']('lever')} jutting from the cliff side",
            desc=text_style['desc'](
                "It looks close enough to reach. Your fingers twitch. You never could resist a good lever."
            )
        ),
        "matchbook": Item(
            game=game,
            name=text_style['item']("matchbook"),
            long_name=f"a {text_style['item']('matchbook')}",
            desc=text_style['desc'](
                "At first glance, the crumpled matchbook appears to be empty, but looking closer,\\you see it still "
                "has a few matches inside. "
            ),
            weight=0.1,
            tags=["obtainable"]
        ),
        "rope": Item(
            game=game,
            name=text_style['item']("rope"),
            long_name=f"some {text_style['item']('rope')}",
            desc=text_style['desc']("Good, sturdy rope, about 50 feet long."),
            weight=2,
            tags=["obtainable"]
        ),
    }

    # Declare the rooms
    room = {
        "outside": Room(
            game=game,
            slug="outside",
            name="Outside Cave Entrance",
            desc=text_style['desc'](
                f"{text_style['dir_in_desc']('North')} of you, the cave mouth beckons."
            ),
            no_mobs=True,
        ),
        "foyer": Room(
            game=game,
            slug="foyer",
            name="Foyer",
            desc=text_style['desc'](
                f"Dim light filters in from the {text_style['dir_in_desc']('south')}. Dusty passages "
                f"run {text_style['dir_in_desc']('north')} and {text_style['dir_in_desc']('east')}."
            ),
            init_items=[item["sword"]],
        ),
        "overlook": Room(
            game=game,
            slug="overlook",
            name="Grand Overlook",
            desc=text_style['desc'](
                f"A steep cliff appears before you, falling into the darkness. Ahead to the "
                f"{text_style['dir_in_desc']('north')}, a light\\flickers in the distance, but there is no way across "
                f"the chasm. A passage leads {text_style['dir_in_desc']('south')},\\away from the cliff."
            ),
            init_items=[item["rope"]],
        ),
        "narrow": Room(
            game=game,
            slug="narrow",
            name="Narrow Passage",
            desc=text_style['desc'](
                f"The narrow passage bends here from {text_style['dir_in_desc']('west')} to "
                f"{text_style['dir_in_desc']('north')}. The smell of gold permeates the air."
            ),
        ),
        "treasure": Room(
            game=game,
            slug="treasure",
            name="Treasure Chamber",
            desc=text_style['desc'](
                f"You've found the long-lost treasure chamber! Sadly, it has already been completely emptied "
                f"by\\earlier adventurers. The only exit is to the {text_style['dir_in_desc']('south')}."
            ),
            init_items=[item["lantern"]],
        ),
        "chasm": Room(
            game=game,
            slug="chasm",
            name="Over The Edge",
            desc=text_style['desc'](
                f"You find yourself suspended over a dark chasm, at the end of a rope that was clearly not\\long "
                f"enough for this job. Glancing about, you see a {text_style['item_in_desc']('lever')} jutting out "
                f"from the wall, half hidden.\\The rope leads back {text_style['dir_in_desc']('up')}."
            ),
            dark=True,
            dark_desc=text_style['desc'](
                f"You find yourself suspended over a dark chasm, at the end of a rope that was clearly not\\long "
                f"enough for this job. It is dark. You can't see a thing. You are likely to be eaten by a grue.\\The "
                f"rope leads back {text_style['dir_in_desc']('up')}."
            ),
            no_mobs=True,
            no_drop=True,
            init_items=[item["lever"]]
        ),
        "final": Room(
            game=game,
            slug="final",
            name="Across the Chasm",
            desc=text_style['desc'](
                f"You find a small, elaborately decorated room. Sunlight streams down a hole in the ceiling "
                f"high\\above you, illuminating an altar upon which sits the fabled "
                f"{text_style['item_in_desc']('Amulet of Yendor')}.\\To the {text_style['dir_in_desc']('south')}, a "
                f"bridge leads back the way you came."
            ),
            init_items=[item["amulet_of_yendor"]]
        ),
    }

    # Declare the mobs
    mob = {
        "goblin": Mob(
            game=game,
            name=text_style['mob']("goblin"),
            long_name=f"a {text_style['mob']('goblin')}",
            desc=text_style['desc'](
                f"The {text_style['mob_in_desc']('goblin')} is eyeing you warily and shuffling his weight from one "
                f"foot to the other.\\A crude knife dangles from his belt."
            ),
            text={
                "enter": (
                    f"A {text_style['mob']('goblin')} shuffles into the room. At the sight of you, he gives a squeal "
                    f"of surprise and bares his teeth.",
                ),
                "exit": (
                    f"The {text_style['mob']('goblin')} skitters out of the room, heading ",
                ),
                "idle": (
                    f"The {text_style['mob']('goblin')} grumbles nervously about how crowded the cave has "
                    f"gotten lately.",
                    f"The {text_style['mob']('goblin')} pulls out a knife, then thinks better of it and puts "
                    f"the knife back.",
                    f"The {text_style['mob']('goblin')} is momentarily transfixed by a rash on his elbow.",
                ),
                "dodge_success": (
                    f"The {text_style['mob']('goblin')} leaps back, emotionally scarred by your violent outburst "
                    f"but physically unharmed.",
                ),
                "dodge_fail": (
                    f"The {text_style['mob']('goblin')} staggers back, wounded physically (and emotionally).",
                ),
                "dead": (
                    f"The {text_style['mob']('goblin')} cries out in shock as your attack connects. He gives you a "
                    f"baleful glare that fades into\\a look of weary resignation as he slumps to the ground, dead.",
                ),
                "attack_success": (
                    f"The {text_style['mob']('goblin')} whips its knife out towards you in a desperate arc. It carves "
                    f"into you.",
                ),
                "attack_fail": (
                    f"The {text_style['mob']('goblin')} whips its knife out towards you in a desperate arc. You dodge "
                    f"nimbly out of the way.",
                ),
                "kill_player": (
                    f"The {text_style['mob']('goblin')} screams at you and flies forward, plunging its knife into "
                    f"your chest. You final thought,\\improbably, is a silent prayer that the "
                    f"{text_style['mob']('goblin')}'s filthy knife doesn't give you an infection.",
                )
            },
            stats={
                "health": 10,
                "damage": 2,
                "accuracy": .75,
                "evasion": .15
            },
            init_loc=room["foyer"],
            init_att="neutral",
            items=([item["goblin_corpse"]])
        )
    }

    # Declare the player
    player = Player(game=game, init_loc=room["outside"], init_items=[item["cheese"]])

    # Link rooms together
    room["outside"].n_to = (room["foyer"], "You step into the mouth of the cave.")
    room["foyer"].s_to = (room["outside"], "You head south, and find yourself outside the cave.")
    room["foyer"].n_to = (
        room["overlook"],
        "You make your way north, and the cave opens up suddenly, revealing a vast chasm before you."
    )
    room["foyer"].e_to = (
        room["narrow"],
        "You take the eastern passage. It grows narrower until you have a hard time standing straight."
    )
    room["overlook"].s_to = (room["foyer"], "You step back from the cliff's edge and head south.")
    room["overlook"].n_to = (
        room["overlook"],
        "You take a step back, and get ready to jump over the gap. Then you realize that is "
        f"an\\incredibly stupid idea, and decide you would rather live."
    )
    room["narrow"].w_to = (room["foyer"], "You move west through the cramped passage until it opens up a bit.")
    room["narrow"].n_to = (room["treasure"], "You follow your nose and head north.")
    room["treasure"].s_to = (room["narrow"], "You head south into the narrow passage.")
    room["chasm"].u_to = (
        room["overlook"],
        "You climb slowly back up the rope, and pull yourself back onto the overlook, panting."
    )
    room["final"].s_to = (room["overlook"], "You go back across the bridge, resisting the pull of the amulet.")

    # Add functionality to items

    # sword
    def use_sword():
        if player.loc.no_drop:
            player.game.display.print(
                f"This isn't a great place to mess around with your {text_style['item']('sword')}. You leave it be.")
            return False
        else:
            player.game.display.print(
                f"You swing the {text_style['item']('sword')} around wildly. After a few wide arcs, it slips out of "
                f"your fingers and clatters to the ground.\\"
            )
            player.drop_item(item["sword"], quiet=True)

        return True

    item["sword"].use = use_sword

    # rope
    def use_rope():
        if player.loc == room["overlook"]:
            player.game.display.print(
                f"You tie off one end of the {text_style['item']('rope')} to a convenient stalagmite "
                f"and drop the rest off the cliff.\\"
            )

            # remove from inventory
            player.drop_item(item["rope"], quiet=True)

            # modify the room
            room["overlook"].desc = text_style['desc'](
                f"A steep cliff appears before you, falling into the darkness. Ahead to the "
                f"{text_style['dir_in_desc']('north')}, a light\\flickers in the distance, but there is no way "
                f"across the chasm. A passage leads {text_style['dir_in_desc']('south')},\\away from the cliff. A "
                f"tied off rope offers a way {text_style['dir_in_desc']('down')}."
            )
            room["overlook"].d_to = (
                room["chasm"],
                "You climb down the rope, and make it about a third of the way\\down the cliff before you reach "
                f"the end of the line. Oh dear.",
            )

            # modify the item
            item["rope"].long_name = f"a tied off length of {text_style['item']('rope')}"
            item["rope"].desc = text_style['desc'](
                "The rope looks pretty sturdy. It will probably hold your weight. Probably."
            )
            item["rope"].tags.remove("obtainable")

            def use_from_env_rope():
                player.move("d")
                return True

            item["rope"].use_from_env = use_from_env_rope

        else:
            player.game.display.print(
                f"You try to use the {text_style['item']('rope')} as a lasso, and fail miserably."
            )

        return True

    item["rope"].use = use_rope

    # lantern
    def use_lantern():
        if item["matchbook"] in player.items:
            if item["lantern"].lit:
                player.game.display.print(f"The lantern is already lit.\\")
                return False
            else:
                item["lantern"].lit = True
                item["lantern"].long_name = f"a lit {text_style['item']('lantern')}"
                item["lantern"].desc = f"The {text_style['item']('lantern')} is giving off a warm glow."
                player.game.display.print(f"You strike a match and light the lantern. The room brightens.\\")
                return True
        else:
            player.game.display.print("You don't have anything to light it with.")
            return False

    item["lantern"].use = use_lantern

    # matchbook
    def use_matchbook():
        if item["lantern"] in player.items:
            if item["lantern"].lit:
                player.game.display.print(f"The lantern is already lit.\\")
                return False
            else:
                item["lantern"].lit = True
                player.game.display.print(f"You strike a match and light the lantern. The room brightens.\\")
                return True
        else:
            player.game.display.print("You don't have anything you want to light on fire.\\")
            return False

    item["matchbook"].use = use_matchbook

    # goblin_corpse
    def on_look_goblin_corpse():
        item["goblin_corpse"].desc = "It's a dead goblin. You don't want to touch it again."
        player.loc.add_item(item["matchbook"])
        delattr(item["goblin_corpse"], "on_look")

    item["goblin_corpse"].on_look = on_look_goblin_corpse

    # lever
    def use_from_env_lever():
        if player.light_check():
            player.game.display.print(
                "You pull the lever. A loud rinding noise echoes through the chasm. You nearly lose your grip "
                f"but\\manage to hold on as a bridge lowers from the ceiling of the cave, shuddering into place\\above "
                f"you. Looks like you can cross the chasm now. What are the odds that lever would be in this "
                f"exact\\place on the cliff side?\\"
            )
            room["overlook"].desc = text_style['desc'](
                f"A steep cliff appears before you, falling into the darkness. Ahead to the "
                f"{text_style['dir_in_desc']('north')}, a narrow bridge\\has been lowered, leading to a light "
                f"flickering in the distance. A passage leads {text_style['dir_in_desc']('south')}, away from the "
                f"cliff.\\A tied off rope offers a way {text_style['dir_in_desc']('down')}."
            )
            room["overlook"].n_to = (
                room["final"],
                "You carefully walk across the bridge, heading towards the light on the other side."
            )
            return True
        else:
            player.game.display.print(
                f"It's too dark for that right now. Also, how do you know about "
                f"the {text_style['item']('lever')}, cheater?\\"
            )
            return False

    item["lever"].use_from_env = use_from_env_lever

    return {
        "item": item,
        "room": room,
        "mob": mob,
        "player": player,
        "action": action
    }
