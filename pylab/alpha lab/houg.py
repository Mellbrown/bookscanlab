import cv2
import numpy as np

img = cv2.imread('./test1.jpg')
cv2.imshow("result", img)

val4Edge = 30
val4FilterCount = 90
val4angle = 0.3

image = img.copy()
row, cols = image.shape[:2]

# 그레이 스케일 먹이고, 가우시안 블루 먹인다.
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# 엣지 검출 시킨다.
edges = cv2.Canny(blurred, 0, val4Edge)

lines = cv2.HoughLines(edges, rho = 1, theta = np.pi / 180.0, threshold = 100)

for line in lines:
    rho, theta = line[0]
    c = np.cos(theta)
    s = np.sin(theta)
    x0 = c * rho
    y0 = s * rho
    x1 = int(x0 + 1000 * (-s))
    y1 = int(y0 + 1000 * (c))
    x2 = int(x0 - 1000 * (-s))
    y2 = int(y0 - 1000 * (c))
    cv2.line(image, (x1,y1), (x2, y2), (0,0,255), 1)

# 출력
cv2.imshow("result", image)

key = cv2.waitKey()
cv2.destroyAllWindows()