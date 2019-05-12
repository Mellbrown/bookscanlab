import cv2
import math
import numpy as np
import 색
import 모드
import matplotlib.pyplot as plt

plt.ion()

def cany_con_can(src, t1, t2, thick, ksize = None, it = None, sw = False):
    edged = cv2.Canny(src, t1, t2)
    dilate = None
    if sw: dilate = cv2.dilate(edged, kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=ksize), iterations=it)
    (_, contours, _) = cv2.findContours(dilate if sw else edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    canvas = np.zeros(shape=(src.shape[0], src.shape[1], 3), dtype=np.uint8)
    cv2.drawContours(canvas, contours, -1, 색.회색, thick)
    return edged, contours, canvas, dilate


class 콘트라분석:
    def __init__(self, contour):
        self.contour = contour
        verlines = {}
        horlines = {}
        for con in contour:
            x, y = con[0]
            if x not in verlines: verlines[x] = (x, [])
            if y not in horlines: horlines[y] = (y, [])
            verlines[x][1].append(y)
            horlines[y][1].append(x)
        for x in verlines.keys(): print(x)



def 테이크1(src):
    height, width = src.shape[:2]  # 이미지 크기 구하기
    mn = min(height, width)
    xxsm = int(mn * 0.01)
    xsm = int(mn * 0.05)
    sm = int(mn * 0.1)
    md = int(mn * 0.4)

    gray = cv2.cvtColor(src, cv2.COLOR_BGRA2GRAY)
    gblur = cv2.GaussianBlur(gray, (5, 5), 1)
    mblurWeek = cv2.medianBlur(gblur, ksize=7)

    cany, contours, canvas, dilate = cany_con_can(mblurWeek, 10, 200, 1, (3,3), 1, False)

    def size_filter(cnt):
        x, y, width, height = cv2.boundingRect(cnt)
        return width * height
    contours.sort(key=size_filter, reverse = True)
    contour = contours[0]
    # 콘트라분석(contour)

    # cv2.drawContours(canvas,[contour], -1, 색.흰, 1)
    diff = xxsm * 2
    _deg = lambda i: math.atan2(contour[i + diff, 0, 1] - contour[i, 0, 1],
                                contour[i + diff, 0, 0] - contour[i, 0, 0]) * 180.0 / math.pi + 180
    # prevDeg = 0
    # for i in range(0, len(contour) - diff):
    #     deg = int(round(_deg(i)))
    #     if not abs(prevDeg - deg) <= 20:
    #         cv2.circle(canvas, (contour[i,0,0], contour[i,0,1]), 10, 색.빨, 8,)
    #     prevDeg = deg
    degs = [_deg(i) for i in range(0, len(contour) - diff)]
    def deltadeg(d1, d2):
        delta = abs(d1 - d2)
        delta = delta if delta < 180 else 360 - delta
        return delta

    difDeg = [int(deltadeg(degs[i], degs[i+1])) for i in range(0, len(degs) -1)]
    counting = {}
    for (i,d) in enumerate(difDeg):
        if d not in counting: counting[d] = [d, 0]
        counting[d][1] += 1
        if 1 < d < 30:
            cv2.circle(canvas, (contour[i][0][0], contour[i][0][1]), 3, 색.초, 3)
        elif 30 < d:
            cv2.circle(canvas, (contour[i][0][0], contour[i][0][1]), 20, 색.빨, 3)

    print(sorted(counting.values(), key= lambda o: o[1], reverse=True))
    plt.clf()
    plt.yticks(np.arange(0, 360, 5))
    plt.plot(difDeg)
    plt.pause(0.0001)
    plt.show()

    return [canvas]

def 테이크2 (src):
    height, width = src.shape[:2]  # 이미지 크기 구하기
    mn = min(height, width)
    xxsm = int(mn * 0.01)
    xsm = int(mn * 0.05)
    sm = int(mn * 0.1)
    md = int(mn * 0.4)

    gray = cv2.cvtColor(src, cv2.COLOR_BGRA2GRAY)
    gblur = cv2.GaussianBlur(gray, (5, 5), 1)
    mblurWeek = cv2.medianBlur(gblur, ksize=7)

    cany, contours, canvas, dilate = cany_con_can(mblurWeek, 10, 200, 1, (3,3), 1, False)

    def size_filter(cnt):
        x, y, width, height = cv2.boundingRect(cnt)
        return width * height
    contours.sort(key=size_filter, reverse = True)
    contour = contours[0]

    class 기울기표현:
        def __init__(self, contour):
            self.contour = contour
            self.canvas = self.result_canvas(self.두배씩())

        def 두배씩(self):
            diff, l, result = 1, len(self.contour) - 1, []
            while diff <= l:
                degrees, x = [], 0
                while x + diff <= l:
                    deg = self.deg(x, x + diff)
                    degrees.append(deg)
                    x += diff
                result.append((diff, degrees))
                diff *= 2
            return result

        def result_canvas(self, result):
            width = len(result[0][1])
            height = 360
            canvas = np.zeros(shape=(height, width), dtype=np.uint8)
            for sub in result:
                diff, degrees = sub
                start = 0
                for deg in degrees:
                    for x in range(start, start +diff):
                        canvas[height-int(deg)][x] += 100
                    start += diff
            return canvas

        def deg(self, idxP1, idxP2):
            p1x, p1y = self.contour[idxP1][0]
            p2x, p2y = self.contour[idxP2][0]
            return math.atan2(p2y-p1y, p2x-p1x) * 180.0 / math.pi + 180

    can_기울기 = 기울기표현(contour).canvas
    return [can_기울기]

r = 모드.사진(테이크2, 0)
r.run()

