import cv2
import math
import numpy as np
import 색
import 모드
import randomcolor

__rand_color = randomcolor.RandomColor()
def rand_color():
    global __rand_color
    return [int(c.lstrip()) for c in reversed(__rand_color.generate(format_='rgb')[0][4:-1].split(","))]

class BookScanner:
    def __init__(m, src):
        m.height, m.width = src.shape[:2]
        m.src = src
        m.blur = cv2.GaussianBlur(src, (3, 3), 1)
        m.blGray = cv2.cvtColor(m.blur, cv2.COLOR_BGRA2GRAY)
        m.edge = cv2.Canny(m.blGray, 30, 40)
        m.dilate = m.get_dilate(m.edge, cv2.MORPH_ELLIPSE, (5, 5), 3)
        m.contours = m.get_contours(m.dilate)
        m.redeuced_contours = m.get_redeuce_contours(m.contours, m.width * 0.2)
        m.canvas = m.get_canvas()
        # cv2.drawContours(m.canvas, m.redeuced_contours, -1, 색.흰, -1)

        m.polies = [cv2.approxPolyDP(contour, 3, True,) for contour in m.contours]
        m.polyline_data = m.get_polyline_data(m.polies, m.height)
        m.reduced_polyline_data = m.get_reduced_polyline_data(m.polyline_data, m.width * 0.01)
        m.sidever_candi = m.get_lg_side_ver(m.polyline_data, m.height * 0.01)

        m.draw_polyline_data(m.src, m.polyline_data, 색.빨, 3)
        # m.draw_line_data(m.canvas, m.sidever_candi, 색.흰, 3)
        m.drawHoughLines(m.canvas, 색.시안, 2)

        m.out = [m.src,m.canvas]


    def get_canvas(m, color=False):
        shape = (m.height, m.width) if not color else (m.height, m.width, 3)
        return np.zeros(shape=shape, dtype=np.uint8)

    def get_redeuce_contours(m, contours, xxsm):
        def size(contour):
            (x, y), (w, h), angle = cv2.minAreaRect(contour)
            return w > xxsm or h > xxsm
        return [contour for contour in contours if size(contour)]

    def drawHoughLines(m, src, color, thick):
        lines = cv2.HoughLinesP(
            src,
            rho = 5,
            theta= np.pi / 180 * 3,
            threshold=30,
            minLineLength=m.height * 0.1,
            maxLineGap=m.width * 0.2
        )
        # print(lines)
        if not lines is None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(m.src, (x1, y1), (x2, y2), color, thick)

    def draw_line_data(m, src, line_data, color, thick):
        for line in line_data:
            cv2.line(src, line["p1"], line["p2"], color if not color == 'rand' else rand_color(), thick)

    def draw_polyline_data(m, src, polyline_data, color, thick):
        for poly in polyline_data:
            for line in poly["line_data"]:
                cv2.line(src, line["p1"], line["p2"], color if not color == 'rand' else rand_color(), thick)

    def get_lg_side_ver(m, polyline_data, md):
        return [
            line for poly in polyline_data
                    for line in poly["line_data"]
                        if 60 <= line["ang"] <= 120 and line["len"] > md
        ]

    def get_reduced_polyline_data(m, polyline_data, xxsm):
        return [poly for poly in polyline_data if poly["w"] > xxsm and poly["h"] > xxsm]

    def get_polyline_data(m, polies, img_height):
        poly_data = []
        for j, poly in enumerate(polies):
            rect = cv2.minAreaRect(poly)
            (x, y), (w, h), angle = rect
            box = cv2.boxPoints(rect)
            box = np.int32(box)

            line_data = []
            l = len(poly)
            for i in range(0, l):
                x1, y1 = poly[i][0]
                x2, y2 = poly[i + 1 if i + 1 < l else 0][0]
                iy1, iy2 = img_height - y1, img_height - y2

                rad = math.atan2((iy2 - iy1), (x2 - x1))
                deg = rad * 180.0 / math.pi
                deg = deg if deg >= 0 else 360 + deg
                rho = x1 * math.cos(rad) * iy1 * math.sin(rad)

                length = math.sqrt((x2 - x1) ** 2 + (iy2 - iy1) ** 2)

                line_data.append({
                    "idx": j,
                    "p1": (x1, y1),
                    "p2": (x2, y2),
                    "ang": deg,
                    "len": length,
                    "rad": rad,
                    "rho": rho,
                })

            poly_data.append({
                "idx": (j, i),
                "poly": poly,
                "line_data": line_data,
                "x": x,
                "y": y,
                "w": w,
                "h": h,
                "ang": angle,
                "box": box
            })

        return poly_data

    def get_dilate(m, edge, shape, ksize, iterations):
        kernel = cv2.getStructuringElement(shape, ksize=ksize)
        dilate = cv2.dilate(edge, kernel=kernel, iterations=iterations)
        return dilate

    def get_contours(m, dilate):
        (_, contours, _) = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        return contours

    def sort_size_contours(m, contours):
        def get_rect_size(contour):
            rect = cv2.minAreaRect(contour)
            (x, y), (w, h), angle = rect
            return w * h

        return sorted(contours, get_rect_size, True)


    def get_contours_infoes(m, contours):
        def get_info(contour):
            rect = cv2.minAreaRect(contour)
            (x, y), (w, h), angle = rect
            box = cv2.boxPoints(rect)
            box = np.int32(box)
            return contour, w*h, x, y, w, h, angle, rect, box

        contours_infoes = [get_info(contour) for contour in contours]
        contours_infoes.sort(key=lambda o: o[1], reverse=True)
        return contours_infoes


def main_proc(src):
    return BookScanner(src).out


r = 모드.사진(main_proc, 0.3)
r.run()
