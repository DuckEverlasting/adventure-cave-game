import random

from constants import half_space


def mob_act(mob, player, player_moved):
    if mob.attitude == "neutral":
        return neutral_behavior(mob, player, player_moved)
    elif mob.attitude == "hostile":
        return hostile_behavior(mob, player, player_moved)


def neutral_behavior(mob, player, player_moved):
    result = mob.move_rand()
    if result:
        if mob.loc == player.loc:
            return {
                "wait": True,
                "print_text": random.choice(mob.text['enter']) + half_space
            }
        elif mob.prev_loc == player.loc and not player_moved:
            return {
                "wait": True,
                "print_text": random.choice(mob.text['exit']) + result + half_space
            }

    elif mob.loc == player.loc and not player_moved:
        return {
            "wait": True,
            "print_text": random.choice(mob.text['idle']) + half_space
        }
    return {}


def hostile_behavior(mob, player, player_moved):
    if mob.loc == player.prev_loc and player_moved:
        if player.loc.no_mobs:
            return {
                "wait": True,
                "print_text": f"You hear the {mob.name}'s snarls echoing after you, "
                              "but it seems you won't be followed here. + half_space"
            }
        else:
            mob.move(room=player.loc)
            return {
                "wait": True,
                "print_text": f"The {mob.name} chases after you." + half_space
            }
    elif mob.loc == player.loc:
        if player_moved:
            return {
                "wait": True,
                "print_text": f"The {mob.name} spots you and growls, preparing to attack." + half_space
            }
        else:
            return mob.attack_player(player)
    return {}
