import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

def calc_angle(a, b, c):
    """
    a = 손목
    b = MCP 관절
    c = 손가락 끝
    """
    v1 = a - b
    v2 = c - b

    angle = np.degrees(
        np.arccos(
            np.clip(
                np.dot(v1, v2) /
                (np.linalg.norm(v1) * np.linalg.norm(v2)),
                -1.0, 1.0
            )
        )
    )
    return angle

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        lm = result.multi_hand_landmarks[0].landmark

        def pt(i):
            return np.array([lm[i].x, lm[i].y])

        wrist = pt(0)

        index_angle  = calc_angle(wrist, pt(5),  pt(8))
        middle_angle = calc_angle(wrist, pt(9),  pt(12))
        ring_angle   = calc_angle(wrist, pt(13), pt(16))
        pinky_angle  = calc_angle(wrist, pt(17), pt(20))

        text = (
            f"Index: {int(index_angle)}°  "
            f"Middle: {int(middle_angle)}°  "
            f"Ring: {int(ring_angle)}°  "
            f"Pinky: {int(pinky_angle)}°"
        )

        print(text)

        cv2.putText(
            frame,
            text,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        mp_draw.draw_landmarks(
            frame,
            result.multi_hand_landmarks[0],
            mp_hands.HAND_CONNECTIONS
        )

    cv2.imshow("Finger Angle Output", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
