import numpy as np
import pyautogui
import os

EAR_THRESHOLD = 0.25

mouseController = None


class MouseController:
    def __init__(self):
        self.left_mouse_down = False
        self.right_mouse_down = False

    def eye_aspect_ratio_algorithm(self, eye):
        height1 = np.linalg.norm(eye[1] - eye[5])
        height2 = np.linalg.norm(eye[2] - eye[4])
        width = np.linalg.norm(eye[0] - eye[3])
        return (height1 + height2) / (2.0 * width)

    def mouse_click(self, left_eye, right_eye):
        left_EAR = self.eye_aspect_ratio_algorithm(left_eye)
        right_EAR = self.eye_aspect_ratio_algorithm(right_eye)

        print(left_EAR, right_EAR)

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


def mouse_click(left_eye, right_eye):
    global mouseController

    if mouseController is None:
        mouseController = MouseController()
    mouseController.mouse_click(left_eye, right_eye)
