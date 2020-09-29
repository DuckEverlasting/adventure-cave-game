import time
from colorama import Fore, Back, Style

# Set up wrappers for coloring text
def title_text(string):
    return f"{Fore.YELLOW}{Style.BRIGHT}{Back.BLUE}{Style.BRIGHT}{string}{Style.RESET_ALL}{Style.BRIGHT}"

def error_text(string):
    return f"{Fore.RED}{Style.BRIGHT}{string}{Style.RESET_ALL}{Style.BRIGHT}"

def desc_text(string):
    return f"{Fore.YELLOW}{Style.BRIGHT}{string}{Style.RESET_ALL}{Style.BRIGHT}"

def item_text(string):
    return f"{Fore.CYAN}{Style.BRIGHT}{string}{Style.RESET_ALL}{Style.BRIGHT}"

def item_in_desc_text(string):
    return f"{Fore.CYAN}{Style.BRIGHT}{string}{Fore.YELLOW}{Style.BRIGHT}"

def mob_text(string):
    return f"{Fore.RED}{Style.BRIGHT}{string}{Style.RESET_ALL}{Style.BRIGHT}"

def mob_in_desc_text(string):
    return f"{Fore.RED}{Style.BRIGHT}{string}{Fore.YELLOW}{Style.BRIGHT}"

def dir_text(string):
    return f"{Fore.MAGENTA}{Style.BRIGHT}{string}{Style.RESET_ALL}{Style.BRIGHT}"

def dir_in_desc_text(string):
    return f"{Fore.MAGENTA}{Style.BRIGHT}{string}{Fore.YELLOW}{Style.BRIGHT}"

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