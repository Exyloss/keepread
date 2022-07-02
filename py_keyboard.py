#!/usr/bin/env python3
from pynput.keyboard import Controller
from sys import argv
keyboard = Controller()
string = argv[-1]
for i in string:
    keyboard.press(i)
