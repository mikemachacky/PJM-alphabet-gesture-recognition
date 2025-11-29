import cv2
import mediapipe as mp
import numpy as np

class Camera:
    """Wrapper kamery i MediaPipe — zwraca surową klatkę i (opcjonalnie) landmarki."""
    def __init__(self, device=0):
        self.cap = cv2.VideoCapture(device)
        mp_hands = mp.solutions.hands
        self.hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

    def read(self):
        ret, frame = self.cap.read()
        if not ret:
            return False, None, None
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)
        landmarks = None
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand.landmark])
            # narysuj na oryginalnej klatce
            mp.solutions.drawing_utils.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
        return True, frame, landmarks

    def release(self):
        self.cap.release()
