import cv2
import mediapipe as mp
import numpy as np
import serial
import time

ser = serial.Serial("COM6", 9600)
time.sleep(2)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

cap = cv2.VideoCapture(0)

# 🔥 논리 각도 (-90 ~ +90)
PRESET = {
    0: -90,   # 펴짐
    1: 0,     # 반 접힘
    2: 90     # 완전 접힘
}

GRIP_OPEN  = -90
GRIP_CLOSE = 90

def finger_state(wrist, mcp, tip):
    v1 = mcp - wrist
    v2 = tip - mcp
    angle = np.degrees(
        np.arccos(
            np.clip(
                np.dot(v1, v2) /
                (np.linalg.norm(v1) * np.linalg.norm(v2)),
                -1, 1
            )
        )
    )

    if angle > 160:
        return 0
    elif angle > 100:
        return 1
    else:
        return 2

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        lm = result.multi_hand_landmarks[0].landmark
        def pt(i): return np.array([lm[i].x, lm[i].y])

        wrist = pt(0)

        index  = finger_state(wrist, pt(6),  pt(8))
        middle = finger_state(wrist, pt(10), pt(12))
        ring   = finger_state(wrist, pt(14), pt(16))
        pinky  = finger_state(wrist, pt(18), pt(20))

        index_angle = PRESET[index]

        # 🔥 조건 유지
        shoulder = 0 if index_angle == 90 else index_angle

        elbow   = PRESET[middle]
        wrist_a = PRESET[ring]
        gripper = GRIP_CLOSE if pinky == 2 else GRIP_OPEN

        ser.write(f"{shoulder},{elbow},{wrist_a},{gripper}\n".encode())

    cv2.imshow("Hand → Robot Arm", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
ser.close()
cv2.destroyAllWindows()
