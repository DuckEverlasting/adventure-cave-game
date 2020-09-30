import random
import copy
import os

from constants import text_style, pause
from logic import parse_list, parse_command, action_synonyms
from definitions import create
from mob_act import mob_act

class Game:
    def __init__(self, screen):
        this.screen = screen
        end_game = False
        time_passed = False
        player_moved = True
        item = None
        room = None
        mob = None
        player = None
        action = None
        mem = {}
        screen = None

    def initialize_state(self):
        temp = create(self)
        self.item = temp["item"]
        self.room = temp["room"]
        self.mob = temp["mob"]
        self.player = temp["player"]
        self.action = temp["action"]
        temp = None

    def initialize_mem(self):
    # Initialize mem - use when starting new game
        return {
            "score": 0,
            "looked_at": {},
            "save_dat": {}
        }

    def game_start(self):
        # Opening sequence
        self.screen.print(
            text_style['title'](
                """
        █‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾█
        █    █████╗ ██████╗ ██╗   ██╗███████╗███╗   ██╗████████╗██╗   ██╗██████╗ ███████╗   █
        █   ██╔══██╗██╔══██╗██║   ██║██╔════╝████╗  ██║╚══██╔══╝██║   ██║██╔══██╗██╔════╝   █
        █   ███████║██║  ██║██║   ██║█████╗  ██╔██╗ ██║   ██║   ██║   ██║██████╔╝█████╗     █
        █   ██╔══██║██║  ██║╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║   ██║   ██║██╔══██╗██╔══╝     █
        █   ██║  ██║██████╔╝ ╚████╔╝ ███████╗██║ ╚████║   ██║   ╚██████╔╝██║  ██║███████╗   █
        █   ╚═╝  ╚═╝╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝   █
        █                                                                                   █
        █                         ██████╗ █████╗ ██╗   ██╗███████╗                          █
        █                        ██╔════╝██╔══██╗██║   ██║██╔════╝                          █
        █                        ██║     ███████║██║   ██║█████╗                            █
        █                        ██║     ██╔══██║╚██╗ ██╔╝██╔══╝                            █
        █                        ╚██████╗██║  ██║ ╚████╔╝ ███████╗                          █
        █                         ╚═════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝                          █
        █___________________________________________________________________________________█

        """
            )
        )

        pause(3)

        self.screen.clear()

        pause()

    # Start of main loop
    def submit_input(self, command):
        # Player's turn
        
        # Parse command
        command = parse_command(command)
        act = command["act"]
        adv = command["adv"]
        d_obj = command["d_obj"]
        prep = command["prep"]
        i_obj = command["i_obj"]
        error = command["error"]

        # Check for synonyms in actions. This check happens here as opposed
        # to in "logic" to preserve the parsed command for actions where
        # the wording is important. 
        if act in action_synonyms:
            act = action_synonyms[act]

        # Resolve player action
        self.screen.print()

        if error:
            self.screen.print(text_style['error']("ERROR: COMMAND NOT RECOGNIZED\n"))

        elif act in action:
            grammar_check = action[act].check_grammar(command)
            if not grammar_check["result"]:
                self.screen.print(grammar_check["message"] + "\n")
            else:
                action_result = action[act].run(self, command)
                if action_result != None:  
                    if "time_passed" in action_result:
                        time_passed = True
                    if "player_moved" in action_result:
                        player_moved = True
                    if "end_game" in action_result:
                        end_game = True
                    if "load_game" in action_result:
                        mem = action_result["load_game"]
                        player_moved = True
                        self.screen.clear()

        else:
            self.screen.print(f"You don't know how to {act}.\n")
            

        # Brief pause included for flavor
        pause()

        # check for game over cases
        if self.player.health <= 0:
            self.screen.print("You have died. Better luck next time!")

        elif self.item["amulet_of_yendor"] in self.player.items:
            self.screen.print("You've won the game! Congratulations!!!")
        
        if self.player.health <= 0 or self.item["amulet_of_yendor"] in self.player.items:
            pause()
            self.screen.print(
                text_style['title'](
    """
    █‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾█
    █     ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗      █
    █    ██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗     █
    █    ██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║██║   ██║█████╗  ██████╔╝     █
    █    ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗     █
    █    ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║     █
    █     ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝     █
    █___________________________________________________________________________________█

    """
                )
            )
            pause(2)
            choice = None
            while choice not in ["1", "2", "3"]:
                if not choice == None:
                    self.screen.print("Please enter one of the below options:")
                self.screen.print(text_style["item"]("1: Start new game\n2: Load game\n3: Quit game\n"))
                choice = self.screen.get_input("> ")
            if choice == "1":
                initialize_state()
                mem = initialize_mem()
                player_moved = True
                os.system("cls" if os.name == "nt" else "clear")
                pause()
            elif choice == "2":
                result = action["load"].run(mem = mem, get_confirm=False)
                if result and "load_game" in result:
                    mem = result["load_game"]
                    player_moved = True
                    os.system("cls" if os.name == "nt" else "clear")
                    pause()
                else:
                    end_game = True
            elif choice == "3":
                end_game = True
                self.screen.print("\nExiting game...\n")
                pause(0.75)

        # Check for loaded game
        if not mem["save_dat"] == {}:
            player = mem["save_dat"]["player"]
            item = mem["save_dat"]["item"]
            room = mem["save_dat"]["room"]
            mob = mem["save_dat"]["mob"]
            mem["save_dat"] = {}

        # After player's turn
        # Mob actions
        if time_passed:
            for i in mob:
                if mob[i].alive:
                    mob_act(mob[i], player, player_moved)

        # Determine which information to display            
        if player_moved:
            spacers = "-" * len(player.loc.name)
            self.screen.print(spacers)
            self.screen.print(player.loc.name)
            self.screen.print(spacers)

        mobs_here = [mob[i] for i in mob if mob[i].alive and mob[i].loc == player.loc]
        if player.loc.dark and not player.light_check():
            if not player.loc.slug + "_dark" in mem["looked_at"]:
                self.screen.print(f"{player.loc.dark_desc}\n")
                mem["looked_at"][player.loc.slug + "_dark"] = True
            if player_moved and len(mobs_here) > 0:
                self.screen.print(f"You hear {parse_list('something')} moving in the darkness.\n")
        else:
            if not player.loc.slug in mem["looked_at"]:
                self.screen.print(f"{player.loc.desc}\n")
                mem["looked_at"][player.loc.slug] = True
            if player_moved:
                if len(player.loc.items) > 0:
                    self.screen.print(f"You see {parse_list(player.loc.items)} here.")
                    if len(mobs_here) == 0:
                        self.screen.print()
                if len(mobs_here) > 0:
                    self.screen.print(f"You see {parse_list(mobs_here)} here.\n")

        # Reset variables
        time_passed = False
        player_moved = False
        

