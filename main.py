import curses
from curses import wrapper
import time 
import random

def startScreen(standardScreen):
    with open("art.txt", "r") as fileHandler:
        standardScreen.clear()
        standardScreen.addstr(fileHandler.read())
        standardScreen.addstr("\nPress any key to begin")
        standardScreen.refresh()
        standardScreen.getkey()

def displayText(standardScreen, target, current, wpm=0):
    standardScreen.addstr(target)
    standardScreen.addstr(1, 0, f"WPM: {wpm}")


    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)
        standardScreen.addstr(0, i, char, color)

def textLoader():
    with open("words.txt", "r") as fileHandler:
        lines = fileHandler.readlines()
        return random.choice(lines).strip()


def wpm_test(standardScreen):
    target_text = textLoader()
    current_text = []
    wpm = 0
    startTime = time.time()
    standardScreen.nodelay(True)

    while True:        
        timeElapsed = max(time.time() - startTime, 1)
        wpm = round((len(current_text) / (timeElapsed / 60)) / 5)

        standardScreen.clear()
        displayText(standardScreen, target_text, current_text, wpm)
        standardScreen.refresh()

        if "".join(current_text) == target_text:
            standardScreen.nodelay(False)
            break


        try: 
            key = standardScreen.getkey()
        except:
            continue


        if ord(key) == 27:
            break

        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):                      
            current_text.append(key)
         
def main(standardScreen):
    #Colour Initializer
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    startScreen(standardScreen)

    while True:
        
        wpm_test(standardScreen)
        standardScreen.addstr(2, 0, "GAME ENDED! PRESS TO PLAY AGAIN")
        standardScreen.getkey()
        key = standardScreen.getkey()
        if ord(key) == 27:
            break


    

wrapper(main)
