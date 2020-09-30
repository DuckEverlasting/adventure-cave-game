import random
from constants import pause


def mob_act(mob, player, player_moved):
    if mob.attitude == "neutral":
        neutral_behavior(mob, player, player_moved)
    elif mob.attitude == "hostile":
        hostile_behavior(mob, player, player_moved)


def neutral_behavior(mob, player, player_moved):
    result = mob.move_rand()
    if result:
        if mob.loc == player.loc:
            player.game.display.print_list(random.choice(mob.text['enter']) + ["\n"])
            # Brief pause included for flavor
            pause()
        elif mob.prev_loc == player.loc and not player_moved:
            player.game.display.print_list(random.choice(mob.text['exit']) + [result, "\n"])
            # Brief pause included for flavor
            pause()

    elif mob.loc == player.loc and not player_moved:
        player.game.display.print_list(random.choice(mob.text['idle']) + ["\n"])
        # Brief pause included for flavor
        pause()


def hostile_behavior(mob, player, player_moved):
    if mob.loc == player.prev_loc and player_moved:
        if player.loc.no_mobs:
            player.game.display.print_list(f"You hear the {mob.name}'s snarls echoing after you, but it seems you won't be followed here.\n")
        else:
            mob.move(room=player.loc)
            player.game.display.print_list(f"The {mob.name} chases after you.\n")
    elif mob.loc == player.loc:
        if player_moved:
            player.game.display.print_list(f"The {mob.name} spots you and growls, preparing to attack.\n")
        else:
            mob.attack_player(player)
