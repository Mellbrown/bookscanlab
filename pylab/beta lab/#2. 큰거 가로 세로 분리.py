import cv2
import numpy as np
import 모드 as mode
import math
import 색


def point2angle (x1, y1, x2, y2):
    deltax = x2 - x1
    deltay = y2 - y1

    angle_rad = math.atan2(deltay, deltax)
    angle_deg = angle_rad * 180.0 / math.pi
    return angle_deg


def resolution_info(image): # 사진 해상도 조사
    height, width = image.shape[:2]
    clp = height if height < width else width
    clp_small = clp * 0.3
    clp_large = clp * 0.5
    return height, width, clp_small, clp_large


def box_info (con): # 박스 조사
    rect = cv2.minAreaRect(con)
    origin, size, angle = rect
    box = cv2.boxPoints(rect)
    box = np.int32(box)
    return box, origin, size, angle


def findLocalMaxima(src):
    kernel = cv2.getStructuringElement(shape= cv2.MORPH_RECT, ksize= (11,11))
    dilate = cv2.dilate(src, kernel)
    localMax = (src == dilate)

    erode = cv2.erode(src, kernel)
    localMax2 = src > erode
    localMax &= localMax2
    points = np.argwhere(localMax == True)
    points[:, [0, 1]] = points[:,[1,0]]
    return points


def main_proc(image, contours):
    height, width, clp_small, clp_large = resolution_info(image)
    canvas = np.zeros(shape=(height, width), dtype=np.uint8)


    관심엣지 = []
    다각형근사 = []
    for con in contours:
        box, origin, (h, w), angle = box_info(con)

        if h > clp_large and w > clp_large: # 큰사이즈
            관심엣지.append(con)
            cv2.drawContours(image, [con], -1, 색.시안, 2)
            다각형근사.append(cv2.approxPolyDP(con, epsilon=20, closed=False))

        elif h > clp_small or w > clp_small: # 중간 사이즈
            # 세로선
            vx, vy, x, y = cv2.fitLine(con, cv2.DIST_L2, 0, 0.01, 0.01)
            if vx > 0.3: continue
            관심엣지.append(con)
            cv2.drawContours(image, [con], -1, 색.빨, 2)
            다각형근사.append(cv2.approxPolyDP(con, epsilon=20, closed=False))

    다각형의수직 = []
    for poly in 다각형근사:
        l = len(poly)
        if l == 0:
            print("x")
        else:
            for i in range(1, l):
                x1, y1 = poly[i-1][0]
                x2, y2 = poly[i][0]
                ang = point2angle(x1, y1, x2, y2)

                if 60 <= ang <= 120 or -120 <= ang <= -60 :
                    다각형의수직.append(np.array([[(x1, y1)],[(x2, y2)]], dtype=np.int32))

    cv2.drawContours(image, 다각형의수직, -1, 색.파, 2)

    # 출력
    return {
        'image': image,
        'canvas': canvas
    }


r = mode.PictureMode(main_proc)
r.run(3)

