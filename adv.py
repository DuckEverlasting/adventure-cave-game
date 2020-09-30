from constants import text_style, pause
from logic import parse_list, parse_command, action_synonyms
from definitions import create
from mob_act import mob_act


class Game:
    def __init__(self, display):
        self.display = display
        self.end_game = False
        self.time_passed = False
        self.player_moved = True
        temp = create(self)
        self.item = temp["item"]
        self.room = temp["room"]
        self.mob = temp["mob"]
        self.player = temp["player"]
        self.action = temp["action"]
        self.mem = {
            "score": 0,
            "looked_at": {},
            "save_dat": {}
        }

    def game_start(self):
        # Opening sequence
        self.display.print_list(
            text_style['title'](
                """
        █‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾█\\
        █    █████╗ ██████╗ ██╗   ██╗███████╗███╗   ██╗████████╗██╗   ██╗██████╗ ███████╗   █\\
        █   ██╔══██╗██╔══██╗██║   ██║██╔════╝████╗  ██║╚══██╔══╝██║   ██║██╔══██╗██╔════╝   █\\
        █   ███████║██║  ██║██║   ██║█████╗  ██╔██╗ ██║   ██║   ██║   ██║██████╔╝█████╗     █\\
        █   ██╔══██║██║  ██║╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║   ██║   ██║██╔══██╗██╔══╝     █\\
        █   ██║  ██║██████╔╝ ╚████╔╝ ███████╗██║ ╚████║   ██║   ╚██████╔╝██║  ██║███████╗   █\\
        █   ╚═╝  ╚═╝╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝   █\\
        █                                                                                   █\\
        █                         ██████╗ █████╗ ██╗   ██╗███████╗                          █\\
        █                        ██╔════╝██╔══██╗██║   ██║██╔════╝                          █\\
        █                        ██║     ███████║██║   ██║█████╗                            █\\
        █                        ██║     ██╔══██║╚██╗ ██╔╝██╔══╝                            █\\
        █                        ╚██████╗██║  ██║ ╚████╔╝ ███████╗                          █\\
        █                         ╚═════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝                          █\\
        █___________________________________________________________________________________█\\

        """
            )
        )

        pause(3)

        self.display.clear()

        pause()

    # Start of main loop
    def submit_input(self, command):
        # Player's turn

        # Parse command
        command = parse_command(command)
        act = command["act"]
        error = command["error"]

        # Check for synonyms in actions. This check happens here as opposed
        # to in "logic" to preserve the parsed command for actions where
        # the wording is important. 
        if act in action_synonyms:
            act = action_synonyms[act]

        # Resolve player action
        self.display.print_list()

        if error:
            self.display.print_list(text_style['error']("ERROR: COMMAND NOT RECOGNIZED\\"))

        elif act in self.action:
            grammar_check = self.action[act].check_grammar(command)
            if not grammar_check["result"]:
                self.display.print_list(grammar_check["message"] + "\\")
            else:
                action_result = self.action[act].run(self, command)
                if action_result is not None:
                    if "time_passed" in action_result:
                        self.time_passed = True
                    if "player_moved" in action_result:
                        self.player_moved = True
                    if "end_game" in action_result:
                        self.end_game = True
                    if "load_game" in action_result:
                        self.mem = action_result["load_game"]
                        self.player_moved = True
                        self.display.clear()

        else:
            self.display.print_list(f"You don't know how to {act}.\\")

        # Brief pause included for flavor
        pause()

        # check for game over cases
        if self.player.health <= 0:
            self.display.print_list("You have died. Better luck next time!")

        elif self.item["amulet_of_yendor"] in self.player.items:
            self.display.print_list("You've won the game! Congratulations!!!")

        if self.player.health <= 0 or self.item["amulet_of_yendor"] in self.player.items:
            pause()
            self.display.print_list(
                text_style['title'](
                    """
    █‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾█\\
    █     ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗      █\\
    █    ██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗     █\\
    █    ██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║██║   ██║█████╗  ██████╔╝     █\\
    █    ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗     █\\
    █    ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║     █\\
    █     ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝     █\\
    █___________________________________________________________________________________█\\

    """
                )
            )
            pause(2)
            choice = None
            while choice not in ["1", "2", "3"]:
                if choice is not None:
                    self.display.print_list("Please enter one of the below options:")
                self.display.print_list(text_style["item"]("1: Start new game\\2: Load game\\3: Quit game\\"))
                choice = self.display.get_input("> ")
            if choice == "1":
                self.__init__(self.display)
                self.player_moved = True
                self.display.clear()
                pause()
            elif choice == "2":
                result = self.action["load"].run(mem=self.mem, get_confirm=False)
                if result and "load_game" in result:
                    self.mem = result["load_game"]
                    self.player_moved = True
                    self.display.clear()
                    pause()
                else:
                    self.end_game = True
            elif choice == "3":
                self.end_game = True
                self.display.print_list("\\Exiting game...\\")
                pause(0.75)

        # Check for loaded game
        if not self.mem["save_dat"] == {}:
            self.player = self.mem["save_dat"]["player"]
            self.item = self.mem["save_dat"]["item"]
            self.room = self.mem["save_dat"]["room"]
            self.mob = self.mem["save_dat"]["mob"]
            self.mem["save_dat"] = {}

        # After player's turn
        # Mob actions
        if self.time_passed:
            for i in self.mob:
                if self.mob[i].alive:
                    mob_act(self.mob[i], self.player, self.player_moved)

        # Determine which information to display            
        if self.player_moved:
            spacers = "-" * len(self.player.loc.name)
            self.display.print_list(spacers)
            self.display.print_list(self.player.loc.name)
            self.display.print_list(spacers)

        mobs_here = [self.mob[i] for i in self.mob if self.mob[i].alive and self.mob[i].loc == self.player.loc]
        if self.player.loc.dark and not self.player.light_check():
            if not self.player.loc.slug + "_dark" in self.mem["looked_at"]:
                self.display.print_list(self.player.loc.dark_desc + "\\")
                self.mem["looked_at"][self.player.loc.slug + "_dark"] = True
            if self.player_moved and len(mobs_here) > 0:
                self.display.print_list(f"You hear {parse_list('something')} moving in the darkness.\\")
        else:
            if self.player.loc.slug not in self.mem["looked_at"]:
                self.display.print_list(self.player.loc.desc, "\\")
                self.mem["looked_at"][self.player.loc.slug] = True
            if self.player_moved:
                if len(self.player.loc.items) > 0:
                    self.display.print_list(f"You see {parse_list(self.player.loc.items)} here.")
                    if len(mobs_here) == 0:
                        self.display.print_list()
                if len(mobs_here) > 0:
                    self.display.print_list(f"You see {parse_list(mobs_here)} here.\\")

        # Reset variables
        self.time_passed = False
        self.player_moved = False
