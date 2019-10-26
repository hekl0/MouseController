import numpy as np
import pyautogui
import os
import screeninfo
import math

EAR_THRESHOLD = 0.25
BOUND_RADIUS = 10
SCREEN_W = screeninfo.get_monitors()[0].width
SCREEN_H = screeninfo.get_monitors()[0].height

mouseController = None


class MouseController:
    def __init__(self):
        self.last_left = 0
        self.last_right = 0
        self.left_mouse_down = False
        self.right_mouse_down = False
        self.scroll_up = False
        self.scroll_down = False
        self.last_nose_position = 0
        self.nose_vertical_length = 0
        self.origin_point = None

    def get_center(self):
        return self.origin_point

    def eye_aspect_ratio_algorithm(self, eye):
        height1 = np.linalg.norm(eye[1] - eye[5])
        height2 = np.linalg.norm(eye[2] - eye[4])
        width = np.linalg.norm(eye[0] - eye[3])
        return (height1 + height2) / (2.0 * width)

    def mouse_click(self, right_eye, left_eye, right_eyebrow, left_eyebrow, mouth):
        mouth_ratio =  (mouth[9,1] - mouth[3,1])/(mouth[6,0] - mouth[0,0])
        if mouth_ratio >= 0.5: 
            return 
       
        lower_leftEye = (left_eye[0,0], left_eye[0,1])
        lower_rightEye = (right_eye[3,0], right_eye[3,1])
        right_eyebrow_point = (right_eyebrow[4,0], right_eyebrow[4,1])
        left_eyebrow_point = (left_eyebrow[0,0], left_eyebrow[0,1])
        left = math.sqrt( (lower_rightEye[0] - right_eyebrow_point[0])**2 + (lower_rightEye[1] - right_eyebrow_point[1])**2  )
        right = math.sqrt( (lower_leftEye[0] - left_eyebrow_point[0])**2 + (lower_leftEye[1] - left_eyebrow_point[1])**2 )
        
        if self.last_left == 0:
            self.last_left = left
        if self.last_right == 0:
            self.last_right = right

        if self.left_mouse_down and left >= self.last_left:
            self.left_mouse_down = False
            os.system('xdotool mouseup 1')
        if self.right_mouse_down and right >= self.last_right:
            self.right_mouse_down = False
            os.system('xdotool mouseup 3')

        if not self.left_mouse_down and not self.right_mouse_down:
            if left < right*9/10 and left < self.last_left:
                self.left_mouse_down = True
                # os.system('xdotool mousedown 1') 
                print('LEFT')
            elif right < left*9/10 and right < self.last_right:
                self.right_mouse_down = True
                # os.system('xdotool mousedown 3')
                print('RIGHT')
        
        self.last_left = left
        self.last_right = right

    def mouse_move(self, nose):
        if self.origin_point == None:
            self.origin_point = nose
            return
        x = nose[0] - self.origin_point[0]
        y = nose[1] - self.origin_point[1]
        if (x**2 + y**2 > BOUND_RADIUS**2):
            os.system('xdotool mousemove_relative -- {} {}'.format(x, y))

    def mouse_scroll(self, nose, mouth):
        mouth_ratio =  (mouth[9,1] - mouth[3,1])/(mouth[6,0] - mouth[0,0])
        if mouth_ratio < 0.5: 
            self.last_nose_position = 0
            return 

        if self.last_nose_position == 0: 
            self.last_nose_position = nose[6,1]
            self.nose_vertical_length = nose[7,1] - nose[1,1]

        if nose[6,1] < self.last_nose_position - self.nose_vertical_length/7:
            self.scroll_down = False
            self.scroll_up = True
        elif nose[6,1] > self.last_nose_position + self.nose_vertical_length/7:
            self.scroll_down = True
            self.scroll_up = False
        else:
            self.scroll_down = False
            self.scroll_up = False

        if self.scroll_down:
            os.system('xdotool key Down') 
            
        if self.scroll_up:
            os.system('xdotool key Up') 

def mouse_click(right_eye, left_eye, right_eyebrow, left_eyebrow, mouth):
    global mouseController

    if mouseController is None:
        mouseController = MouseController()
    mouseController.mouse_click(right_eye, left_eye, right_eyebrow, left_eyebrow, mouth)

def mouse_scroll(nose, mouth):
    global mouseController

    if mouseController is None:
        mouseController = MouseController()
    mouseController.mouse_scroll(nose, mouth)

def mouse_move(nose):
    global mouseController
    
    if mouseController is None:
        mouseController = MouseController()
    mouseController.mouse_move(nose)

def get_center():
    global mouseController
    
    if mouseController is None:
        mouseController = MouseController()
    return mouseController.get_center()

def get_radius():
    return BOUND_RADIUS