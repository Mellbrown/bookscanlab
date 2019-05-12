import cv2
import numpy as np
import 색
import 모드
import matplotlib.pyplot as plt
import tkinter as Tk

plt.ion()

class SmoothBall:
    def __init__(self, ):
        self.direction
        self.speed
        self.angleDrag

def cany_con_can(src, t1, t2, thick, ksize = None, it = None, sw = False):
    edged = cv2.Canny(src, t1, t2)
    dilate = None
    if sw: dilate = cv2.dilate(edged, kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=ksize), iterations=it)
    (contours, _) = cv2.findContours(dilate if sw else edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    canvas = np.zeros(shape=(src.shape[0], src.shape[1], 3), dtype=np.uint8)
    cv2.drawContours(canvas, contours, -1, 색.회색, thick)
    return edged, contours, canvas, dilate


def 테이크3 (src):
    height, width = src.shape[:2]  # 이미지 크기 구하기
    mn = min(height, width)
    xxsm = int(mn * 0.01)
    xsm = int(mn * 0.05)
    sm = int(mn * 0.1)
    md = int(mn * 0.4)

    gray = cv2.cvtColor(src, cv2.COLOR_BGRA2GRAY)
    gblur = cv2.GaussianBlur(gray, (5, 5), 1)
    mblurWeek = cv2.medianBlur(gblur, ksize=7)

    cany, contours, canvas, dilate = cany_con_can(mblurWeek, 10, 200, 3, (5,5), 2, False)
    wfile = open('./contours_smaple.txt', 'w')
    print(contours, file=wfile)
    wfile.close()

    def size_filter(cnt):
        x, y, width, height = cv2.boundingRect(cnt)
        return width * height
    contours.sort(key=size_filter, reverse = True)
    contour = contours[0]

    poly = cv2.approxPolyDP(contour, 2, False)
    cv2.drawContours(canvas, [poly], -1, 색.흰, 3)

    for point in poly:
        p = point[0]
        cv2.circle(canvas, (p[0], p[1]), 1, 색.빨, 5)

    # xes = [points[0][0] for points in poly]
    # yes = [points[0][1] for points in poly]

    # plt.clf()
    # plt.plot(xes, 'r')
    # plt.plot(yes, 'b')
    # plt.pause(0.0001)
    # plt.show()

    return [canvas]


r = 모드.사진(테이크3, 600)
r.run()

