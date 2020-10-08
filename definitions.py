from typing import Dict, List, Any, Union

from room import Room
from player import Player
from item import Item, LightSource, Weapon
from mob import Mob
from action import Action
from action_run import run
from constants import text_style

state: Dict[str, Union[Dict[Any, Any], List[Any], Player]] = {
    "item": {},
    "room": {},
    "mobs": [],
    "player": None,
    "action": {}
}


# sword
def use_sword():
    if state["player"].loc.no_drop:
        return {
            "print_text": f"This isn't a great place to mess around with your {text_style['item']('sword')}. "
                          "You leave it be.",
            "success": False
        }
    else:
        state["player"].drop_item(state["item"]["sword"], quiet=True)
        return {
            "print_text": f"You swing the {text_style['item']('sword')} around wildly. After a few wide arcs, "
                          f"it slips out of your fingers and clatters to the ground.\n\n",
            "success": True
        }


# rope
def use_rope():
    if state["player"].loc == state["room"]["overlook"]:
        print_text = f"You tie off one end of the {text_style['item']('rope')} to a convenient stalagmite and " \
                     f"drop the rest off the cliff.\n\n "

        # remove from inventory
        state["player"].drop_item(state["item"]["rope"], quiet=True)

        # modify the room
        state["room"]["overlook"].desc = text_style['desc'](
            f"A steep cliff appears before you, falling into the darkness. Ahead to the "
            f"{text_style['dir_in_desc']('north')}, a lightflickers in the distance, but there is no way "
            f"across the chasm. A passage leads {text_style['dir_in_desc']('south')},away from the cliff. A "
            f"tied off rope offers a way {text_style['dir_in_desc']('down')}."
        )
        state["room"]["overlook"].d_to = (
            state["room"]["chasm"],
            "You climb down the rope, and make it about a third of the waydown the cliff before you reach "
            f"the end of the line. Oh dear.",
        )

        # modify the item
        state["item"]["rope"].long_name = f"a tied off length of {text_style['item']('rope')}"
        state["item"]["rope"].desc = text_style['desc'](
            "The rope looks pretty sturdy. It will probably hold your weight. Probably."
        )
        state["item"]["rope"].tags.remove("obtainable")

        def use_from_env_rope():
            return state["player"].move("d")

        state["item"]["rope"].use_from_env = use_from_env_rope

    else:
        print_text = f"You try to use the {text_style['item']('rope')} as a lasso, and fail miserably."

    return {
        "print_text": print_text,
        "success": True
    }


# lantern
def use_lantern():
    if state["item"]["matchbook"] in state["player"].items:
        if state["item"]["lantern"].lit:
            return {
                "print_text": f"The lantern is already lit.\n\n",
                "success": False
            }
        else:
            state["item"]["lantern"].lit = True
            state["item"]["lantern"].long_name = f"a lit {text_style['item']('lantern')}"
            state["item"]["lantern"].desc = f"The {text_style['item']('lantern')} is giving off a warm glow."
            return {
                "print_text": f"You strike a match and light the lantern. The room brightens.\n\n",
                "success": True
            }
    else:
        return {
            "print_text": "You don't have anything to light it with.",
            "success": False
        }


# matchbook
def use_matchbook():
    if state["item"]["lantern"] in state["player"].items:
        if state["item"]["lantern"].lit:
            return {
                "print_text": f"The lantern is already lit.\n\n",
                "success": False
            }
        else:
            state["item"]["lantern"].lit = True
            state["item"]["lantern"].long_name = f"a lit {text_style['item']('lantern')}"
            state["item"]["lantern"].desc = f"The {text_style['item']('lantern')} is giving off a warm glow."
            return {
                "print_text": f"You strike a match and light the lantern. The room brightens.\n\n",
                "success": True
            }
    else:
        return {
            "print_text": "You don't have anything you want to light on fire.\n\n",
            "success": False
        }


# goblin_corpse
def on_look_goblin_corpse():
    state["item"]["goblin_corpse"].desc = "It's a dead goblin. You don't want to touch it again."
    state["player"].loc.add_item(state["item"]["matchbook"])
    delattr(state["item"]["goblin_corpse"], "on_look")


# lever
def use_from_env_lever():
    if state["player"].light_check():
        state["room"]["overlook"].desc = text_style['desc'](
            f"A steep cliff appears before you, falling into the darkness. Ahead to the "
            f"{text_style['dir_in_desc']('north')}, a narrow bridge has been lowered, leading to a light "
            f"flickering in the distance. A passage leads {text_style['dir_in_desc']('south')}, away from the "
            f"cliff. A tied off rope offers a way {text_style['dir_in_desc']('down')}."
        )
        state["room"]["overlook"].n_to = (
            state["room"]["final"],
            "You carefully walk across the bridge, heading towards the light on the other side."
        )
        return {
            "print_text": "You pull the lever. A loud rinding noise echoes through the chasm. You nearly lose "
                          "your grip but manage to hold on as a bridge lowers from the ceiling of the cave, "
                          "shuddering into place above you. Looks like you can cross the chasm now. What are the "
                          "odds that lever would be in this exact place on the cliff side?\n\n",
            "success": True
        }
    else:
        return {
            "print_text": f"It's too dark for that right now. Also, how do you know about "
                          f"the {text_style['item']('lever')}, cheater?\n\n",
            "success": False
        }


def create():
    """
    Sets game objects at initial state and returns them.
    """
    # Declare the player
    state["player"] = Player()

    # Declare the actions
    state["action"] = {
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
    state["item"] = {
        "fists": Weapon(
            slug="fists",
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
            slug="knife",
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
            slug="sword",
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
            slug="lantern",
            name=text_style['item']("lantern"),
            long_name=f"an extinguished {text_style['item']('lantern')}",
            desc=text_style['desc'](
                "The lantern is unlit. It has fuel though; you imagine you could get it lit if you had some matches."
            ),
            weight=1,
            tags=["obtainable"]
        ),
        "amulet_of_yendor": Item(
            slug="amulet_of_yendor",
            name=text_style['item']("Amulet of Yendor"),
            long_name=f"the {text_style['item']('Amulet of Yendor')}",
            desc=text_style['desc'](
                "This amulet is said to contain unimaginable power."
            ),
            weight=0.5,
            tags=["obtainable"]
        ),
        "cheese": Item(
            slug="cheese",
            name=text_style['item']("cheese"),
            long_name=f"a hunk of {text_style['item']('cheese')}",
            desc=text_style['desc'](
                "It is a hunk of cheese. Looks all right."
            ),
            weight=0.25,
            tags=["obtainable", "food"]
        ),
        "goblin_corpse": Item(
            slug="goblin_corpse",
            name=text_style['item']("goblin corpse"),
            long_name=f"a {text_style['item']('goblin corpse')}",
            desc=text_style['desc'](
                f"It's a dead goblin. You turn it over, looking for valuables, but all you can find is "
                f"a\\crumpled {text_style['item_in_desc']('matchbook')}, which falls to the floor next to the corpse. "
            ),
            tags=["corpse"]
        ),
        "lever": Item(
            slug="lever",
            name=text_style['item']("lever"),
            long_name=f"a {text_style['item']('lever')} jutting from the cliff side",
            desc=text_style['desc'](
                "It looks close enough to reach. Your fingers twitch. You never could resist a good lever."
            )
        ),
        "matchbook": Item(
            slug="matchbook",
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
            slug="rope",
            name=text_style['item']("rope"),
            long_name=f"some {text_style['item']('rope')}",
            desc=text_style['desc']("Good, sturdy rope, about 50 feet long."),
            weight=2,
            tags=["obtainable"]
        ),
    }

    # Declare the rooms
    state["room"] = {
        "outside": Room(
            slug="outside",
            name="Outside Cave Entrance",
            desc=text_style['desc'](
                f"{text_style['dir_in_desc']('North')} of you, the cave mouth beckons."
            ),
            no_mobs=True,
        ),
        "foyer": Room(
            slug="foyer",
            name="Foyer",
            desc=text_style['desc'](
                f"Dim light filters in from the {text_style['dir_in_desc']('south')}. Dusty passages "
                f"run {text_style['dir_in_desc']('north')} and {text_style['dir_in_desc']('east')}."
            ),
            init_items=[state["item"]["sword"]],
        ),
        "overlook": Room(
            slug="overlook",
            name="Grand Overlook",
            desc=text_style['desc'](
                f"A steep cliff appears before you, falling into the darkness. Ahead to the "
                f"{text_style['dir_in_desc']('north')}, a lightflickers in the distance, but there is no way across "
                f"the chasm. A passage leads {text_style['dir_in_desc']('south')},away from the cliff."
            ),
            init_items=[state["item"]["rope"]],
        ),
        "narrow": Room(
            slug="narrow",
            name="Narrow Passage",
            desc=text_style['desc'](
                f"The narrow passage bends here from {text_style['dir_in_desc']('west')} to "
                f"{text_style['dir_in_desc']('north')}. The smell of gold permeates the air."
            ),
        ),
        "treasure": Room(
            slug="treasure",
            name="Treasure Chamber",
            desc=text_style['desc'](
                f"You've found the long-lost treasure chamber! Sadly, it has already been completely emptied "
                f"byearlier adventurers. The only exit is to the {text_style['dir_in_desc']('south')}."
            ),
            init_items=[state["item"]["lantern"]],
        ),
        "chasm": Room(
            slug="chasm",
            name="Over The Edge",
            desc=text_style['desc'](
                f"You find yourself suspended over a dark chasm, at the end of a rope that was clearly notlong "
                f"enough for this job. Glancing about, you see a {text_style['item_in_desc']('lever')} jutting out "
                f"from the wall, half hidden.The rope leads back {text_style['dir_in_desc']('up')}."
            ),
            dark=True,
            dark_desc=text_style['desc'](
                f"You find yourself suspended over a dark chasm, at the end of a rope that was clearly notlong "
                f"enough for this job. It is dark. You can't see a thing. You are likely to be eaten by a grue.The "
                f"rope leads back {text_style['dir_in_desc']('up')}."
            ),
            no_mobs=True,
            no_drop=True,
            init_items=[state["item"]["lever"]]
        ),
        "final": Room(
            slug="final",
            name="Across the Chasm",
            desc=text_style['desc'](
                f"You find a small, elaborately decorated room. Sunlight streams down a hole in the ceiling "
                f"highabove you, illuminating an altar upon which sits the fabled "
                f"{text_style['item_in_desc']('Amulet of Yendor')}.To the {text_style['dir_in_desc']('south')}, a "
                f"bridge leads back the way you came."
            ),
            init_items=[state["item"]["amulet_of_yendor"]]
        ),
    }

    # Declare the mobs
    mob_types = {
        "goblin": lambda mob_id: Mob(
            mob_id=mob_id,
            name=text_style['mob']("goblin"),
            long_name=f"a {text_style['mob']('goblin')}",
            desc=text_style['desc'](
                f"The {text_style['mob_in_desc']('goblin')} is eyeing you warily and shuffling his weight from one "
                f"foot to the other.A crude knife dangles from his belt."
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
                    f"baleful glare that fades intoa look of weary resignation as he slumps to the ground, dead.",
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
                    f"your chest. You final thought,improbably, is a silent prayer that the "
                    f"{text_style['mob']('goblin')}'s filthy knife doesn't give you an infection.",
                )
            },
            stats={
                "health": 10,
                "damage": 2,
                "accuracy": .75,
                "evasion": .15
            },
            init_loc=state["room"]["foyer"],
            init_att="neutral",
            items=([state["item"]["goblin_corpse"]])
        )
    }
    state["mobs"] = [mob_types["goblin"](1)]

    # Link rooms together
    state["room"]["outside"].n_to = (state["room"]["foyer"], "You step into the mouth of the cave.")
    state["room"]["foyer"].s_to = (state["room"]["outside"], "You head south, and find yourself outside the cave.")
    state["room"]["foyer"].n_to = (
        state["room"]["overlook"],
        "You make your way north, and the cave opens up suddenly, revealing a vast chasm before you."
    )
    state["room"]["foyer"].e_to = (
        state["room"]["narrow"],
        "You take the eastern passage. It grows narrower until you have a hard time standing straight."
    )
    state["room"]["overlook"].s_to = (state["room"]["foyer"], "You step back from the cliff's edge and head south.")
    state["room"]["overlook"].n_to = (
        state["room"]["overlook"],
        "You take a step back, and get ready to jump over the gap. Then you realize that is "
        f"an incredibly stupid idea, and decide you would rather live."
    )
    state["room"]["narrow"].w_to = (
        state["room"]["foyer"],
        "You move west through the cramped passage until it opens up a bit."
    )
    state["room"]["narrow"].n_to = (
        state["room"]["treasure"],
        "You follow your nose and head north."
    )
    state["room"]["treasure"].s_to = (state["room"]["narrow"], "You head south into the narrow passage.")
    state["room"]["chasm"].u_to = (
        state["room"]["overlook"],
        "You climb slowly back up the rope, and pull yourself back onto the overlook, panting."
    )
    state["room"]["final"].s_to = (
        state["room"]["overlook"],
        "You go back across the bridge, resisting the pull of the amulet."
    )

    # Set initial room
    state["player"].loc = state["room"]["outside"]

    # Add functionality to items
    state["item"]["sword"].use = use_sword
    state["item"]["rope"].use = use_rope
    state["item"]["lantern"].use = use_lantern
    state["item"]["matchbook"].use = use_matchbook
    state["item"]["goblin_corpse"].on_look = on_look_goblin_corpse
    state["item"]["lever"].use_from_env = use_from_env_lever

    return state
