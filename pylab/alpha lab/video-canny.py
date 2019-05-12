import cv2
import numpy as np

def isLine (cords, zitter, cnt):
    if len(cords) < cnt: return False

    z = []
    for i in range(1, len(cords)):
        x1, y1 = cords[i-1]
        x2, y2 = cords[i]
        z.append((y2-y1)/(x2-x1))
    print(z)

cap = cv2.VideoCapture('http://192.168.0.43:4747/mjpegfeed')

val4Edge = 30
val4FilterCount = 90
val4angle = 0.3

while True:
    retval, image = cap.read()
    if not retval:
        break

    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)  # 회전
    row, cols = image.shape[:2]

    # 그레이 스케일 먹이고, 가우시안 블루 먹인다.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 엣지 검출 시킨다.
    edged = cv2.Canny(blurred, 0, val4Edge)

    # 윤곽선 검출 한다.
    (_, contours, _) = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    for con in contours:
        isLine(con, 0, 10)

    cv2.imshow("result", image)

    key = cv2.waitKey(25)
    if key == 27:
        break

if cap.isOpened():
    cap.release()
cv2.destroyAllWindows()

