import cv2
import math
import numpy as np
import 색
import 모드


class BookCurv:
    @staticmethod
    def merge(curves, pntRngs):
        pass

    def __init__(self, pointRange):
        self.pointData = []
        self.bound

    def add(self, pointRng):
        hor = []
        if len(pointRng) == 3:
            y, x1, x2 = pointRng
            hor.append((x1, x2))
        else:
            y, x = pointRng
            hor.append(x)
    def culling(self):
        pass

class CurvDetector:
    def __init__(self, cany):
        self.cany = cany
        self.height, self.width = cany.shape

        survivalFilter = [None] * self.width
        survivors = set()
        # for y in range(0, self.height):
        #     nxtSurvivalFilter = [None] * self.width
        #     feedingRange = self.getPointRangeList(y)
        #     if len(feedingRange) != 0:
        #         closeCurv = [set(cursor[startx-1:endx+2]) for (y, startx, endx) in lstPntRng]
        #
        #         mergeGroup = self.getMergeGroup(lstPntRng, closeCurv)
        #         mergedNode = [BookCurv.merge(mg['closeCurv'], mg['pntRange']) for mg in mergeGroup]
        #     else:
        #         for survivor :culling


    def getMergeGroup(self, lstPntRng, closeCurv):
        lstMerge = []
        mer = {
            'pntRng': [lstPntRng[0]],
            'closeCurv': closeCurv[0]
        }
        for i in range(1, len(closeCurv)):
            if len(mer['closeCurv'] & closeCurv[i]) > 0:
                mer['pntRng'].append(lstPntRng[i])
                mer['closeCurv'] |= closeCurv[i]
            else:
                lstMerge.append(mer)
                mer = {
                    'pntRng': [lstPntRng[i]],
                    'closeCurv': closeCurv[i]
                }
        lstMerge.append(mer)
        return lstMerge

    def getPointRangeList(self, y):
        lstPntRng = []
        startx = None
        for x in range(0, self.height):
            o = self.cany[y, x]
            if o == 1 and startx is None:
                startx = x
            elif o != 1 and startx is not None:
                lstPntRng.append((y, startx, x))
                startx = None
        return lstPntRng

    def findCloserNode(self, y, startx, endx):
        curves = set(self.cursor[startx-1:endx+2])
        BookCurv.merge(curves, (y, startx, endx))




def 기본필터(src):
    gray = cv2.cvtColor(src, cv2.COLOR_BGRA2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 1)
    edged = cv2.Canny(blur, 35, 125)
    dilate = cv2.dilate(edged, kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=(5, 5)), iterations=3)

    return gray, blur, edged, dilate




def 가이드라인그리기(src, width, height, clpL0, clpL1, clpR0, clpR1, clpT0, clpT1):
    cv2.line(src, (clpL0, 0), (clpL0, height), 색.노, 8)
    cv2.line(src, (clpL1, 0), (clpL1, height), 색.노, 8)
    cv2.line(src, (clpR0, 0), (clpR0, height), 색.노, 8)
    cv2.line(src, (clpR1, 0), (clpR1, height), 색.노, 8)
    cv2.line(src, (0, clpT0), (width, clpT0), 색.노, 8)
    cv2.line(src, (0, clpT1), (width, clpT1), 색.노, 8)


def 윤곽선검출(edged):
    (_, contours, _) = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    contours.sort(key=lambda o: cv2.arcLength(o, closed=False), reverse=True)
    return contours

def 윤곽선가공(contours, xsm):
    def size_filter(cnt):
        x, y, width, height = cv2.boundingRect(cnt)
        return width > xsm or height > xsm
    lg_contours = [contour for contour in contours if size_filter(contour)]
    lg_polies = [cv2.approxPolyDP(contour, 10, False) for contour in lg_contours]
    return lg_contours, lg_polies

def 다각형근사에서코너찾기(polies, src):
    corners = []
    for contour in polies:
        sub = []
        l = len(contour)
        for i in range(0, l - 2):
            x1, y1 = contour[i][0]
            x0, y0 = contour[i + 1][0]
            x2, y2 = contour[i + 2][0]
            ang0 = abs((math.atan2(y1 - y0, x1 - x0) - math.atan2(y0 - y2, x0 - x1)) * 180 / math.pi)
            if src is not None:
                if ang0 < 120:
                    cv2.circle(src, (x0, y0), 10, 색.빨, 8)
                elif ang0 < 160:
                    cv2.circle(src, (x0, y0), 10, 색.파, 8)
                else:
                    cv2.circle(src, (x0, y0), 10, 색.검, 8)
        corners.append(sub)
    return corners


def 다각형근사에서양사이드후보선검출하기(polies, clpL0, clpL1, clpR0, clpR1, clpSLen, src):
    lg_left_side_candy = []
    lg_right_side_candy = []
    for contour in polies:
        l = len(contour)
        for i in range(0, l - 1):
            x1, y1 = contour[i][0]
            x2, y2 = contour[i + 1][0]
            delx, dely = x2 - x1, y2 - y1
            deg = abs(math.atan2(dely, delx) * 180.0 / math.pi)
            ln = math.sqrt(delx ** 2 + dely ** 2)
            if clpL0 <= x1 <= clpL1 and clpL0 <= x2 <= clpL1 and 80 <= deg <= 100 and clpSLen <= ln:
                if src is not None:
                    cv2.line(src, (x1, y1), (x2, y2), 색.빨, 9)
                lg_left_side_candy.append((x1, y1, x2, y2))
            elif clpR0 <= x1 <= clpR1 and clpR0 <= x2 <= clpR1 and 80 <= deg <= 100 and clpSLen <= ln:
                if src is not None:
                    cv2.line(src, (x1, y1), (x2, y2), 색.파, 9)
                lg_right_side_candy.append((x1, y1, x2, y2))
    return lg_left_side_candy, lg_right_side_candy


def 다각형근사색인(polies):
    line_info = []
    for contour in polies:
        l = len(contour)
        for i in range(0, l - 1):
            x1, y1 = contour[i][0]
            x2, y2 = contour[i + 1][0]
            delx, dely = x2 - x1, y2 - y1
            deg = abs(math.atan2(dely, delx) * 180.0 / math.pi)
            ln = math.sqrt(delx ** 2 + dely ** 2)
            line_info.append((x1, y1, x2, y2, deg, ln))
    return line_info


def book_coner_hint(lines, xxsm):
    maxln = 0
    for line in lines:
        maxln = max(maxln, line[5])

    cnt = 0
    acc = np.array([0., 0., 0., 0.])
    for line in lines:
        (x1, y1, x2, y2, deg, ln) = line
        op = np.array([x1, y1, x2, y2] if y1 < y2 else [x2, y2, x1, y1])
        if ln >= maxln - xxsm * 2:
            acc = acc + op
            cnt += 1

    cnt = cnt if cnt != 0 else 1
    return np.array(acc / cnt, dtype=np.int).tolist()

def 양사이드구하기(lg_line_info, clpSLen):
    maxln = 0
    vertical_lines = []
    for line in lg_line_info:
        x1, y1, x2, y2, deg, ln = line
        maxln = max(maxln, ln)

    vertical_lines = [(x1, y1, x2, y2, deg, ln) for (x1, y1, x2, y2, deg, ln) in lg_line_info if 80 <= deg <= 100 and clpSLen <= ln]


def 캐니보기(src, t1, t2):
    gray = cv2.cvtColor(src, cv2.COLOR_BGRA2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 1)
    edged = cv2.Canny(blur, t1, t2)
    contours = 윤곽선검출(edged)
    contours_view = np.zeros(shape=src.shape, dtype=np.uint8)
    cv2.drawContours(contours_view, contours, -1, 색.회색, 5)
    return contours_view

def 딜라이트(src, t1, t2, ksize, it):
    gray = cv2.cvtColor(src, cv2.COLOR_BGRA2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 1)
    edged = cv2.Canny(blur, t1, t2)
    dilate = cv2.dilate(edged, kernel=cv2.getStructuringElement(cv2.MORPH_RECT, ksize=ksize), iterations=it)
    return dilate

def con_canvas(src, contours):
    canvas = np.zeros(shape=src.shape, dtype=np.uint8)
    cv2.drawContours(canvas, contours, -1, 색.회색, 5)
    return canvas

def cany_con_can(src, t1, t2):
    edged = cv2.Canny(src, t1, t2)
    (_, contours, _) = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    canvas = np.zeros(shape=(src.shape[0], src.shape[1], 3), dtype=np.uint8)
    cv2.drawContours(canvas, contours, -1, 색.회색, 1)
    return edged, contours, canvas

def 캐니연구(src):
    height, width = src.shape[:2]  # 이미지 크기 구하기
    mn = min(height, width)
    xsm = int(mn * 0.01)
    sm = int(mn * 0.1)
    md = int(mn * 0.4)

    gray = cv2.cvtColor(src, cv2.COLOR_BGRA2GRAY)
    gblur = cv2.GaussianBlur(gray, (5, 5), 1)
    mblurWeek = cv2.medianBlur(gblur, ksize=7)
    mblurStrong = cv2.medianBlur(gblur, ksize=9)


    lst = [
        cany_con_can(mblurWeek, 10, 200),
        cany_con_can(gblur, 10, 200),
        cany_con_can(mblurStrong, 30, 30),
        cany_con_can(gblur, 35, 35),
    ]



    return [l[2] for l in lst]

def draw_con_box(src, con, color, thick):
    x, y, width, height = cv2.boundingRect(con)
    cv2.rectangle(src, (x, y), (x + width, y + height), color, thick)

def get_bound_size(con):
    x, y, width, height = cv2.boundingRect(con)
    return width * height

def get_top_size(con):
    top_size = []
    for i in range(0, len(con) - 1):
        if int(get_bound_size(con[i]) / get_bound_size(con[i + 1])) != 1:
            top_size = con[:i + 1]
            break
    return top_size

def 캐니연구2(src):
    height, width = src.shape[:2]  # 이미지 크기 구하기
    mn = min(height, width)
    xxsm = int(mn * 0.01)
    xsm = int(mn * 0.05)
    sm = int(mn * 0.1)
    md = int(mn * 0.4)

    gray = cv2.cvtColor(src, cv2.COLOR_BGRA2GRAY)
    gblur = cv2.GaussianBlur(gray, (5, 5), 1)
    mblurWeek = cv2.medianBlur(gblur, ksize=7)

    cany, con, can = cany_con_can(mblurWeek, 10, 200)
    poly = [cv2.approxPolyDP(c, epsilon=xxsm, closed=False) for c in con]

    # cv2.drawContours(can, poly, -1 , 색.빨, -1)

    # cv2.rectangle(can, (xxsm, xxsm), (xxsm * 2, xxsm *2), 색.노, 2)

    return [can]


def main_proc(src):
    # 사진 정보 구하기
    height, width = src.shape[:2]  # 이미지 크기 구하기
    clpL0, clpL1 = int(0.01 * width), int(0.3 * width)
    clpR0, clpR1 = int(0.7 * width), int(0.99 * width)
    clpT0, clpT1 = int(0.01 * height), int(0.1 * height)
    clpSLen = int(0.4 * height)
    xsm = int(0.1 * width)
    xxsm = int(0.01 * height)

    # 구조화 작업
    gray, blur, edged, dilate = 기본필터(src)
    contours = 윤곽선검출(edged)
    lg_contours, lg_polies = 윤곽선가공(contours, xsm)
    lg_line_info = 다각형근사색인(lg_polies)

    # 양사이드 검색
    left_lines = [
        (x1, y1, x2, y2, deg, ln) for (x1, y1, x2, y2, deg, ln) in lg_line_info
                  if clpL0 <= x1 <= clpL1 and clpL0 <= x2 <= clpL1 and 80 <= deg <= 100 and clpSLen <= ln
    ]
    right_lines = [
        (x1, y1, x2, y2, deg, ln) for (x1, y1, x2, y2, deg, ln) in lg_line_info
        if clpR0 <= x1 <= clpR1 and clpR0 <= x2 <= clpR1 and 80 <= deg <= 100 and clpSLen <= ln
    ]

    lh = book_coner_hint(left_lines, xxsm)
    rh = book_coner_hint(right_lines, xxsm)

    top_lines = [
        (x1, y1, x2, y2, deg, ln) for (x1, y1, x2, y2, deg, ln) in lg_line_info
        if clpT0 <= y1 <= clpT1 and clpT0 <= y2 <= clpT1 and (deg <= 45 or 135 <= deg)
    ]


    contours_view = np.zeros(shape=src.shape, dtype=np.uint8)
    cv2.drawContours(contours_view, contours, -1, 색.회색, 5)
    cv2.drawContours(contours_view, lg_polies, -1, 색.흰, 8)
    for (x1, y1, x2, y2, _, _) in left_lines: cv2.line(contours_view, (x1, y1), (x2, y2), 색.빨, 8)
    for (x1, y1, x2, y2, _, _) in right_lines: cv2.line(contours_view, (x1, y1), (x2, y2), 색.파, 8)
    for (x1, y1, x2, y2, _, _) in top_lines: cv2.line(contours_view, (x1, y1), (x2, y2), 색.초, 8)
    cv2.circle(contours_view, (lh[0], lh[1]), 20, 색.시안, 8)
    cv2.circle(contours_view, (lh[2], lh[3]), 20, 색.시안, 8)
    cv2.circle(contours_view, (rh[0], rh[1]), 20, 색.시안, 8)
    cv2.circle(contours_view, (rh[2], rh[2]), 20, 색.시안, 8)
    가이드라인그리기(contours_view, width, height, clpL0, clpL1, clpR0, clpR1, clpT0, clpT1)
    return [src, contours_view]


r = 모드.사진(캐니연구2, 0)
r.run()

