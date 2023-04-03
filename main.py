import keyboard as kb
import time
import json
import os
from colorama import init, Fore, Back, Style

class TextFormatter:
    """
    Contains numerous ANSI escape sequences used to apply
    formatting and styling to text.
    """
    # Blue colouring
    BLUE_COL = '\033[94m'
    # Red Colouring
    RED_COL = '\033[91m'
    # Green colouring
    GREEN_COL = '\033[92m'
    
    # Reset formatting and styling
    RESET = '\033[0m'
    # Underlined text
    UNDERLINE = '\033[4m'
    # Yellow colouring
    YELLOW_COL = '\033[93m'


def read_config(path='./config.json'):
    '''
    As you may noticed from function name. It's reading json config file.
    '''
    config_file_name = path
    with open(config_file_name, encoding="utf-8") as config_file:
        config = json.load(config_file)
    jump_key = config["jump_key"]
    crouch_key = config["crouch_key"]
    fps = config["fps"]
    return jump_key, crouch_key, fps

def __main__():
    jump_key, crouch_key, fps = read_config(path='./config.json')
    frame_time = (1 / fps) * 1000

    print(f'''  
    jump key - {jump_key}
    crouch key - {'spacebar' if crouch_key == ' ' else crouch_key}
    fps - {fps}
     ''')

    previous_jump_state = False
    previous_crouch_state = False

    while True:
        if kb.is_pressed(jump_key) & (previous_jump_state == False):
            jump_time = time.time()
            previous_jump_state = True
            while True:
                if kb.is_pressed(crouch_key) & (previous_crouch_state == False):
                    previous_crouch_state = True
                    crouch_time = time.time()
                    diff_time = (crouch_time - jump_time) * 1000
                    diff_time_pretty = int((diff_time / frame_time)* 10) / 10

                    if (diff_time // frame_time) < 2:
                        str_to_show = f"{TextFormatter.GREEN_COL}possible - {diff_time_pretty} frames {TextFormatter.RESET}              "
                    else:
                        str_to_show = f"{TextFormatter.UNDERLINE}late by  {diff_time_pretty} frames {TextFormatter.RESET}               "
                    
                    print(str_to_show, end='')
                    print('\r', end='')
                    break
                
                if not kb.is_pressed(crouch_key):
                    previous_crouch_state = False

        if kb.is_pressed(crouch_key) & (previous_jump_state == False) & (previous_crouch_state == False):
            previous_crouch_state = True
            print(f"{TextFormatter.UNDERLINE}Crouched to early{TextFormatter.RESET}                            ",
                end='')
            print('\r', end='')

        if not kb.is_pressed(crouch_key):
            previous_crouch_state = False

        if not kb.is_pressed(jump_key):
            previous_jump_state = False

if __name__ == '__main__':
    init()
    os.system("mode con lines=15 cols=50")
    print(f'''
    To close window press {TextFormatter.BLUE_COL}Ctrl + C{TextFormatter.RESET}
    Change key bindings in {TextFormatter.BLUE_COL}config.json{TextFormatter.RESET}''')
    try:
         __main__()
    except KeyboardInterrupt:
        exit
