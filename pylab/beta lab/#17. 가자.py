import cv2
import numpy as np
import 색
import 모드
import matplotlib.pyplot as plt


def 기릿(src):
    height, width = src.shape[:2]  # 이미지 크기 구하기
    mn = min(height, width)
    xxsm = int(mn * 0.01)
    xsm = int(mn * 0.05)
    sm = int(mn * 0.1)
    md = int(mn * 0.4)

    gblur = cv2.GaussianBlur(src, (7, 7), 1)
    mblur = cv2.medianBlur(gblur, 7)
    mgray = cv2.cvtColor(mblur, cv2.COLOR_BGR2GRAY)
    mcany = cv2.Canny(mgray, 30, 40)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=(3, 3))
    dilate = cv2.dilate(mcany, kernel=kernel, iterations=1)
    contours, _ = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    canvas = np.zeros(shape=(height, width), dtype=np.uint8)

    for con in contours:
        rect = cv2.minAreaRect(con)
        (origin, area, angle) = rect
        box = cv2.boxPoints(rect)
        box = np.int32(box)

        if area[0] < xsm and area[1] < xsm: continue  # 작은거 필터링

        cv2.drawContours()

    return {
        'original' : src,
        'dilate' : dilate,
        'canvas' : canvas
    }

r = 모드.사진(기릿, 600)
r.run()