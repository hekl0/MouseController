import numpy as np
import pyautogui
import os
import screeninfo

EAR_THRESHOLD = 0.25
SCREEN_W = screeninfo.get_monitors()[0].width
SCREEN_H = screeninfo.get_monitors()[0].height

mouseController = None


class MouseController:
    def __init__(self):
        self.left_mouse_down = False
        self.right_mouse_down = False
        self.origin_point = None

    def eye_aspect_ratio_algorithm(self, eye):
        height1 = np.linalg.norm(eye[1] - eye[5])
        height2 = np.linalg.norm(eye[2] - eye[4])
        width = np.linalg.norm(eye[0] - eye[3])
        return (height1 + height2) / (2.0 * width)

    def mouse_click(self, left_eye, right_eye):
        left_EAR = self.eye_aspect_ratio_algorithm(left_eye)
        right_EAR = self.eye_aspect_ratio_algorithm(right_eye)

        if self.left_mouse_down and left_EAR >= EAR_THRESHOLD:
            self.left_mouse_down = False
            os.system('xdotool mouseup 1')
        if self.right_mouse_down and right_EAR >= EAR_THRESHOLD:
            self.right_mouse_down = False
            os.system('xdotool mouseup 3')

        if not self.left_mouse_down and not self.right_mouse_down:
            if left_EAR < EAR_THRESHOLD and left_EAR < right_EAR:
                self.left_mouse_down = True
                os.system('xdotool mousedown 1') 
                print('LEFT')
            elif right_EAR < EAR_THRESHOLD and right_EAR < left_EAR:
                self.right_mouse_down = True
                os.system('xdotool mousedown 3')
                print('RIGHT')

    def mouse_move(self, nose):
        if self.origin_point == None:
            self.origin_point = nose
            return
        x = SCREEN_W / 2 + (nose[0] - self.origin_point[0]) * 20
        y = SCREEN_H / 2 + (nose[1] - self.origin_point[1]) * 20
        x = min(max(x, 0), SCREEN_W)
        y = min(max(y, 0), SCREEN_H)
        os.system('xdotool mousemove {} {}'.format(x, y))
        print(x, y)


def mouse_click(left_eye, right_eye):
    global mouseController

    if mouseController is None:
        mouseController = MouseController()
    mouseController.mouse_click(left_eye, right_eye)

def mouse_move(nose):
    global mouseController
    
    if mouseController is None:
        mouseController = MouseController()
    mouseController.mouse_move(nose)
