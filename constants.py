import time

black = "(0, 0, 0, 255)}"
red = "(255, 0, 0, 255)}"
blue = "(0, 0, 255, 255)}"
yellow = "(255, 255, 0, 255)}"
cyan = "(0, 255, 255, 255)}"
magenta = "(255, 0, 255, 255)}"

color = "{color: "
background = "{background: "


# Set up wrappers for coloring text
def title_text(string):
    return color + yellow + background + blue + string + color + black + background + black


def error_text(string):
    return color + red + string + color + black


def desc_text(string):
    return color + yellow + string + color + black


def item_text(string):
    return color + cyan + string + color + black


def item_in_desc_text(string):
    return color + cyan + string + color + yellow


def mob_text(string):
    return color + red + string + color + black


def mob_in_desc_text(string):
    return color + red + string + color + yellow


def dir_text(string):
    return color + magenta + string + color + black


def dir_in_desc_text(string):
    return color + magenta + string + color + yellow


text_style = {
    "title": title_text,
    "error": error_text,
    "desc": desc_text,
    "item": item_text,
    "item_in_desc": item_in_desc_text,
    "mob": mob_text,
    "mob_in_desc": mob_in_desc_text,
    "dir": dir_text,
    "dir_in_desc": dir_in_desc_text,
}


def pause(num=0.75):
    time.sleep(num)
