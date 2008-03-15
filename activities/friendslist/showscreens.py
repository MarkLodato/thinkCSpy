#
# Program: showscreens.py
# Author: Jeff Elkner
# Date: Feb 2, 2007
#
# Description: Display a series of "screens" extracted from a text file.
#
import os

def show(screen):
    os.system('clear')
    choice = raw_input(screen)
    return choice

f = open('screens.txt', 'r')
text = f.read()
f.close()
screens = text.split('+++')

for screen in screens[:3]:
    show(screen)

choice = show(screens[3].rstrip() + ' ')

while choice[0].upper() not in ['L', 'A', 'E', 'S', 'Q']:
    show(screens[-1] % choice)
    choice = show(screens[3].rstrip() + ' ')

show(screens[-2] % choice)