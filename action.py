def scrub_underscores(string):
    return string.replace("_", " ")


class Action:
    def __init__(self, name, grammar, run):
        self.name = name
        self.grammar = grammar
        self.run = run

    def check_grammar(self, command):
        # Adverb rules
        if "adv_required" in self.grammar:
            # Currently hard coded for movement, since that's the only
            # place adverbs are being used.
            if command["adv"] is not None:
                act = scrub_underscores(command['act'])
                return {
                    "result": False,
                    "message": f"Where would you like to {act}?"
                }

        # Direct object rules
        if "d_obj_prohibited" in self.grammar:
            if command["d_obj"] is not None:
                d_obj = scrub_underscores(command['d_obj'])
                return {
                    "result": False,
                    "message": f"The word {d_obj} doesn't make sense there.",
                }
        elif "d_obj_required" in self.grammar:
            if command["d_obj"] is None:
                act = scrub_underscores(command['act'])
                return {"result": False, "message": f"What would you like to {act}?"}

        # Indirect object rules
        if "i_obj_prohibited" in self.grammar:
            if command["i_obj"] is not None:
                i_obj = scrub_underscores(command['i_obj'])
                return {
                    "result": False,
                    "message": f"The word {i_obj} doesn't make sense there.",
                }
        elif "i_obj_required" in self.grammar:
            if command["i_obj"] is None:
                if command["d_obj"] is not None:
                    act = scrub_underscores(command['act'])
                    d_obj = scrub_underscores(command['d_obj'])
                    return {
                        "result": False,
                        "message": f"What would you like to {act} {d_obj} {self.grammar['preps_accepted'][0]}?",
                    }
                else:
                    act = scrub_underscores(command['act'])
                    if command['prep'] is not None:
                        prep = scrub_underscores(command['prep'])
                    else:
                        prep = self.grammar['preps_accepted'][0]
                    return {"result": False, "message": f"What would you like to {act} {prep}?"}

        if command["i_obj"] is not None:
            if command["prep"] not in self.grammar["preps_accepted"]:
                prep = scrub_underscores(command['prep'])
                return {
                    "result": False,
                    "message": f"The word {prep} doesn't make sense there.",
                }

        return {"result": True, "message": None}
