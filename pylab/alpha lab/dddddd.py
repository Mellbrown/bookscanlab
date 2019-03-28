import cv2
import numpy as np

img = cv2.imread('./test1.jpg')
cv2.imshow("result", img)

val4Edge = 30
val4FilterCount = 90
val4angle = 0.3
ar = 10

def onChange(pos):
    global ar
    ar = int(cv2.getTrackbarPos('ar', 'result') )


cv2.createTrackbar('ar', 'result', 0, 100, onChange)


cv2.setTrackbarPos('ar', 'result', ar)


while True:
    image = img.copy()

    # image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)  # 회전
    row, cols = image.shape[:2]
    raiot = row if row < cols else cols

    # 그레이 스케일 먹이고, 가우시안 블루 먹인다.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 엣지 검출 시킨다.
    edged = cv2.Canny(blurred, 0, val4Edge)

    # 윤곽선 검출 한다.
    (_, contours, _) = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # 세로선 검출해 그린다.
    for con in contours:
        rect = cv2.minAreaRect(con)
        (origin, area, angle) = rect
        if area[0] < ar/100*raiot and area[1] < ar/100*raiot: continue
        box = cv2.boxPoints(rect)
        box = np.int32(box)
        cv2.drawContours(image, [box], 0, (0, 0, 255), 1)

    # 출력
    cv2.imshow("result", image)

    key = cv2.waitKey(25)
    if key == 27:
        break

cv2.destroyAllWindows()