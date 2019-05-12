import math
import random

import cv2
import numpy as np
import 모드
import 색


def lineInfos(cnt, height):
    poly = cv2.approxPolyDP(cnt, epsilon=3, closed=True)
    l = len(poly)
    points = []
    for i in range(0, l):
        x1, y1 = poly[i][0]
        x2, y2 = poly[i + 1 if i + 1 < l else 0][0]
        iy1, iy2 = height - y1, height - y2

        rad = math.atan2((iy2 - iy1), (x2 - x1))
        deg = rad * 180.0 / math.pi
        deg = deg if deg >= 0 else 360 + deg

        length = math.sqrt((x2 - x1) ** 2 + (iy2 - iy1) ** 2)

        points.append(((x1, y1), (x2, y2), deg, length))

        lbi = int((deg + 22.5) / 45)
        lbi = lbi if lbi < 8 else 0
        deg_lb = ["→", "↗", "↑", "↖", "←", "↙", "↓", "↘"]
        print('%s ,%d %d (%d, %d) -> (%d, %d)' % (deg_lb[lbi], deg, length, x1, y1, x2, y2))
    return points

def draw_point (poly, image):
    l = len(poly)
    for i in range(0, l):
        curX, curY = poly[i][0]
        preX, preY = poly[i-1 if i-1 >=0 else l-1][0]
        nxtX, nxtY = poly[i+1 if i+1 < l else 0][0]

        o1 = math.atan2((preY - curY), (preX - curX))
        o2 = math.atan2((nxtY - curY), (nxtX - curX))
        ang = ((o1-o2) * 180/math.pi)
        ang = ang if ang >= 0 else -ang
        ang = ang if ang <= 180 else 360 - ang

        c = 색.검
        if ang < 30: c = 색.시안
        elif ang < 60: c = 색.노
        elif ang < 120: c = 색.빨
        elif ang < 160: c = 색.파
        else: c = 색.검

        cv2.circle(image, (curX, curY), 10, c, 3)
        # cv2.putText(image, "%d" % ang, (curX + random.randrange(0,50), curY+ random.randrange(0,50)), cv2.FONT_HERSHEY_SIMPLEX, 2, 색.빨, 3)


def print2porintAng(x1, y1, x2, y2):
    deltax = x2 - x1
    deltay = y2 - y1

    angle_rad = math.atan2(deltay, deltax)
    angle_deg = angle_rad * 180.0 / math.pi
    length = math.sqrt(deltax ** 2 + deltay ** 2)

    a = int((angle_deg + 180) / 22.5)
    b = ["←", "↖", "↖", "↑", "↑", "↗", "↗", "→", "→", "↘", "↘", "↓", "↓", "↙", "↙", "←", "←"]
    # print('%s %d, (%d, %d) -> (%d, %d)' % ("*" if length == 0 else b[a], length, x1, y1, x2, y2))
    print("*" if length == 0 else b[a], end='')


def ancnt (cnt):
    prevx, prevy = cnt[0][0]
    for i, c in enumerate(cnt):
        x, y = c[0]
        print2porintAng(prevx, prevy, x, y)
        prevx, prevy = x, y

        if i % 10 == 0: print()


def main_proc(image):
    # 이미지 필터링
    height, width = image.shape[:2]
    blur = cv2.GaussianBlur(image, (5, 5), 3)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGRA2GRAY)

    # 콘트라 추출
    edged = cv2.Canny(gray, 40, 50)
    kernel = cv2.getStructuringElement(shape=cv2.MORPH_ELLIPSE, ksize= (3,3))
    dilated = cv2.dilate(edged, kernel, iterations=5)
    (_, contours, _) = cv2.findContours(dilated, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # 콘트라 태깅
    cntrect = []
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        (x, y), (w, h), angle = rect
        box = cv2.boxPoints(rect)
        box = np.int32(box)
        cntrect.append((cnt, w*h, x, y, w, h, angle, rect, box))

    # 제일큰 콘트라
    cntrect.sort(key=lambda o: o[1], reverse=True)
    cnt, area, x, y, w, h, angle, rect, box = cntrect[0]
    # cv2.drawContours(image, [cnt], -1, 색.파, 3)

    # # 콘트라 근사
    # poly = cv2.approxPolyDP(cnt, epsilon=3, closed=True)
    # canvas = np.zeros(shape=(height, width, 3), dtype=np.uint8)
    # cv2.drawContours(canvas, [poly], -1, 색.빨, 5)

    poly = cv2.approxPolyDP(cnt, epsilon=3, closed=True)
    lines = lineInfos(poly, height)
    lines.sort(key = lambda o : o[3], reverse=True)

    for line in lines:
        p1, p2, deg, length = line
        if length < 50 : continue
        cv2.line(image, p1, p2, (random.randrange(100,255,30), random.randrange(100,255,30), random.randrange(100,255,30)), 5)

    return image,


r = 모드.사진(main_proc, 0.3)
r.run()

