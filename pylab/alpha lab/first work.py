import cv2
import numpy as np

cap = cv2.VideoCapture('http://192.168.0.43:8080/video/mjpeg')

_, image = cap.read()
cv2.imshow("result", image)

while True:
    retval, image = cap.read()
    if not retval:
        break
    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)  # 회전
    row, cols = image.shape[:2]
    minRect = (row if row < cols else cols) * 0.3
    maxRect = (row if row < cols else cols) * 0.5

    # 그레이 스케일 먹이고, 가우시안 블루 먹인다.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 엣지 검출 시킨다.
    edged = cv2.Canny(blurred, 0, 30)

    # 윤곽선 검출 한다.
    (_, contours, _) = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    # cv2.drawContours(image, contours, -1, (255, 0, 0), 1)

    # 윤곽선 판별기
    for con in contours:
        # 사각형 테스트
        rect = cv2.minAreaRect(con)
        (origin, area, angle) = rect
        box = cv2.boxPoints(rect)
        box = np.int32(box)

        if area[0] < minRect and area[1] < minRect: continue # 작은거 필터링
        if area[0] > maxRect and area[1] > maxRect:
            cv2.drawContours(image, [con], 0, (255, 255, 0), 1)
        else:

            # 직선 테스트
            (vx, vy, x, y) = cv2.fitLine(con, cv2.DIST_L2, 0, 0.01, 0.01)
            if vx > 0.3: continue # 세로 아닌거 필터링

            ly = int((-x*vy/vx) + y)
            ry = int(((cols-x) * vy/vx) + y)
            try:
                pass
                cv2.line(image, (cols-1, ry), (0, ly), (0,0,255), 1)
            except:
                print("can't draw")


    # 출력
    cv2.imshow("result", cv2.resize(image, dsize=(0,0), fx=1, fy=1))

    key = cv2.waitKey(25)
    if key == 27:
        break

if cap.isOpened():
    cap.release()
cv2.destroyAllWindows()