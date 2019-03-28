import cv2
import numpy as np
import 모드
import math
import 색
import 전처리

def divPoly(poly):
    선들 = {"세로": [], "가로": []}

    prevState = '세로'
    prevx, prevy = conpick(poly[0])
    선 = [(prevx, prevy)]

    for p in poly:
        x, y = conpick(p)
        ang, length = point2angle(prevx, prevy, x, y)
        state = "세로" if 60 <= ang <= 120 or -120 <= ang <= -60 else "가로"
        a = int((ang + 180) / 22.5)
        b = ["←", "↖","↖", "↑", "↑", "↗", "↗", "→","→", "↘", "↘", "↓", "↓", "↙","↙", "←", "←"]
        # print('%s %d, (%d, %d) -> (%d, %d)' % ( "*" if length == 0 else b[a], length, prevx, prevy, x, y))

        if state == prevState:
            선.append((x, y))
        else:
            선들[prevState].append(points2Contra(선))
            선 = [(prevx, prevy), (x, y)]


        prevState = state
        (prevx, prevy) = (x, y)

    선들[prevState].append(points2Contra(선))
    if len(선들["세로"][0]) == 1:
        선들["세로"].pop(0)

    return 선들['가로'], 선들['세로']


def point2angle(x1, y1, x2, y2):
    deltax = x2 - x1
    deltay = y2 - y1

    angle_rad = math.atan2(deltay, deltax)
    angle_deg = angle_rad * 180.0 / math.pi

    length = math.sqrt(deltax ** 2 + deltay ** 2)
    return angle_deg, length


def points2Contra(points):
    result = []
    for point in points:
        result.append([point])
    return np.array(result, dtype=np.int32)


def conpick(contra):
    return contra[0][0], contra[0][1]


def resolution_info(image):  # 사진 해상도 조사
    height, width = image.shape[:2]
    clp = height if height < width else width
    clp_small = clp * 0.3
    clp_xsmall = clp * 0.01
    clp_large = clp * 0.5
    return height, width, clp_small, clp_xsmall, clp_large


def box_info(con):  # 박스 조사
    rect = cv2.minAreaRect(con)
    origin, size, angle = rect
    box = cv2.boxPoints(rect)
    box = np.int32(box)
    return box, origin, size, angle


def findLocalMaxima(src):
    kernel = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(11, 11))
    dilate = cv2.dilate(src, kernel)
    localMax = (src == dilate)

    erode = cv2.erode(src, kernel)
    localMax2 = src > erode
    localMax &= localMax2
    points = np.argwhere(localMax == True)
    points[:, [0, 1]] = points[:, [1, 0]]
    return points


def main_proc(image):
    contours = 전처리.get_contours(image)
    height, width, clp_small, clp_xsmall, clp_large = resolution_info(image)
    canvas = np.zeros(shape=(height, width, 3), dtype=np.uint8)

    큰관심콘트라 = []
    소관심콘트라 = []


    큰다각형근사 = []
    소다각형근사 = []
    다각형근사 = []

    큰다각세로 = []
    큰다각가로 = []

    소다각세로 = []
    소다각가로 = []

    for con in contours:
        box, origin, (h, w), angle = box_info(con)
        if h > clp_large and w > clp_large:  # 큰사이즈
            다각형 = cv2.approxPolyDP(con, epsilon=2, closed=True)
            큰관심콘트라.append(con)
            큰다각형근사.append(다각형)
            다각형근사.append(다각형)
        elif h > clp_small or w > clp_small:  # 중간 사이즈
            다각형 = cv2.approxPolyDP(con, epsilon=2, closed=True)
            소관심콘트라.append(con)
            소다각형근사.append(다각형)
            다각형근사.append(다각형)
    # 관심 엣지 콘트라

    for 다각형 in 큰다각형근사:
        가로, 세로 = divPoly(다각형)
        print("")
        큰다각세로.extend(세로)
        큰다각가로.extend(가로)

    print("")
    for 다각형 in 소다각형근사:
        가로, 세로 = divPoly(다각형)
        print("")
        소다각세로.extend(세로)
        소다각가로.extend(가로)

    cv2.drawContours(image, 소다각형근사, -1, 색.시안, 1)
    cv2.drawContours(image, 큰다각형근사, -1, 색.빨, 1)

    # cv2.drawContours(image, 큰다각세로, -1, 색.시안, 1)  # 큰 세로선 후보
    # cv2.drawContours(image, 큰다각가로, -1, 색.파, 1)
    #
    # cv2.drawContours(image, 소다각세로, -1, 색.초, 1)  # 작은 세로선 후보
    # cv2.drawContours(image, 소다각가로, -1, 색.빨, 1)



    # 출력
    return {
        # 'canvas': canvas,
        'image': image
    }


r = 모드.사진(main_proc)
r.run(3)

