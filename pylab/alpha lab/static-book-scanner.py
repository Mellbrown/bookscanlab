import cv2

# 이미지를 불러 온다.
image = cv2.imread('./opencv-scanner-test2.jpg')
row, cols = image.shape[:2]

# 그레이 스케일 먹이고, 가우시안 블루 먹인다.
# image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)  # 회전
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# 엣지 검출 시킨다.
edged = cv2.Canny(blurred, 0, 50)
orig_edged = edged.copy()

# 윤곽선 검출 한다.
(_, contours, _) = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)

f = open("result.txt", 'w')
f.write("contours length: %d\n" % len(contours))
for con in contours:
    if len(con) < 80: continue
    (vx, vy, x, y) = cv2.fitLine(con, cv2.DIST_L2, 0, 0.01, 0.01)
    if vx >= 0.5: continue
    print( "vx: %s, vy: %s" % (vx, vy))
    ly = int((-x*vy/vx) + y)
    ry = int(((cols-x) * vy/vx) + y)
    try:
        cv2.line(image, (cols-1, ry), (0, ly), (0,0,255), 2)
    except:
        print("can't draow")

f.close()

# 윤곽선 그린다.
cv2.drawContours(image, contours, -1, (255, 0, 0), 1)


cv2.imshow("Outline.jpg", image)

key = cv2.waitKey()
cv2.destroyAllWindows()