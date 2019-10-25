import cv2
import FaceDetector
import MouseController
import time
import math

CAM_W = 640
CAM_H = 480

FRAME_RATE = 30

if __name__ == '__main__':
    vid = cv2.VideoCapture(0)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_W)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_H)

    prev = 0
    while True:
        if time.time() - prev <= 1./FRAME_RATE:
            continue
        else:
            prev = time.time()

        _, frame = vid.read()
        frame = cv2.flip(frame, 1)

        # Remove color for optimization
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Find a face amd get eyes and nose from it
        faces = FaceDetector.get_faces(gray_frame)
        if len(faces) == 0:
            cv2.imshow('Test', frame)
            key = cv2.waitKey(1)
            if key == 27:
                break
            continue
        leftEye, rightEye, nose, mouth, right_eyebrow, left_eyebrow = FaceDetector.get_essential(gray_frame, faces[0])

        # Show eyes
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 255), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 255), 1)
        lower_leftEye = (leftEye[0,0], leftEye[0,1])
        lower_rightEye = (rightEye[3,0], rightEye[3,1])
        left_edge_nose = (nose[4,0], nose[4,1])
        right_edge_nose = (nose[8,0], nose[8,1])
        top_of_nose = (nose[0,0], nose[0,1])
        right_eyebrow_point = (right_eyebrow[4,0], right_eyebrow[4,1])
        left_eyebrow_point = (left_eyebrow[0,0], left_eyebrow[0,1])
        cv2.line(frame,left_edge_nose, top_of_nose, (255, 0, 0), 2)
        cv2.line(frame,right_edge_nose, top_of_nose, (255, 0, 0), 2)
        cv2.line(frame,lower_rightEye, right_eyebrow_point, (255, 0, 0), 2)
        cv2.line(frame,lower_leftEye, left_eyebrow_point, (255, 0, 0), 2)

        # Check eyes and click
        MouseController.mouse_click(rightEye, leftEye, right_eyebrow, left_eyebrow, mouth)

        # Check mouth and scroll
        MouseController.mouse_scroll(nose,mouth)
        
        # Move mouse according to nose position
        # nose_center = (nose[3, 0], nose[3, 1])
        # MouseController.mouse_move(nose_center)
        
        # Show mouth
        upper_lips = (mouth[9,0], mouth[9,1])
        under_lips = (mouth[3,0], mouth[3,1])
        left_of_lips = (mouth[0,0], mouth[0,1])
        right_of_lips = (mouth[6,0], mouth[6,1])
        cv2.line(frame, upper_lips, under_lips, (255, 0, 0), 2)
        cv2.line(frame, left_of_lips, right_of_lips, (255, 0, 0), 2 )

        cv2.imshow("Test", frame)

        # Press `Esc` key to exit
        key = cv2.waitKey(1)
        if key == 27:
            break
