from inspect import signature

import pyglet
from constants import text_style, command_text
from logic import parse_list, parse_command, action_synonyms
from definitions import create
from mob_act import mob_act


class Game:
    def __init__(self, app):
        self.app = app
        self.display = app.display
        self.game_initialized = False
        self.game_running = False
        self.time_passed = False
        self.player_moved = True
        self.item = None
        self.room = None
        self.mob = None
        self.player = None
        self.action = None
        self.override = None
        self.mem = {}

    def game_boot(self):
        # Opening sequence
        self.display.print_text(
            text_style['title'](
                "{.align 'center'}"
                "█████████████████████████████████████████████████████████████████████████████████████\n\n"
                "█                                                                                   █\n\n"
                "█    █████╗ ██████╗ ██╗   ██╗███████╗███╗   ██╗████████╗██╗   ██╗██████╗ ███████╗   █\n\n"
                "█   ██╔══██╗██╔══██╗██║   ██║██╔════╝████╗  ██║╚══██╔══╝██║   ██║██╔══██╗██╔════╝   █\n\n"
                "█   ███████║██║  ██║██║   ██║█████╗  ██╔██╗ ██║   ██║   ██║   ██║██████╔╝█████╗     █\n\n"
                "█   ██╔══██║██║  ██║╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║   ██║   ██║██╔══██╗██╔══╝     █\n\n"
                "█   ██║  ██║██████╔╝ ╚████╔╝ ███████╗██║ ╚████║   ██║   ╚██████╔╝██║  ██║███████╗   █\n\n"
                "█   ╚═╝  ╚═╝╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝   █\n\n"
                "█                                                                                   █\n\n"
                "█                         ██████╗ █████╗ ██╗   ██╗███████╗                          █\n\n"
                "█                        ██╔════╝██╔══██╗██║   ██║██╔════╝                          █\n\n"
                "█                        ██║     ███████║██║   ██║█████╗                            █\n\n"
                "█                        ██║     ██╔══██║╚██╗ ██╔╝██╔══╝                            █\n\n"
                "█                        ╚██████╗██║  ██║ ╚████╔╝ ███████╗                          █\n\n"
                "█                         ╚═════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝                          █\n\n"
                "█                                                                                   █\n\n"
                "█                             Press Any Key To Begin                                █\n\n"
                "█████████████████████████████████████████████████████████████████████████████████████\n\n\n\n"
                "{.align 'left'}"
            )
        )

    def create_new_game(self):
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

    # Main loop
    def player_action(self, command):
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
        self.display.print_text()
        if error:
            self.display.print_text(text_style['error']("ERROR: COMMAND NOT RECOGNIZED\n\n"))
        elif act in self.action:
            grammar_check = self.action[act].check_grammar(command)
            if not grammar_check["result"]:
                self.display.print_text(grammar_check["message"] + "\n\n")
            else:
                run = self.action[act].run
                if "game" not in signature(run).parameters:
                    action_result = run()
                elif "command" not in signature(run).parameters:
                    action_result = run(self)
                else:
                    action_result = self.action[act].run(self, command)
                if action_result is not None:
                    if "time_passed" in action_result:
                        self.time_passed = True
                    if "player_moved" in action_result:
                        self.player_moved = True
                    if "end_game" in action_result:
                        self.app.window.close()
                    if "load_game" in action_result:
                        self.mem = action_result["load_game"]
                        self.player_moved = True
                        self.display.clear()
                    if "override" in action_result:
                        self.override = action_result["override"]
                        return

        else:
            self.display.print_text(f"You don't know how to {act}.\n\n")

    def submit_command(self, command):
        # Player action
        self.display.print_text(command_text(">>> " + command))

        command = command.lower()
        if self.game_running is False:
            self.handle_game_not_running(command)
            return
        elif self.override:
            self.override(command)
            self.override = None
        else:
            self.player_action(command)

        # Mob actions
        if self.time_passed:
            for i in self.mob:
                if self.mob[i].alive:
                    self.display.wait()
                    mob_act(self.mob[i], self.player, self.player_moved)

        # Check for game over
        game_is_over = False
        if self.player.health <= 0:
            self.display.print_text("You have died. Better luck next time!")
            self.game_running = False

        elif self.item["amulet_of_yendor"] in self.player.items:
            self.display.print_text("You've won the game! Congratulations!!!")
            self.game_running = False

        if not self.game_running:
            self.display.wait()
            self.print_game_over()
            self.display.wait(2)
            self.handle_game_not_running()

        # Check for loaded game
        if not self.mem["save_dat"] == {}:
            self.player = self.mem["save_dat"]["player"]
            self.item = self.mem["save_dat"]["item"]
            self.room = self.mem["save_dat"]["room"]
            self.mob = self.mem["save_dat"]["mob"]
            self.mem["save_dat"] = {}

        # Display current data
        self.display_room_info()

    def print_game_over(self):
        self.display.print_text(
            text_style['title'](
                "█‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾█\n\n"
                "█     ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗      █\n\n"
                "█    ██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗     █\n\n"
                "█    ██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║██║   ██║█████╗  ██████╔╝     █\n\n"
                "█    ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗     █\n\n"
                "█    ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║     █\n\n"
                "█     ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝     █\n\n"
                "█___________________________________________________________________________________█\n\n\n\n"
            )
        )

    def handle_game_not_running(self, choice=None):
        if not self.game_initialized:
            self.display.clear()
            self.display.wait(.3)
        if choice not in ["1", "2", "3"]:
            if choice is not None:
                self.display.print_text("Please enter one of the below options:")
            self.display.print_text(text_style["item"]("1: Start new game\n\n2: Load game\n\n3: Quit game\n\n"))
            return
        if choice == "1":
            self.create_new_game()
            self.player_moved = True
            self.game_running = True
            self.display.clear()
            self.display_room_info()
        elif choice == "2":
            result = self.action["load"].run(mem=self.mem, get_confirm=False)
            if result and "load_game" in result:
                self.mem = result["load_game"]
                self.player_moved = True
                self.game_running = True
                self.display.clear()
                self.display_room_info()
            else:
                pyglet.app.exit()
        elif choice == "3":
            self.display.print_text("\n\nExiting game...\n\n")
            self.display.wait(.75)
            pyglet.app.exit()

    def display_room_info(self):
        if self.player_moved:
            spacers = "-" * 10
            self.display.print_text(spacers)
            self.display.print_text(self.player.loc.name)
            self.display.print_text(spacers + "\n\n")

        mobs_here = [self.mob[i] for i in self.mob if self.mob[i].alive and self.mob[i].loc == self.player.loc]
        if self.player.loc.dark and not self.player.light_check():
            if not self.player.loc.slug + "_dark" in self.mem["looked_at"]:
                self.display.print_text(self.player.loc.dark_desc + "\n\n")
                self.mem["looked_at"][self.player.loc.slug + "_dark"] = True
            if self.player_moved and len(mobs_here) > 0:
                self.display.print_text(f"You hear {parse_list('something')} moving in the darkness.\n\n")
        else:
            if self.player.loc.slug not in self.mem["looked_at"]:
                self.display.print_text(self.player.loc.desc + "\n\n")
                self.mem["looked_at"][self.player.loc.slug] = True
            if self.player_moved:
                if len(self.player.loc.items) > 0:
                    self.display.print_text(f"You see {parse_list(self.player.loc.items)} here.")
                    if len(mobs_here) == 0:
                        self.display.print_text()
                if len(mobs_here) > 0:
                    self.display.print_text(f"You see {parse_list(mobs_here)} here.\n\n")

        # Reset variables
        self.time_passed = False
        self.player_moved = False
