import shelve # Used in saving / loading
from constants import text_style, pause
from logic import parse_list

def run_help(game, command):
    game.screen.print("==============\nBasic Controls\n==============")
    game.screen.print(
        f"Move around: \"{text_style['item']('n')}orth\", \"{text_style['item']('s')}outh\", \"{text_style['item']('e')}ast\", \"{text_style['item']('w')}est\", \"down\", \"up\""
    )
    game.screen.print(
        f"Interact with things: \"{text_style['item']('l')}ook\", \"{text_style['item']('g')}et\", \"{text_style['item']('d')}rop\", \"{text_style['item']('u')}se\", \"eat\""
    )
    game.screen.print(f"Check inventory: \"{text_style['item']('i')}nv\"")
    game.screen.print(f"Fight: \"attack\"")
    game.screen.print(f"Do nothing: \"wait\"")
    game.screen.print(f"Save game: \"save\"")
    game.screen.print(f"Load game: \"load\"")
    game.screen.print(f"Exit game: \"{text_style['item']('q')}uit\"")
    game.screen.print()

def run_go(game, command):
    dir_letter = command["adv"][0]
    result = game.player.move(dir_letter)
    if result:
        return {
            "time_passed": True,
            "player_moved": True,
        }
        

def run_inventory(game, command):
    if len(game.player.items) > 0:
        game.screen.print(f"You have {parse_list(game.player.items)} in your inventory.\n")
    else:
        game.screen.print("You have no game.items in your inventory.\n")

def run_wait(game, command):
    return {
        "time_passed": True,
    }

def run_quit(game, command):
    confirm = game.screen.get_input('Are you sure? (Type "y" to confirm)\n> ')
    if confirm in ("y", "yes"):
        game.screen.print("\nExiting game...\n")
        pause(0.75)
        return {"end_game": True}
    else:
        game.screen.print()

def run_look(game, command):
    # GENERAL LOOK
    if not command["i_obj"] and not command["d_obj"]:
        if game.player.loc.dark and not game.player.light_check():
            game.screen.print(f"{game.player.loc.dark_desc}\n")
        else:
            game.screen.print(f"{game.player.loc.desc}\n")

        mobs_here = [game.mob[i] for i in game.mob if game.mob[i].alive and game.mob[i].loc == game.player.loc]

        if not game.player.loc.dark or game.player.light_check():
            if len(game.player.loc.items) > 0:
                game.screen.print(f"You see {parse_list(game.player.loc.items)} here.")
                if len(mobs_here) == 0:
                    game.screen.print()

            if len(mobs_here) > 0:
                game.screen.print(f"You see {parse_list(mobs_here)} here.\n")
        else:
            if len(mobs_here) > 0:
                game.screen.print(f"You hear {parse_list('something')} moving in the darkness.\n")
    else:    
    # SPECIFIC LOOK
        # Grammar check (because "look" uses prepositions but none of its synonyms do)
        if command["act"] != "look":
            if command["i_obj"]:
                game.screen.print(text_style['error']("ERROR: COMMAND NOT RECOGNIZED\n"))
            obj = command["d_obj"]
        else:
            if command["d_obj"]:
                game.screen.print(text_style['error']("ERROR: COMMAND NOT RECOGNIZED\n"))
            obj = command["i_obj"]

        # Check lights
        if game.player.loc.dark and not game.player.light_check():
            game.screen.print("Too dark for that right now.\n")
        
        # Return description for item or mob if available
        elif obj in game.item:
            if game.item[obj] in game.player.items or game.item[obj] in game.player.loc.items:
                game.screen.print(f"{game.item[obj].desc}\n")
                game.item[obj].on_look()
                return {"time_passed": True}
            else:
                game.screen.print("There's nothing here by that name.\n")

        elif obj in game.mob:
            if game.mob[obj].loc == game.player.loc:
                game.screen.print(f"{game.mob[obj].desc}\n")
                game.mob[obj].on_look()
                return {"time_passed": True}
            else:
                game.screen.print("There's nothing here by that name.\n")

def run_get(game, command):
    d_obj = command["d_obj"]
    if d_obj in game.item:
        result = game.player.get_item(game.item[d_obj])
        if result:
            return {"time_passed": True}
    else:
        game.screen.print("There's nothing here by that name.\n")

def run_drop(game, command):
    d_obj = command["d_obj"]
    if d_obj in game.item:
        result = game.player.drop_item(game.item[d_obj])
        if result:
            return {"time_passed": True}
    else:
        game.screen.print("You don't have one of those in your inventory\n")

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
        game.screen.print("There's nothing here by that name.\n")

def run_attack(game, command):
    d_obj = command["d_obj"]
    i_obj = command["i_obj"]
    
    if d_obj in game.mob:
        if game.mob[d_obj].loc == game.player.loc:
            if not i_obj:
                weapons = [i for i in game.player.items if "weapon" in i.tags] + [game.item["fists"]]
                weapon_string = "Attack with what?"
                for i in range(len(weapons)):
                    weapon_string += f"\n{i + 1}:  {text_style['item'](weapons[i].name)}"
                game.screen.print(weapon_string)
                selection = game.screen.get_input('\n> ')
                try:
                    selection = int(selection) - 1
                    i_obj = weapons[selection]
                except:
                    return
            elif not game.item[i_obj] in game.player.items:
                if i_obj[0] in ["a", "e", "i", "o", "u"]:
                    game.screen.print(f"You don't have an {i_obj} on you.\n")
                    return
                else:
                    game.screen.print(f"You don't have a {i_obj} on you.\n")
                    return
            elif "weapon" not in game.item[i_obj].tags:
                game.screen.print("That's not a weapon.\n")
                return
            else:
                i_obj = game.item[i_obj]
            game.player.attack_mob(i_obj, game.mob[d_obj])
            return {"time_passed": True}                 
        else:
            game.screen.print(f"There's no {d_obj} here.\n")
    else:
        game.screen.print(f"There's no {d_obj} here.\n")

def run_eat(game, command):
    d_obj = command["d_obj"]
    if d_obj in game.item:
        result = game.player.eat_item(game.item[d_obj])
        if result:
            return {"time_passed": True}
    elif d_obj in game.mob:
        if game.mob[d_obj].loc == game.player.loc:
            game.screen.print("That's... not food.\n")
        else:
            game.screen.print("There's nothing here by that name.\n")
    else:
        game.screen.print("There's nothing here by that name.\n")

def run_talk(game, command):
    i_obj = command["i_obj"]
    if i_obj in game.item and (game.item[i_obj] in game.player.items or game.item[i_obj] in game.player.loc.items):
        game.screen.print(f"You attempt to have a comversation with the {i_obj}. It is rather one-sided.\n")
    elif i_obj in game.mob and game.mob[i_obj].loc == game.player.loc:
        game.mob[i_obj].on_talk()
    elif i_obj in ("myself", "yourself", "self",):
        game.screen.print("You strike up a conversation with yourself, but quickly grow bored.\n")
    else:
        game.screen.print(f"There's no {i_obj} here.\n")

def run_die(game, command):
    confirm = game.screen.get_input('Really? (Type "y" to confirm)\n> ')
    if confirm in ("y", "yes"):
        game.screen.print("\nOkay...\n")
        game.player.health = 0
    else:
        game.screen.print()

def run_save(game):
    # Get saved games
    saved_games = shelve.open('saved_games')
    if not "list" in saved_games:
        saved_games["list"] = []
    confirm = game.screen.get_input('Save your game? (Type "y" to confirm)\n> ')
    if not confirm in ("y", "yes"):
        game.screen.print("\nNever mind, then.\n")
        saved_games.close()
        return
    game.screen.print("\nPick a name.")
    name = game.screen.get_input('> ')
    if not name or name == "list":
        game.screen.print("\nSave failed.\n")
        saved_games.close()
        return
    elif name in saved_games:
        confirm = game.screen.get_input('That name already exists. Overwrite saved game? (Type "y" to confirm)\n> ')
        if not confirm in ("y", "yes"):
            game.screen.print("\nNever mind, then.\n")
            saved_games.close()
            return
    mem["save_dat"] = {
        "player": game.player,
        "item": game.item,
        "room": game.room,
        "mob": game.mob
    }
    saved_games["list"] += [name]
    saved_games[name] = game.mem
    saved_games.close()
    game.screen.print("\nSaved!.\n")
    return
    
def run_load(game, loop=False, get_confirm=True):
    if not loop:
        saved_games = shelve.open('saved_games')
        if get_confirm:
            confirm = game.screen.get_input('Load a saved game? (Type "y" to confirm)\n> ')
            if not confirm in ("y", "yes"):
                game.screen.print("\nNever mind, then.\n")
                saved_games.close()
                return
        game.screen.print('\nLoad which game?')
        game.screen.print(text_style['error']("0: NONE (Cancel load)"))
        for i in range(len(saved_games["list"])):
            game.screen.print(text_style['item'](f"{i + 1}: {saved_games['list'][i]}"))
    else:
        game.screen.print('\nPlease enter a valid number')
    number = game.screen.get_input('\n> ')
    try:
        if int(number) == 0:
            game.screen.print("\nNever mind, then.\n")
            saved_games.close()
            return
        elif int(number) - 1 in range(len(saved_games["list"])):
            game.screen.print("\nLoading game...\n")
            pause(0.75)
            name = saved_games["list"][int(number) - 1]
            mem = saved_games[name]
            saved_games.close()
            return {"load_game": mem}
        else:
            run_load(mem, loop=True)
    except:
        run_load(mem, loop=True)

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