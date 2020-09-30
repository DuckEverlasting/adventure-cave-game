import pygame
import time

black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
magenta = (255, 0, 255)


# Set up wrappers for coloring text
def title_text(string):
    return {
        "text": string,
        "color": yellow,
        "background": blue
    }


def error_text(string):
    return {
        "text": string,
        "color": red,
        "background": None
    }


def desc_text(string):
    return {
        "text": string,
        "color": yellow,
        "background": None
    }


def item_text(string):
    return {
        "text": string,
        "color": cyan,
        "background": None
    }


def mob_text(string):
    return {
        "text": string,
        "color": red,
        "background": None
    }


def dir_text(string):
    return {
        "text": string,
        "color": magenta,
        "background": None
    }


text_style = {
    "title": title_text,
    "error": error_text,
    "desc": desc_text,
    "item": item_text,
    "mob": mob_text,
    "dir": dir_text
}


def pause(num=0.75):
    time.sleep(num)
