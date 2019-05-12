import cv2
import math
import 색
import 모드
import randomcolor

__rand_color = randomcolor.RandomColor()
def rand_color():
    global __rand_color
    return [int(c.lstrip()) for c in reversed(__rand_color.generate(format_='rgb')[0][4:-1].split(","))]

class BookScanner:
    def __init__(m, src):
        height, width = src.shape[:2] # 이미지 크기 구하기

        clpL0, clpL1 = int(0.01 * width), int(0.3 * width)
        clpR0, clpR1 = int(0.7 * width), int(0.99 * width)
        clpT0, clpT1 = int(0.01 * height), int(0.1 * height)
        clpSLen = int(0.4 * height)

        xsm = int(0.1 * width)

        gray = cv2.cvtColor(src, cv2.COLOR_BGRA2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 1)
        edged = cv2.Canny(blur, 35, 125)
        dilate = cv2.dilate(edged, kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=(5, 5)), iterations=3)

        (_, contours, _) = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        contours.sort(key=lambda o : cv2.arcLength(o, closed=False), reverse=True)

        def size_filter(cnt):
            x, y, width, height = cv2.boundingRect(cnt)
            return width > xsm or height > xsm

        lg_contours = [contour for contour in contours if size_filter(contour)]
        lg_polies = [cv2.approxPolyDP(contour, 10, False) for contour in lg_contours]
        cv2.drawContours(src, lg_polies, -1, 색.초, 5)

        corners = []
        for contour in lg_polies:
            sub = []
            l = len(contour)
            for i in range(0, l -2):
                x1, y1 = contour[i][0]
                x0, y0 = contour[i+1][0]
                x2, y2 = contour[i+2][0]
                ang0 = abs((math.atan2(y1 - y0, x1 - x0) - math.atan2(y0 - y2, x0 - x1)) * 180 / math.pi)
                if ang0 < 120:
                    cv2.circle(src, (x0, y0), 10, 색.빨, 8)
                elif ang0 < 160:
                    cv2.circle(src, (x0, y0), 10, 색.파, 8)
                else:
                    cv2.circle(src, (x0, y0), 10, 색.검, 8)
            corners.append(sub)


        lg_left_side_candy = []
        lg_right_side_candy = []
        for contour in lg_polies:
            l = len(contour)
            for i in range(0, l -1):
                x1, y1 = contour[i][0]
                x2, y2 = contour[i+1][0]

                delX, delY = x2-x1, y2-y1

                deg = abs(math.atan2(delY, delX) * 180.0 / math.pi)
                ln = math.sqrt(delX ** 2 + delY ** 2)
                if clpL0 <= x1 <= clpL1 and clpL0 <= x2 <= clpL1 and 80 <= deg <= 100 and  clpSLen <= ln:
                    cv2.line(src, (x1, y1), (x2, y2), 색.빨, 8)
                    lg_left_side_candy.append((x1, y1, x2, y2))
                elif clpR0 <= x1 <= clpR1 and clpR0 <= x2 <= clpR1 and 80 <= deg <= 100 and  clpSLen <= ln:
                    cv2.line(src, (x1, y1), (x2, y2), 색.파, 8)
                    lg_right_side_candy.append((x1, y1, x2, y2))

        cv2.line(src, (clpL0, 0), (clpL0, height), 색.노, 8)
        cv2.line(src, (clpL1, 0), (clpL1, height), 색.노, 8)

        cv2.line(src, (clpR0, 0), (clpR0, height), 색.노, 8)
        cv2.line(src, (clpR1, 0), (clpR1, height), 색.노, 8)

        cv2.line(src, (0, clpT0), (width, clpT0), 색.노, 8)
        cv2.line(src, (0, clpT1), (width, clpT1), 색.노, 8)

        m.out = [src, dilate]




def main_proc(src):
    return BookScanner(src).out


r = 모드.사진(main_proc, 600)
r.run()
