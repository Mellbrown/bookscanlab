import cv2
import math
import numpy as np
import 색
import 모드
import HintSystem as hs

hints = hs.HintSystem()


def get_size(hs):
    src = hs.getHint('src')
    height, width = src.shape[:2]
    hs.putHints({
        'height': height,
        'width': width
    })
hints.registTrigger('크기 GET', ['src'], get_size)


def get_left_clip(hs):
    width, cpl= hs.getHints(['width', 'left clip'])
    hs.putHint('cpl', (int(cpl[0] * width), int(cpl[1] * width)))
hints.registTrigger('좌측 클립 계산', ['width', 'left clip'], get_left_clip)


def get_right_clip(hs):
    width, cpr = hs.getHints(['width', 'right clip'])
    hs.putHint('cpr', (int(cpr[0] * width), int(cpr[1] * width)))
hints.registTrigger('우측 클립 계산', ['width', 'right clip'], get_right_clip)


def get_top_clip(hs):
    height, cpt= hs.getHints(['height', 'top clip'])
    hs.putHint('cpt', (int(cpt[0] * height), int(cpt[1] * height)))
hints.registTrigger('상단 클립 계산', ['height', 'top clip'], get_top_clip)


def 기본필터(hs):
    src = hs.getHint('src')
    gray = cv2.cvtColor(src, cv2.COLOR_BGRA2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 1)
    edged = cv2.Canny(blur, 35, 125)
    dilate = cv2.dilate(edged, kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=(5, 5)), iterations=3)
    hs.putHints({ 'gray': gray, 'blur': blur, 'edged': edged, 'dilate': dilate })
hints.registTrigger('기본필터', ['src'], 기본필터)


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

def 구조화작업(hs):
    edged, xsm = hs.getHints(['edged', 'xsm'])
    contours = 윤곽선검출(edged)
    lg_contours, lg_polies = 윤곽선가공(contours, xsm)
    lg_line_info = 다각형근사색인(lg_polies)
    hs.putHints({ 'contours': contours, 'lg_contours': lg_contours, 'lg_polies': lg_polies, 'lg_line_info': lg_line_info })
hints.registTrigger('구조화작업',['edged', 'xsm'], 구조화작업)


def 단위추가(hs):
    height, width = hs.getHints(['height', 'width'])
    xsm = int(0.1 * width)
    xxsm = int(0.01 * height)
    md = int(0.4 * height)
    hs.putHints({ 'xsm': xsm, 'xxsm': xxsm, 'md': md})
hints.registTrigger('단위추가', ['height', 'width'], 단위추가)


def 좌측_수직선_후보(hs):
    cpl, lg_line_info, md = hs.getHints(['cpl', 'lg_line_info', 'md'])
    left_lines = [
        (x1, y1, x2, y2, deg, ln) for (x1, y1, x2, y2, deg, ln) in lg_line_info
                  if cpl[0] <= x1 <= cpl[1] and cpl[0] <= x2 <= cpl[1] and 80 <= deg <= 100 and md <= ln
    ]
    hs.putHint('left_lines', left_lines)
hints.registTrigger('좌측 수직선 후보 GET', ['cpl', 'lg_line_info', 'md'], 좌측_수직선_후보)


def 우측_수직선_후보(hs):
    cpr, lg_line_info, md = hs.getHints(['cpr', 'lg_line_info', 'md'])
    left_lines = [
        (x1, y1, x2, y2, deg, ln) for (x1, y1, x2, y2, deg, ln) in lg_line_info
                  if cpr[0] <= x1 <= cpr[1] and cpr[0] <= x2 <= cpr[1] and 80 <= deg <= 100 and md <= ln
    ]
    hs.putHint('right_lines', left_lines)
hints.registTrigger('우측 수직선 후보 GET', ['cpr', 'lg_line_info', 'md'], 우측_수직선_후보)


def 가이드라인그리기(src, width, height, clpL0, clpL1, clpR0, clpR1, clpT0, clpT1):
    cv2.line(src, (clpL0, 0), (clpL0, height), 색.노, 8)
    cv2.line(src, (clpL1, 0), (clpL1, height), 색.노, 8)
    cv2.line(src, (clpR0, 0), (clpR0, height), 색.노, 8)
    cv2.line(src, (clpR1, 0), (clpR1, height), 색.노, 8)
    cv2.line(src, (0, clpT0), (width, clpT0), 색.노, 8)
    cv2.line(src, (0, clpT1), (width, clpT1), 색.노, 8)

def 정보드로잉(hs):
    src, contours, lg_polies  = hs.getHints(['src', 'contours', 'lg_polies'])
    left_lines, right_lines, top_lines = hs.getHints(['left_lines', 'right_lines', 'top_lines'])
    width, height, cpl, cpr, cpt = hs.getHints(['width', 'height', 'cpl', 'cpr', 'cpt'])
    contours_view = np.zeros(shape=src.shape, dtype=np.uint8)
    cv2.drawContours(contours_view, contours, -1, 색.회색, 5)
    cv2.drawContours(contours_view, lg_polies, -1, 색.흰, 8)
    for (x1, y1, x2, y2, _, _) in left_lines: cv2.line(contours_view, (x1, y1), (x2, y2), 색.빨, 8)
    for (x1, y1, x2, y2, _, _) in right_lines: cv2.line(contours_view, (x1, y1), (x2, y2), 색.파, 8)
    for (x1, y1, x2, y2, _, _) in top_lines: cv2.line(contours_view, (x1, y1), (x2, y2), 색.초, 8)
    # cv2.circle(contours_view, (lhx1, lhy1), 20, 색.시안, 8)
    # cv2.circle(contours_view, (lhx2, lhy2), 20, 색.시안, 8)
    # cv2.circle(contours_view, (rhx1, rhy1), 20, 색.시안, 8)
    # cv2.circle(contours_view, (rhx2, rhy2), 20, 색.시안, 8)
    가이드라인그리기(contours_view, width, height, cpl[0], cpl[1], cpr[0], cpr[1], cpt[0], cpt[1])
    hs.putHint('contours_view', contours_view)
hints.registTrigger('정보드로잉', ['src', 'contours', 'lg_polies', 'left_lines', 'right_lines', 'top_lines', 'width', 'height', 'cpl', 'cpr', 'cpt'], 정보드로잉)


print()
def main_proc(src):
    global hints
    hints.clear()

    hints.putHint('src', src)
    hints.putHint('left clip', (0.01, 0.3))
    hints.putHint('right clip', (0.7, 0.99))
    hints.putHint('top clip', (0.01, 0.1))

    hints.runSystem()

    return hints.getHints(['src'])

모드.사진(main_proc, 500).run()