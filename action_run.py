import shelve  # Used in saving / loading
from constants import text_style, pause
from logic import parse_list


# noinspection SpellCheckingInspection
def run_help(game):
    game.display.print_list(["==============\nBasic Controls\n=============="])
    game.display.print_list([
        'Move around: "',
        text_style['item']('n'),
        'orth", "',
        text_style['item']('s'),
        'outh", "',
        text_style['item']('e'),
        'ast", "',
        text_style['item']('w'),
        'est", "down", "up"'
    ])
    game.display.print_list([
        'Interact with things: "',
        text_style['item']('l'),
        'ook," "',
        text_style['item']('g'),
        'et", "',
        text_style['item']('d'),
        'rop", "',
        text_style['item']('u'),
        'se", "eat"'
    ])
    game.display.print_list([
        'Check inventory: "',
        text_style['item']('i'),
        'nv"'
    ])
    game.display.print_list(['Fight: "attack"'])
    game.display.print_list(['Do nothing: "wait"'])
    game.display.print_list(['Save game: "save"'])
    game.display.print_list(['Load game: "load"'])
    game.display.print_list([
        'Exit game: "',
        text_style['item']('q'),
        'uit"'
    ])
    game.display.print_list()


def run_go(game, command):
    dir_letter = command["adv"][0]
    result = game.player.move(dir_letter)
    if result:
        return {
            "time_passed": True,
            "player_moved": True,
        }


def run_inventory(game):
    if len(game.player.items) > 0:
        game.display.print_list(
            ["You have ,"] +
            parse_list(game.player.items) +
            [" in your inventory.\n"]
        )
    else:
        game.display.print_list(["You have no items in your inventory.\n"])


def run_wait():
    return {
        "time_passed": True,
    }


def run_quit(game):
    confirm = game.display.get_input('Are you sure? (Type "y" to confirm)\n> ')
    if confirm in ("y", "yes"):
        game.display.print_list(["\nExiting game...\n"])
        pause(0.75)
        return {"end_game": True}
    else:
        game.display.print_list()


def run_look(game, command):
    # GENERAL LOOK
    if not command["i_obj"] and not command["d_obj"]:
        if game.player.loc.dark and not game.player.light_check():
            game.display.print_list([game.player.loc.dark_desc, "\n"])
        else:
            game.display.print_list([game.player.loc.desc, "\n"])

        mobs_here = [game.mob[i] for i in game.mob if game.mob[i].alive and game.mob[i].loc == game.player.loc]

        if not game.player.loc.dark or game.player.light_check():
            if len(game.player.loc.items) > 0:
                game.display.print_list(
                    ["You see "] +
                    parse_list(game.player.loc.items) +
                    [" here."]
                )
                if len(mobs_here) == 0:
                    game.display.print_list()

            if len(mobs_here) > 0:
                game.display.print_list(
                    ["You see "] +
                    parse_list(mobs_here) +
                    [" here.\n"]
                )
        else:
            if len(mobs_here) > 0:
                game.display.print_list(
                    ["You hear "] +
                    parse_list('something') +
                    [" moving in the darkness.\n"]
                )
    else:
        # SPECIFIC LOOK
        # Grammar check (because "look" uses prepositions but none of its synonyms do)
        if command["act"] != "look":
            if command["i_obj"]:
                game.display.print_list([text_style['error']("ERROR: COMMAND NOT RECOGNIZED\n")])
            obj = command["d_obj"]
        else:
            if command["d_obj"]:
                game.display.print_list([text_style['error']("ERROR: COMMAND NOT RECOGNIZED\n")])
            obj = command["i_obj"]

        # Check lights
        if game.player.loc.dark and not game.player.light_check():
            game.display.print_list(["Too dark for that right now.\n"])

        # Return description for item or mob if available
        elif obj in game.item:
            if game.item[obj] in game.player.items or game.item[obj] in game.player.loc.items:
                game.display.print_list([game.item[obj].desc, "\n"])
                game.item[obj].on_look()
                return {"time_passed": True}
            else:
                game.display.print_list(["There's nothing here by that name.\n"])

        elif obj in game.mob:
            if game.mob[obj].loc == game.player.loc:
                game.display.print_list([game.mob[obj].desc, "\n"])
                game.mob[obj].on_look()
                return {"time_passed": True}
            else:
                game.display.print_list(["There's nothing here by that name.\n"])


def run_get(game, command):
    d_obj = command["d_obj"]
    if d_obj in game.item:
        result = game.player.get_item(game.item[d_obj])
        if result:
            return {"time_passed": True}
    else:
        game.display.print_list(["There's nothing here by that name.\n"])


def run_drop(game, command):
    d_obj = command["d_obj"]
    if d_obj in game.item:
        result = game.player.drop_item(game.item[d_obj])
        if result:
            return {"time_passed": True}
    else:
        game.display.print_list(["You don't have one of those in your inventory\n"])


def run_use(game, command):
    d_obj = command["d_obj"]
    i_obj = command["d_obj"]
    if d_obj in game.player.items:
        result = game.player.use_item(game.item[d_obj], i_obj)
        if result:
            return {"time_passed": True}
    elif d_obj in game.player.loc.items:
        result = game.player.use_item_from_env(game.item[d_obj], i_obj)
        if result:
            return {"time_passed": True}
    else:
        game.display.print_list(["There's nothing here by that name.\n"])


def run_attack(game, command):
    d_obj = command["d_obj"]
    i_obj = command["i_obj"]

    if d_obj in game.mob:
        if game.mob[d_obj].loc == game.player.loc:
            if not i_obj:
                weapons = [i for i in game.player.items if "weapon" in i.tags] + [game.item["fists"]]
                weapon_string_list = ["Attack with what?"]
                for i in range(len(weapons)):
                    weapon_string_list += [f"\n{i + 1}: ", text_style['item'](weapons[i].name)]
                game.display.print_list(weapon_string_list)
                selection = game.display.get_input('\n> ')
                try:
                    selection = int(selection) - 1
                    i_obj = weapons[selection]
                except:
                    return
            elif not game.item[i_obj] in game.player.items:
                if i_obj[0] in ["a", "e", "i", "o", "u"]:
                    game.display.print_list([f"You don't have an {i_obj} on you.\n"])
                    return
                else:
                    game.display.print_list([f"You don't have a {i_obj} on you.\n"])
                    return
            elif "weapon" not in game.item[i_obj].tags:
                game.display.print_list(["That's not a weapon.\n"])
                return
            else:
                i_obj = game.item[i_obj]
            game.player.attack_mob(i_obj, game.mob[d_obj])
            return {"time_passed": True}
        else:
            game.display.print_list([f"There's no {d_obj} here.\n"])
    else:
        game.display.print_list([f"There's no {d_obj} here.\n"])


def run_eat(game, command):
    d_obj = command["d_obj"]
    if d_obj in game.item:
        result = game.player.eat_item(game.item[d_obj])
        if result:
            return {"time_passed": True}
    elif d_obj in game.mob:
        if game.mob[d_obj].loc == game.player.loc:
            game.display.print_list(["That's... not food.\n"])
        else:
            game.display.print_list(["There's nothing here by that name.\n"])
    else:
        game.display.print_list(["There's nothing here by that name.\n"])


def run_talk(game, command):
    i_obj = command["i_obj"]
    if i_obj in game.item and (game.item[i_obj] in game.player.items or game.item[i_obj] in game.player.loc.items):
        game.display.print_list([f"You attempt to have a conversation with the {i_obj}. It is rather one-sided.\n"])
    elif i_obj in game.mob and game.mob[i_obj].loc == game.player.loc:
        game.mob[i_obj].on_talk()
    elif i_obj in ("myself", "yourself", "self",):
        game.display.print_list(["You strike up a conversation with yourself, but quickly grow bored.\n"])
    else:
        game.display.print_list([f"There's no {i_obj} here.\n"])


def run_die(game):
    confirm = game.display.get_input('Really? (Type "y" to confirm)\n> ')
    if confirm in ("y", "yes"):
        game.display.print_list(["\nOkay...\n"])
        game.player.health = 0
    else:
        game.display.print_list()


def run_save(game):
    # Get saved games
    saved_games = shelve.open('saved_games')
    if "list" not in saved_games:
        saved_games["list"] = []
    confirm = game.display.get_input('Save your game? (Type "y" to confirm)\n> ')
    if confirm not in ("y", "yes"):
        game.display.print_list(["\nNever mind, then.\n"])
        saved_games.close()
        return
    game.display.print_list(["\nPick a name."])
    name = game.display.get_input('> ')
    if not name or name == "list":
        game.display.print_list(["\nSave failed.\n"])
        saved_games.close()
        return
    elif name in saved_games:
        confirm = game.display.get_input('That name already exists. Overwrite saved game? (Type "y" to confirm)\n> ')
        if confirm not in ("y", "yes"):
            game.display.print_list(["\nNever mind, then.\n"])
            saved_games.close()
            return
    game.mem["save_dat"] = {
        "player": game.player,
        "item": game.item,
        "room": game.room,
        "mob": game.mob
    }
    saved_games["list"] += [name]
    saved_games[name] = game.mem
    saved_games.close()
    game.display.print_list(["\nSaved!.\n"])
    return


def run_load(game, loop=False, get_confirm=True):
    saved_games = shelve.open('saved_games')
    if not loop:
        if get_confirm:
            confirm = game.display.get_input('Load a saved game? (Type "y" to confirm)\n> ')
            if confirm not in ("y", "yes"):
                game.display.print_list(["\nNever mind, then.\n"])
                saved_games.close()
                return
        game.display.print_list(['\nLoad which game?'])
        game.display.print_list([text_style['error']("0: NONE (Cancel load)")])
        for i in range(len(saved_games["list"])):
            game.display.print_list([text_style['item'](f"{i + 1}: {saved_games['list'][i]}")])
    else:
        game.display.print_list(['\nPlease enter a valid number'])
    number = game.display.get_input('\n> ')
    try:
        if int(number) == 0:
            game.display.print_list(["\nNever mind, then.\n"])
            saved_games.close()
            return
        elif int(number) - 1 in range(len(saved_games["list"])):
            game.display.print_list(["\nLoading game...\n"])
            pause(0.75)
            name = saved_games["list"][int(number) - 1]
            new_mem = saved_games[name]
            saved_games.close()
            return {"load_game": new_mem}
        else:
            saved_games.close()
            return run_load(game, loop=True)
    except:
        saved_games.close()
        return run_load(game, loop=True)


run = {
    "help": run_help,
    "go": run_go,
    "inventory": run_inventory,
    "wait": run_wait,
    "quit": run_quit,
    "look": run_look,
    "get": run_get,
    "drop": run_drop,
    "use": run_use,
    "attack": run_attack,
    "eat": run_eat,
    "talk": run_talk,
    "die": run_die,
    "save": run_save,
    "load": run_load
}
