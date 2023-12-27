# Pylon contender
# also there is a lot of delays for a reason lmao

import win32api
import time
import pyautogui
import random
import keyboard
import imgui
import glfw
import OpenGL.GL as gl
from imgui.integrations.glfw import GlfwRenderer

state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
state_right = win32api.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128

def impl_glfw_init(window_name="Bunny Clicker", width=400, height=100, backgroundColor=(100, 100, 100, 255)):
    #hopefully this doesn't happen
    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(int(width), int(height), window_name, None, None)
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        exit(1)

    return window

# shoutout to mlegend
class GUI(object):

    #set up the window
    def __init__(self):
        super().__init__()
        self.backgroundColor = (34,37,40, 1)
        self.window = impl_glfw_init()
        gl.glClearColor(*self.backgroundColor)
        imgui.create_context()
        self.impl = GlfwRenderer(self.window)
        
        self.loop() 

    #main function
    def loop(self):
        chance = 100 # percent
        cps_extra = 1 # an int that defines how many extra cps will be clicked, default is one (basically a double click)
        running = True

        def mouseClick(percentage):
            if(random.random() < (percentage / 100)):
                # giving it a little interval cuz why not
                pyautogui.click(clicks=cps_extra+1, interval=0.01) # for some reason pyautogui.click() only doesn't work lol

        #this is what happens every frame
        while not glfw.window_should_close(self.window):
            #imgui frame stuff
            glfw.poll_events()
            self.impl.process_inputs()

            imgui.new_frame()
            imgui.set_next_window_size(550, 235)
            imgui.set_next_window_position(-1, -1)

            #start window and make it not movable and all that
            imgui.begin("Bunny Clicker", True, imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_SAVED_SETTINGS | imgui.WINDOW_ALWAYS_USE_WINDOW_PADDING)

            #ui elements
            _, running = imgui.checkbox("Running", running)
            imgui.push_item_width(250)
            _, chance = imgui.slider_int("Chance", chance, 1, 100)
            _, cps_extra = imgui.slider_int("Extra CPS", cps_extra, 1, 10)
            imgui.pop_item_width()
            imgui.end()

            #more imgui frame stuff
            imgui.render()

            gl.glClearColor(*self.backgroundColor)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            self.impl.render(imgui.get_draw_data())
            glfw.swap_buffers(self.window)

            #the actual clicking logic
            a = win32api.GetKeyState(0x01)
            b = win32api.GetKeyState(0x02)

            if a != state_left and a < 0 and running:  # Button state changed and being pressed        
                mouseClick(chance)
                time.sleep(0.01)
        
            # if the button "p" is pressed then disable the clicker
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

if __name__ == "__main__":
    gui = GUI()