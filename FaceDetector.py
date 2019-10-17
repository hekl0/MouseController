import dlib
from imutils import face_utils

SHAPE_PREDICTOR_68_FACE_LANDMARKS = 'model/shape_predictor_68_face_landmarks.dat'

faceDetector = None


class FaceDetector:
    def __init__(self):
        self.face_detector = dlib.get_frontal_face_detector()
        self.landmarks_detector = dlib.shape_predictor(SHAPE_PREDICTOR_68_FACE_LANDMARKS)

    def get_faces(self, frame):
        return self.face_detector(frame, 0)

    def get_face_part(self, landmarks, face_part):
        start, end = face_utils.FACIAL_LANDMARKS_IDXS[face_part]
        return landmarks[start:end]

    def get_eyes_and_nose(self, frame, face):
        landmarks = self.landmarks_detector(frame, face)
        landmarks = face_utils.shape_to_np(landmarks)

        left_eye = self.get_face_part(landmarks, 'right_eye')
        right_eye = self.get_face_part(landmarks, 'left_eye')
        nose = self.get_face_part(landmarks, 'nose')

        return left_eye, right_eye, nose


def get_faces(frame):
    global faceDetector

    if faceDetector is None:
        faceDetector = FaceDetector()
    return faceDetector.get_faces(frame)


def get_eyes_and_nose(frame, face):
    global faceDetector

    if faceDetector is None:
        faceDetector = FaceDetector()
    return faceDetector.get_eyes_and_nose(frame, face)
