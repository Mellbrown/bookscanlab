import cv2

# 이미지를 불러 온다.
image = cv2.imread('./opencv-scanner-test2.jpg')
cap = cv2.VideoCapture('http://192.168.0.43:4747/mjpegfeed')

while True:
    retval, image = cap.read()
    if not retval:
        break

    # 그레이 스케일 먹이고, 가우시안 블루 먹인다.
    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)  # 회전
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 엣지 검출 시킨다.
    edged = cv2.Canny(blurred, 0, 35)
    orig_edged = edged.copy()

    # 윤곽선 검출 한다.
    (_, contours, _) = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    print(len(contours))

    # 윤곽선 그린다.
    cv2.drawContours(image, contours, -1, (255, 0, 0), 1)


    cv2.imshow("Outline.jpg", image)

    key = cv2.waitKey(25)
    if key == 27:
        break

if cap.isOpened():
    cap.release()
cv2.destroyAllWindows()