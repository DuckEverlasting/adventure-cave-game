import shelve  # Used in saving / loading
from constants import text_style
from logic import parse_list


# noinspection SpellCheckingInspection
def run_help(game):
    game.display.print_text("==============\n\nBasic Controls\n\n==============")
    game.display.print_text(
        'Move around: "' +
        text_style['item']('n') +
        'orth", "' +
        text_style['item']('s') +
        'outh", "' +
        text_style['item']('e') +
        'ast", "' +
        text_style['item']('w') +
        'est", "down", "up"'
    )
    game.display.print_text(
        'Interact with things: "' +
        text_style['item']('l') +
        'ook," "' +
        text_style['item']('g') +
        'et", "' +
        text_style['item']('d') +
        'rop", "' +
        text_style['item']('u') +
        'se", "eat"'
    )
    game.display.print_text(
        'Check inventory: "' +
        text_style['item']('i') +
        'nv"'
    )
    game.display.print_text('Fight: "attack"')
    game.display.print_text('Do nothing: "wait"')
    game.display.print_text('Save game: "save"')
    game.display.print_text('Load game: "load"')
    game.display.print_text(
        'Exit game: "' +
        text_style['item']('q') +
        'uit"'
    )
    game.display.print_text()


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
        game.display.print_text(
            "You have " +
            parse_list(game.player.items) +
            " in your inventory.\n\n"
        )
    else:
        game.display.print_text("You have no items in your inventory.\n\n")


def run_wait():
    return {
        "time_passed": True,
    }


def run_quit(game, confirm=None):
    if confirm is None:
        game.display.print_text('Are you sure? (Type "y" to confirm)\n\n')
        return {"override": lambda response: run_quit(game, confirm=response)}
    if confirm in ("y", "yes"):
        game.display.print_text("\n\nExiting game...\n\n")
        game.display.wait(0.75)
        return {"end_game": True}
    else:
        game.display.print_text()


def run_look(game, command):
    # GENERAL LOOK
    if not command["i_obj"] and not command["d_obj"]:
        if game.player.loc.dark and not game.player.light_check():
            game.display.print_text(game.player.loc.dark_desc + "\n\n")
        else:
            game.display.print_text(game.player.loc.desc + "\n\n")

        mobs_here = [game.mob[i] for i in game.mob if game.mob[i].alive and game.mob[i].loc == game.player.loc]

        if not game.player.loc.dark or game.player.light_check():
            if len(game.player.loc.items) > 0:
                game.display.print_text(
                    f"You see {parse_list(game.player.loc.items)} here."
                )
                if len(mobs_here) == 0:
                    game.display.print_text()

            if len(mobs_here) > 0:
                game.display.print_text(
                    f"You see {parse_list(mobs_here)} here."
                )
        else:
            if len(mobs_here) > 0:
                game.display.print_text(
                    f"You hear {parse_list('something')} moving in the darkness.\n\n"
                )
    else:
        # SPECIFIC LOOK
        # Grammar check (because "look" uses prepositions but none of its synonyms do)
        if command["act"] != "look":
            if command["i_obj"]:
                game.display.print_text(text_style['error']("ERROR: COMMAND NOT RECOGNIZED\n\n"))
            obj = command["d_obj"]
        else:
            if command["d_obj"]:
                game.display.print_text(text_style['error']("ERROR: COMMAND NOT RECOGNIZED\n\n"))
            obj = command["i_obj"]

        # Check lights
        if game.player.loc.dark and not game.player.light_check():
            game.display.print_text("Too dark for that right now.\n\n")

        # Return description for item or mob if available
        elif obj in game.item:
            if game.item[obj] in game.player.items or game.item[obj] in game.player.loc.items:
                game.display.print_text(game.item[obj].desc + "\n\n")
                game.item[obj].on_look()
                return {"time_passed": True}
            else:
                game.display.print_text("There's nothing here by that name.\n\n")

        elif obj in game.mob:
            if game.mob[obj].loc == game.player.loc:
                game.display.print_text(game.mob[obj].desc + "\n\n")
                game.mob[obj].on_look()
                return {"time_passed": True}
            else:
                game.display.print_text("There's nothing here by that name.\n\n")


def run_get(game, command):
    d_obj = command["d_obj"]
    if d_obj in game.item:
        result = game.player.get_item(game.item[d_obj])
        if result:
            return {"time_passed": True}
    else:
        game.display.print_text("There's nothing here by that name.\n\n")


def run_drop(game, command):
    d_obj = command["d_obj"]
    if d_obj in game.item:
        result = game.player.drop_item(game.item[d_obj])
        if result:
            return {"time_passed": True}
    else:
        game.display.print_text("You don't have one of those in your inventory\n\n")


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
        game.display.print_text("There's nothing here by that name.\n\n")


def run_attack(game, command, selection=None):
    d_obj = command["d_obj"]
    i_obj = command["i_obj"]

    if d_obj in game.mob:
        if game.mob[d_obj].loc == game.player.loc:
            if not i_obj:
                weapons = [i for i in game.player.items if "weapon" in i.tags] + [game.item["fists"]]
                if not selection:
                    weapon_string = "Attack with what?"
                    for i in range(len(weapons)):
                        weapon_string += f"\n\n{i + 1}: {text_style['item'](weapons[i].name)}"
                    game.display.print_text(weapon_string)
                    return {"override": lambda num: run_attack(game, command, num)}
                try:
                    selection = int(selection) - 1
                    i_obj = weapons[selection]
                except:
                    return
            elif not game.item[i_obj] in game.player.items:
                if i_obj[0] in ["a", "e", "i", "o", "u"]:
                    game.display.print_text(f"You don't have an {i_obj} on you.\n\n")
                    return
                else:
                    game.display.print_text(f"You don't have a {i_obj} on you.\n\n")
                    return
            elif "weapon" not in game.item[i_obj].tags:
                game.display.print_text("That's not a weapon.\n\n")
                return
            else:
                i_obj = game.item[i_obj]
            game.player.attack_mob(i_obj, game.mob[d_obj])
            return {"time_passed": True}
        else:
            game.display.print_text(f"There's no {d_obj} here.\n\n")
    else:
        game.display.print_text(f"There's no {d_obj} here.\n\n")


def run_eat(game, command):
    d_obj = command["d_obj"]
    if d_obj in game.item:
        result = game.player.eat_item(game.item[d_obj])
        if result:
            return {"time_passed": True}
    elif d_obj in game.mob:
        if game.mob[d_obj].loc == game.player.loc:
            game.display.print_text("That's... not food.\n\n")
        else:
            game.display.print_text("There's nothing here by that name.\n\n")
    else:
        game.display.print_text("There's nothing here by that name.\n\n")


def run_talk(game, command):
    i_obj = command["i_obj"]
    if i_obj in game.item and (game.item[i_obj] in game.player.items or game.item[i_obj] in game.player.loc.items):
        game.display.print_text(f"You attempt to have a conversation with the {i_obj}. It is rather one-sided.\n\n")
    elif i_obj in game.mob and game.mob[i_obj].loc == game.player.loc:
        game.mob[i_obj].on_talk()
    elif i_obj in ("myself", "yourself", "self",):
        game.display.print_text("You strike up a conversation with yourself, but quickly grow bored.\n\n")
    else:
        game.display.print_text(f"There's no {i_obj} here.\n\n")


def run_die(game, confirm=None):
    if confirm is None:
        game.display.print_text('Really? (Type "y" to confirm)\n\n')
        return {"override": lambda response: run_die(game, confirm=response)}
    if confirm in ("y", "yes"):
        game.display.print_text("\n\nOkay...\n\n")
        game.player.health = 0
    else:
        game.display.print_text()


def run_save(game, confirm=None, name=None, overwrite=None):
    # Get saved games
    saved_games = shelve.open('saved_games')
    if "list" not in saved_games:
        saved_games["list"] = []
    if confirm is None:
        game.display.print_text('Save your game? (Type "y" to confirm)\n\n')
        return {"override": lambda response: run_save(game, confirm=response)}
    elif confirm not in ("y", "yes"):
        game.display.print_text("\n\nNever mind, then.\n\n")
        saved_games.close()
        return
    if name is None:
        game.display.print_text("\n\nPick a name.")
        return {"override": lambda response: run_save(game, confirm="y", name=response)}
    if not name or name == "list":
        game.display.print_text("\n\nSave failed.\n\n")
        saved_games.close()
        return
    elif name in saved_games:
        if overwrite not in ("y", "yes"):
            game.display.print_text('That name already exists. Overwrite saved game? (Type "y" to confirm)\n\n')
            return {"override": lambda response: run_save(game, confirm="y", name=name, overwrite=response)}
        if confirm not in ("y", "yes"):
            game.display.print_text("\n\nNever mind, then.\n\n")
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
    game.display.print_text("\n\nSaved!.\n\n")
    return


def run_load(game, loop=False, get_confirm=True, confirm=None, number=None):
    if number is not None:
        try_load(game, number)
        return
    if not loop:
        if get_confirm:
            if confirm is None:
                game.display.print_text('Load a saved game? (Type "y" to confirm)\n\n')
                return {"override": lambda response: run_load(game, confirm=response)}
            if confirm not in ("y", "yes"):
                game.display.print_text("\n\nNever mind, then.\n\n")
                return
        game.display.print_text('\n\nLoad which game?')
        game.display.print_text(text_style['error']("0: NONE (Cancel load)"))
        saved_games = shelve.open('saved_games')
        for i in range(len(saved_games["list"])):
            game.display.print_text(text_style['item'](f"{i + 1}: {saved_games['list'][i]}"))
        saved_games.close()
    else:
        game.display.print_text('\n\nPlease enter a valid number')
    return {"override": lambda response: run_load(game, number=response)}


def try_load(game, number):
    saved_games = shelve.open('saved_games')
    try:
        if int(number) == 0:
            game.display.print_text("\n\nNever mind, then.\n\n")
            saved_games.close()
            return
        elif int(number) - 1 in range(len(saved_games["list"])):
            game.display.print_text("\n\nLoading game...\n\n")
            game.display.wait(0.75)
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
