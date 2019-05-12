import cv2

cap = cv2.VideoCapture('http://192.168.0.43:4747/mjpegfeed')

_, image = cap.read()
cv2.imshow("result", image)

val4Edge = 30
val4FilterCount = 90
val4angle = 0.3

def onChange(pos):
    global val4Edge, val4FilterCount, val4angle
    val4Edge = int(cv2.getTrackbarPos('edge', 'result') )
    val4FilterCount = int(cv2.getTrackbarPos('count', 'result'))
    val4angle = cv2.getTrackbarPos('angle', 'result') / 100

cv2.createTrackbar('edge', 'result', 0, 100, onChange)
cv2.createTrackbar('count', 'result', 0, 200, onChange)
cv2.createTrackbar('angle', 'result', 0, 100, onChange)

cv2.setTrackbarPos('edge', 'result', 30)
cv2.setTrackbarPos('count', 'result', 90)
cv2.setTrackbarPos('angle', 'result', int(0.3 * 100))

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
    (_, contours, _) = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # 윤곽선 그린다.
    cv2.drawContours(image, contours, -1, (255, 0, 0), 1)

    # 세로선 검출해 그린다.
    for con in contours:
        if len(con) < val4FilterCount: continue
        (vx, vy, x, y) = cv2.fitLine(con, cv2.DIST_L2, 0, 0.01, 0.01)
        if vx >= val4angle: continue
        ly = int((-x*vy/vx) + y)
        ry = int(((cols-x) * vy/vx) + y)
        try:
            cv2.line(image, (cols-1, ry), (0, ly), (0,0,255), 2)
        except:
            print("can't draow")

    # 출력
    cv2.imshow("result", image)

    key = cv2.waitKey(25)
    if key == 27:
        break

if cap.isOpened():
    cap.release()
cv2.destroyAllWindows()