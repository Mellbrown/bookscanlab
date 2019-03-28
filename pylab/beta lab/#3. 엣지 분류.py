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

    length = math.sqrt(deltax**2 + deltay**2)
    return angle_deg, length


def points2Contra(points):
    result = []
    for point in points:
        result.append([point])
    return np.array(result, dtype=np.int32)

def conpick(contra):
    return contra[0][0], contra[0][1]

def resolution_info(image): # 사진 해상도 조사
    height, width = image.shape[:2]
    clp = height if height < width else width
    clp_small = clp * 0.3
    clp_half = clp * 0.35
    clp_large = clp * 0.5
    return height, width, clp_small, clp_half, clp_large


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
    height, width, clp_small, clp_half, clp_large = resolution_info(image)
    canvas = np.zeros(shape=(height, width, 3), dtype=np.uint8)

    큰관심콘트라 = []
    큰다각형근사 = []
    소관심콘트라 = []
    소다각형근사 = []
    다각형근사 = []

    다각형의세로선 = []
    소다각형의세로선 = []
    # 확실한 세로 테두리선을 잡음 하지만, 희미한 건 잘 못잡음
    다각형나머지 = []

    for con in contours:
        box, origin, (h, w), angle = box_info(con)
        if h > clp_large and w > clp_large: # 큰사이즈
            다각형 = cv2.approxPolyDP(con, epsilon=2, closed=False)
            큰관심콘트라.append(con)
            큰다각형근사.append(다각형)
            다각형근사.append(다각형)
        elif h > clp_small or w > clp_small: # 중간 사이즈
            vx, vy, x, y = cv2.fitLine(con, cv2.DIST_L2, 0, 0.01, 0.01)
            if vx > 0.3: continue
            다각형 = cv2.approxPolyDP(con, epsilon=3, closed=False)
            소관심콘트라.append(con)
            소다각형근사.append(다각형)
            다각형근사.append(다각형)
    # 관심 엣지 콘트라

    for 다각형 in 큰다각형근사:
        l = len(다각형)
        if not l == 0:
            for i in range(1, l):
                x1, y1 = conpick(다각형[i-1])
                x2, y2 = conpick(다각형[i])
                ang, _ = point2angle(x1, y1, x2, y2)

                if 60 <= ang <= 120 or -120 <= ang <= -60 :
                    다각형의세로선.append(points2Contra([(x1,y1), (x2, y2)]))

    # 다각형 근사 세로선 추출

    for 다각형 in 소다각형근사:
        l = len(다각형)
        if not l == 0:
            for i in range(1, l):
                x1, y1 = conpick(다각형[i-1])
                x2, y2 = conpick(다각형[i])
                ang, length = point2angle(x1, y1, x2, y2)
                if length < clp_half: continue
                if 60 <= ang <= 120 or -120 <= ang <= -60 :
                    소다각형의세로선.append(points2Contra([(x1,y1), (x2, y2)]))

    cv2.drawContours(image, 큰다각형근사, -1, 색.시안, 1) # 책 테두리의 의미
    # cv2.drawContours(image, 소관심콘트라, -1, 색.노, 1) # 희미한 세로선의 의미
    # cv2.drawContours(image, 큰다각형근사, -1, 색.파, 1) #
    # cv2.drawContours(image, 다각형나머지, -1, 색.시안, 2) # 책 테두리의 의미
    # cv2.drawContours(image, 소다각형의세로선, -1, 색.초, 1)
    # cv2.drawContours(image,다각형의세로선,-1,색.빨, 2) #

    # 출력
    return {
        'canvas': canvas,
        'image': image
    }


r = mode.PictureMode(main_proc)
r.run(3)

