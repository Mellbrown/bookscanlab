import cv2

img = cv2.imread('./test1.jpg')
cv2.imshow("result", img)

val4Edge = 30
val4FilterCount = 90
val4angle = 0.3

# def onChange(pos):
#     global val4Edge, val4FilterCount, val4angle
#     val4Edge = int(cv2.getTrackbarPos('edge', 'result') )
#     val4FilterCount = int(cv2.getTrackbarPos('count', 'result'))
#     val4angle = cv2.getTrackbarPos('angle', 'result') / 100
#
# cv2.createTrackbar('edge', 'result', 0, 100, onChange)
# cv2.createTrackbar('count', 'result', 0, 200, onChange)
# cv2.createTrackbar('angle', 'result', 0, 100, onChange)
#
# cv2.setTrackbarPos('edge', 'result', val4Edge)
# cv2.setTrackbarPos('count', 'result', val4FilterCount)
# cv2.setTrackbarPos('angle', 'result', int(val4angle * 100))


image = img.copy()

# image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)  # 회전
row, cols = image.shape[:2]

# 그레이 스케일 먹이고, 가우시안 블루 먹인다.
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# 엣지 검출 시킨다.
edged = cv2.Canny(blurred, 0, val4Edge)

# 윤곽선 검출 한다.
(_, contours, _) = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)

s1000 = [con for con in contours if len(con) >= 1000]
s500= [con for con in contours if 1000 > len(con) >= 500]
s100 = [con for con in contours if 500 > len(con) >= 100]
s10 = [con for con in contours if 100 > len(con) >= 10]
sele = [con for con in contours if 10 > len(con)]

# 윤곽선 그린다.
# cv2.drawContours(image, s1000, -1, (0, 0, 255), 2)
cv2.drawContours(image, s500, -1, (0, 255, 0), 2)
cv2.drawContours(image, s100, -1, (255, 0, 0), 2)
# cv2.drawContours(image, s10, -1, (0, 255, 255), 2)
# cv2.drawContours(image, sele, -1, (255, 255, 0), 2)

# 세로선 검출해 그린다.
f = open("result.txt", 'w')
for con in contours:
    l = len(con)
    f.write("<%d>\n" % l)
    for cord in con:
        x, y = cord[0]
        f.write("%d,%d\n" % (x, y))
    f.write("\n")

# 출력
cv2.imshow("result", image)

key = cv2.waitKey()
cv2.destroyAllWindows()