import cv2

# 웹캠 열기 (0 = 기본 웹캠)
cap = cv2.VideoCapture(0)

# 웹캠이 열리지 않았을 경우
if not cap.isOpened():
    print("웹캠을 열 수 없습니다.")
    exit()

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    
    if not ret:
        print("프레임을 가져올 수 없습니다.")
        break

    # 화면에 출력
    cv2.imshow("Webcam", frame)

    # q 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()