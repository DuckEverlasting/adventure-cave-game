# ADVENTURE CAVE

This started as an intro to Python exercise from the CS portion of Lambda school. (www.lambdaschool.com)

It has grown significantly, but it's purpose still remains largely the same: I've been using it to further my understanding of Python, and of OOP in general.

Aside from the 50 or so lines of code that made up the original assignment, all work here is by Matt Klein. (https://github.com/DuckEverlasting)

## Guide
Welcome, adventurer! This is a text-based adventure game along the lines of Zork or Colossal Cave. You play the game by typing simple commands into the console. Some examples:
* Walk north
* Look at goblin
* Get sword

If you need a list of the most common commands, try entering "help".

## Current Goals

* Add more content of all sorts. More rooms, items, and mobs. Use some of the features that have been built, so the thing doesn't seem so needlessly ornate.

* Add scoring
    - If going by the Zork model, score is achieved specifically by obtaining (and escaping with) certain items. (This allows for a set max score)
    - If not, just about any positive game interaction could add to the score. (This makes it... harder to have a set max score)

* Would it be necessary for items to know where they are? Investigate whether that would help.

* Remember the last item mentioned and substitute that if the user types
"it" later, e.g.

* Add a "continue" option at the end of attacking to retry with the same weapon/target.

* Add items with adjectives, like "rusty sword" and "silver sword".

    - Modify the parser to handle commands like "take rusty sword" as well as "take sword".

    - If the user is in a room that contains both the rusty sword _and_ silver sword, and they type "take sword", the parser should say, "I don't know which you mean: rusty sword or silver sword."
    
    - Accomplish by sorting a new type of word: adjective. This will probably have to be done from a set list. Pull them out before prepositions.

* Right now, optional functions like on_look, on_pick_up, on_eat all fire after their triggering event. Look into if you want any optional functions to fire before. (probably additional preconditions to the event firing).

* Consider replacing the use action. It's crazy generic.

* Fully implement encumberance

* Implement containers

* Think about implementing "get all"

* Add a menu to the beginning of the game similar to the one at the end.

* Add an intro (and on restart, offer the chance to skip the intro)

* Additional actions to consider:
    - Talk (this one could be a bit of a rabbit hole)
    - Status (check status)
    - Open / Close
    - Put in/on
    - Push/Pull/Move/Press
    - Throw
    - Drink
    - Give
    - Smell
    - Dig
