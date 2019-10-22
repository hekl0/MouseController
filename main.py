import cv2
import FaceDetector
import MouseController

SCREEN_W = 1920
SCREEN_H = 1080
CAM_W = 640
CAM_H = 480
ANCHOR_POINT = (CAM_W//2, CAM_H//3)

if __name__ == '__main__':
    vid = cv2.VideoCapture(0)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_W)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_H)

    while True:
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
        leftEye, rightEye, nose = FaceDetector.get_eyes_and_nose(gray_frame, faces[0])
        mouth = FaceDetector.get_mouth(gray_frame, faces[0])

        # Show eyes
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 255), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 255), 1)

        # Check eyes and click
        MouseController.mouse_click(leftEye, rightEye)

        # Check mouth and scroll
        MouseController.nose_upper_limit = nose[6,1] + 15
        MouseController.nose_lower_limit = nose[6,1] - 15
        MouseController.mouse_scroll(nose,mouth)

        # Show nose
        nose_point = (nose[3, 0], nose[3, 1])
        cv2.line(frame, ANCHOR_POINT, nose_point, (255, 0, 0), 2)
        
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
