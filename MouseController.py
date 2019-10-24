import numpy as np
import pyautogui
import os

EAR_THRESHOLD = 0.25

mouseController = None


class MouseController:
    def __init__(self):
        self.left_mouse_down = False
        self.right_mouse_down = False
        self.scroll_up = False
        self.scroll_down = False
        self.last_nose_position = 0

    def eye_aspect_ratio_algorithm(self, eye):
        height1 = np.linalg.norm(eye[1] - eye[5])
        height2 = np.linalg.norm(eye[2] - eye[4])
        width = np.linalg.norm(eye[0] - eye[3])
        return (height1 + height2) / (2.0 * width)

    def mouse_click(self, left_eye, right_eye):
        left_EAR = self.eye_aspect_ratio_algorithm(left_eye)
        right_EAR = self.eye_aspect_ratio_algorithm(right_eye)

        if left_EAR < EAR_THRESHOLD and left_EAR < right_EAR:
            self.left_mouse_down = True
            self.right_mouse_down = False
        elif right_EAR < EAR_THRESHOLD and right_EAR < left_EAR:
            self.right_mouse_down = True
            self.left_mouse_down = False
        else:
            self.left_mouse_down = False
            self.right_mouse_down = False

        if self.left_mouse_down:
            os.system('xdotool mousedown 1') 
        else:
            os.system('xdotool mouseup 1') 

        if self.right_mouse_down:
            os.system('xdotool mousedown 3')
        else:
            os.system('xdotool mouseup 3')

    def mouse_scroll(self, nose, mouth):
        ratio =  (mouth[9,1] - mouth[3,1])/(mouth[6,0] - mouth[0,0])
        # print(ratio)
        if ratio < 0.5: 
            self.last_nose_position = 0
            return 

        # print(self.last_nose_position)
        if self.last_nose_position == 0: 
            self.last_nose_position = nose[6,1]

        if nose[6,1] < self.last_nose_position*9/10:
            self.scroll_down = False
            self.scroll_up = True
        elif nose[6,1] > self.last_nose_position*11/10:
            self.scroll_down = True
            self.scroll_up = False
        else:
            self.scroll_down = False
            self.scroll_up = False

        if self.scroll_down:
            os.system('xdotool key Down') 
            
        if self.scroll_up:
            os.system('xdotool key Up') 


def mouse_click(left_eye, right_eye):
    global mouseController

    if mouseController is None:
        mouseController = MouseController()
    mouseController.mouse_click(left_eye, right_eye)

def mouse_scroll(nose, mouth):
    global mouseController

    if mouseController is None:
        mouseController = MouseController()
        mouseController.nose_upper_limit = nose[6,1] + 15
        mouseController.nose_lower_limit = nose[6,1] - 15
    mouseController.mouse_scroll(nose, mouth)

