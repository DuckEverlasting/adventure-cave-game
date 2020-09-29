import shelve # Used in saving / loading
from constants import text_style, pause
from logic import parse_list

def run_help(command, player, item, mob):
    player.screen.print("==============\nBasic Controls\n==============")
    player.screen.print(
        f"Move around: \"{text_style['item']('n')}orth\", \"{text_style['item']('s')}outh\", \"{text_style['item']('e')}ast\", \"{text_style['item']('w')}est\", \"down\", \"up\""
    )
    player.screen.print(
        f"Interact with things: \"{text_style['item']('l')}ook\", \"{text_style['item']('g')}et\", \"{text_style['item']('d')}rop\", \"{text_style['item']('u')}se\", \"eat\""
    )
    player.screen.print(f"Check inventory: \"{text_style['item']('i')}nv\"")
    player.screen.print(f"Fight: \"attack\"")
    player.screen.print(f"Do nothing: \"wait\"")
    player.screen.print(f"Save game: \"save\"")
    player.screen.print(f"Load game: \"load\"")
    player.screen.print(f"Exit game: \"{text_style['item']('q')}uit\"")
    player.screen.print()

def run_go(command, player, item, mob):
    dir_letter = command["adv"][0]
    result = player.move(dir_letter)
    if result:
        return {
            "time_passed": True,
            "player_moved": True,
        }
        

def run_inventory(command, player, item, mob):
    if len(player.items) > 0:
        player.screen.print(f"You have {parse_list(player.items)} in your inventory.\n")
    else:
        player.screen.print("You have no items in your inventory.\n")

def run_wait(command, player, item, mob):
    return {
        "time_passed": True,
    }

def run_quit(command, player, item, mob):
    confirm = player.screen.get_input('Are you sure? (Type "y" to confirm)\n> ')
    if confirm in ("y", "yes"):
        player.screen.print("\nExiting game...\n")
        pause(0.75)
        return {"end_game": True}
    else:
        player.screen.print()

def run_look(command, player, item, mob):
    # GENERAL LOOK
    if not command["i_obj"] and not command["d_obj"]:
        if player.loc.dark and not player.light_check():
            player.screen.print(f"{player.loc.dark_desc}\n")
        else:
            player.screen.print(f"{player.loc.desc}\n")

        mobs_here = [mob[i] for i in mob if mob[i].alive and mob[i].loc == player.loc]

        if not player.loc.dark or player.light_check():
            if len(player.loc.items) > 0:
                player.screen.print(f"You see {parse_list(player.loc.items)} here.")
                if len(mobs_here) == 0:
                    player.screen.print()

            if len(mobs_here) > 0:
                player.screen.print(f"You see {parse_list(mobs_here)} here.\n")
        else:
            if len(mobs_here) > 0:
                player.screen.print(f"You hear {parse_list('something')} moving in the darkness.\n")
    else:    
    # SPECIFIC LOOK
        # Grammar check (because "look" uses prepositions but none of its synonyms do)
        if command["act"] != "look":
            if command["i_obj"]:
                player.screen.print(text_style['error']("ERROR: COMMAND NOT RECOGNIZED\n"))
            obj = command["d_obj"]
        else:
            if command["d_obj"]:
                player.screen.print(text_style['error']("ERROR: COMMAND NOT RECOGNIZED\n"))
            obj = command["i_obj"]

        # Check lights
        if player.loc.dark and not player.light_check():
            player.screen.print("Too dark for that right now.\n")
        
        # Return description for item or mob if available
        elif obj in item:
            if item[obj] in player.items or item[obj] in player.loc.items:
                player.screen.print(f"{item[obj].desc}\n")
                item[obj].on_look()
                return {"time_passed": True}
            else:
                player.screen.print("There's nothing here by that name.\n")

        elif obj in mob:
            if mob[obj].loc == player.loc:
                player.screen.print(f"{mob[obj].desc}\n")
                mob[obj].on_look()
                return {"time_passed": True}
            else:
                player.screen.print("There's nothing here by that name.\n")

def run_get(command, player, item, mob):
    d_obj = command["d_obj"]
    if d_obj in item:
        result = player.get_item(item[d_obj])
        if result:
            return {"time_passed": True}
    else:
        player.screen.print("There's nothing here by that name.\n")

def run_drop(command, player, item, mob):
    d_obj = command["d_obj"]
    if d_obj in item:
        result = player.drop_item(item[d_obj])
        if result:
            return {"time_passed": True}
    else:
        player.screen.print("You don't have one of those in your inventory\n")

def run_use(command, player, item, mob):
    d_obj = command["d_obj"]
    i_obj = command["d_obj"]
    if d_obj in player.items:
        result = player.use_item(item[d_obj], i_obj)
        if result:
            return {"time_passed": True}
    elif d_obj in player.loc.items:
        result = player.use_item_from_env(item[d_obj], i_obj)
        if result:
            return {"time_passed": True}
    else:
        player.screen.print("There's nothing here by that name.\n")

def run_attack(command, player, item, mob):
    d_obj = command["d_obj"]
    i_obj = command["i_obj"]
    
    if d_obj in mob:
        if mob[d_obj].loc == player.loc:
            if not i_obj:
                weapons = [i for i in player.items if "weapon" in i.tags] + [item["fists"]]
                weapon_string = "Attack with what?"
                for i in range(len(weapons)):
                    weapon_string += f"\n{i + 1}:  {text_style['item'](weapons[i].name)}"
                player.screen.print(weapon_string)
                selection = player.screen.get_input('\n> ')
                try:
                    selection = int(selection) - 1
                    i_obj = weapons[selection]
                except:
                    return
            elif not item[i_obj] in player.items:
                if i_obj[0] in ["a", "e", "i", "o", "u"]:
                    player.screen.print(f"You don't have an {i_obj} on you.\n")
                    return
                else:
                    player.screen.print(f"You don't have a {i_obj} on you.\n")
                    return
            elif "weapon" not in item[i_obj].tags:
                player.screen.print("That's not a weapon.\n")
                return
            else:
                i_obj = item[i_obj]
            player.attack_mob(i_obj, mob[d_obj])
            return {"time_passed": True}                 
        else:
            player.screen.print(f"There's no {d_obj} here.\n")
    else:
        player.screen.print(f"There's no {d_obj} here.\n")

def run_eat(command, player, item, mob):
    d_obj = command["d_obj"]
    if d_obj in item:
        result = player.eat_item(item[d_obj])
        if result:
            return {"time_passed": True}
    elif d_obj in mob:
        if mob[d_obj].loc == player.loc:
            player.screen.print("That's... not food.\n")
        else:
            player.screen.print("There's nothing here by that name.\n")
    else:
        player.screen.print("There's nothing here by that name.\n")

def run_talk(command, player, item, mob):
    i_obj = command["i_obj"]
    if i_obj in item and (item[i_obj] in player.items or item[i_obj] in player.loc.items):
        player.screen.print(f"You attempt to have a comversation with the {i_obj}. It is rather one-sided.\n")
    elif i_obj in mob and mob[i_obj].loc == player.loc:
        mob[i_obj].on_talk()
    elif i_obj in ("myself", "yourself", "self",):
        player.screen.print("You strike up a conversation with yourself, but quickly grow bored.\n")
    else:
        player.screen.print(f"There's no {i_obj} here.\n")

def run_die(command, player, item, mob):
    confirm = player.screen.get_input('Really? (Type "y" to confirm)\n> ')
    if confirm in ("y", "yes"):
        player.screen.print("\nOkay...\n")
        player.health = 0
    else:
        player.screen.print()

def run_save(player, item, room, mob, mem):
    # Get saved games
    saved_games = shelve.open('saved_games')
    if not "list" in saved_games:
        saved_games["list"] = []
    confirm = player.screen.get_input('Save your game? (Type "y" to confirm)\n> ')
    if not confirm in ("y", "yes"):
        player.screen.print("\nNever mind, then.\n")
        saved_games.close()
        return
    player.screen.print("\nPick a name.")
    name = player.screen.get_input('> ')
    if not name or name == "list":
        player.screen.print("\nSave failed.\n")
        saved_games.close()
        return
    elif name in saved_games:
        confirm = player.screen.get_input('That name already exists. Overwrite saved game? (Type "y" to confirm)\n> ')
        if not confirm in ("y", "yes"):
            player.screen.print("\nNever mind, then.\n")
            saved_games.close()
            return
    mem["save_dat"] = {
        "player": player,
        "item": item,
        "room": room,
        "mob": mob
    }
    saved_games["list"] += [name]
    saved_games[name] = mem
    saved_games.close()
    player.screen.print("\nSaved!.\n")
    return
    
def run_load(screen, mem, loop=False, get_confirm=True):
    if not loop:
        saved_games = shelve.open('saved_games')
        if get_confirm:
            confirm = player.screen.get_input('Load a saved game? (Type "y" to confirm)\n> ')
            if not confirm in ("y", "yes"):
                screen.print("\nNever mind, then.\n")
                saved_games.close()
                return
        screen.print('\nLoad which game?')
        screen.print(text_style['error']("0: NONE (Cancel load)"))
        for i in range(len(saved_games["list"])):
            screen.print(text_style['item'](f"{i + 1}: {saved_games['list'][i]}"))
    else:
        screen.print('\nPlease enter a valid number')
    number = player.screen.get_input('\n> ')
    try:
        if int(number) == 0:
            screen.print("\nNever mind, then.\n")
            saved_games.close()
            return
        elif int(number) - 1 in range(len(saved_games["list"])):
            screen.print("\nLoading game...\n")
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