import random


def mob_act(mob, player, player_moved):
    if mob.attitude == "neutral":
        neutral_behavior(mob, player, player_moved)
    elif mob.attitude == "hostile":
        hostile_behavior(mob, player, player_moved)


def neutral_behavior(mob, player, player_moved):
    result = mob.move_rand()
    if result:
        if mob.loc == player.loc:
            player.game.display.print_text(random.choice(mob.text['enter']) + "\n\n")
            # Brief pause included for flavor
            player.game.display.wait()
        elif mob.prev_loc == player.loc and not player_moved:
            player.game.display.print_text(random.choice(mob.text['exit']) + result + "\n\n")
            # Brief pause included for flavor
            player.game.display.wait()

    elif mob.loc == player.loc and not player_moved:
        player.game.display.print_text(random.choice(mob.text['idle']) + "\n\n")
        # Brief pause included for flavor
        player.game.display.wait()


def hostile_behavior(mob, player, player_moved):
    if mob.loc == player.prev_loc and player_moved:
        player.game.display.wait()
        if player.loc.no_mobs:
            player.game.display.print_text(
                f"You hear the {mob.name}'s snarls echoing after you, but it seems you won't be followed here.\n\n"
            )
        else:
            mob.move(room=player.loc)
            player.game.display.print_text(f"The {mob.name} chases after you.\n\n")
    elif mob.loc == player.loc:
        player.game.display.wait()
        if player_moved:
            player.game.display.print_text(f"The {mob.name} spots you and growls, preparing to attack.\n\n")
        else:
            mob.attack_player(player)
