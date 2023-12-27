# Pylon contender
# also there is a lot of delays for a reason lmao

import win32api
import time
import pyautogui
import random
import keyboard

state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
state_right = win32api.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128

chance = 100 # percent
cps_extra = 1 # an int that defines how many extra cps will be clicked, default is one (basically a double click)
running = True

def mouseClick(percentage):
    if(random.random() < (percentage / 100)):
        # giving it a little interval cuz why not
        pyautogui.click(clicks=cps_extra+1, interval=0.01) # for some reason pyautogui.click() only doesn't work lol

if __name__ == "__main__":
    while True:
        a = win32api.GetKeyState(0x01)
        b = win32api.GetKeyState(0x02)

        if a != state_left and a < 0 and running:  # Button state changed and being pressed        
            mouseClick(chance)
            time.sleep(0.01)
       
        # if the button "q" is pressed then disable the clicker
        # this was implemented as a safety feature in case any bugs happened
        if keyboard.is_pressed("p"):
            if (running):
                running = False
                print("DISABLED")
            else:
                running = True
                print("ENABLED")
            time.sleep(0.1)

        time.sleep(0.001)
