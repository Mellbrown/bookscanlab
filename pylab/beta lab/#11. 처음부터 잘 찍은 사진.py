import cv2
import math
import numpy as np
import 모드
import randomcolor

__rand_color = randomcolor.RandomColor()
def rand_color():
    global __rand_color
    return [int(c.lstrip()) for c in reversed(__rand_color.generate(format_='rgb')[0][4:-1].split(","))]

class BookScanner:
    def __init__(m, src):
        # 원본 이미지들
        m.height, m.width = src.shape[:2] # 이미지 크기 구하기
        m.src = src # 원본 사진

        # 잡음 제거
        m.gray = cv2.cvtColor(m.src, cv2.COLOR_BGRA2GRAY)
        m.blur = cv2.GaussianBlur(src, (5, 5), 0) # 블러처리
        m.blGray = cv2.cvtColor(m.blur, cv2.COLOR_BGRA2GRAY) # 그레이 처리

        # 엣지 검출
        m.edge = cv2.Canny(m.blGray, 50, 40) # 캐니 처리
        m.dilate = m.get_dilate(m.edge, cv2.MORPH_ELLIPSE, (5, 5), 3) # 캐니 확장

        m.out = [m.src, m.blGray, m.edge]



    def draw_HoughLine(m, src, rho, theta, color, thick):
        c = np.cos(theta)
        s = np.sin(theta)
        x0 = c * rho
        y0 = s * rho
        # print("%d, %d" % (x0, y0))
        x1 = int(x0 + 100 * -s)
        y1 = int(y0 + 100 * c)
        x2 = int(x0 - 100 * -s)
        y2 = int(y0 - 100 * c)
        iy1 = m.height - y1
        iy2 = m.height - y2
        print("rho:%d theta:%d, (%d, %d), (%d, %d) -> (%d, %d)" % (rho, x0, y0, theta, x1, y1, x2, y2))
        cv2.line(src, (x1, y1), (x2, y2), color, thick)

    def merge_similar_line_data(m, line_data, zit_theta, zit_rho):
        merged = []
        for line in line_data:
            find = False
            for mr in merged:
                (tag_theta, tag_rho) = mr['tag']
                (line_theta, line_rho) = line["ang"], line["rho"]
                diff_theta = abs(line_theta - tag_theta)
                diff_rho = abs(line_rho - tag_rho)

                if diff_theta < zit_theta and diff_rho < zit_rho: # 찾은 경우
                    mr['line'].append(line)
                    acc_theta = 0.0
                    acc_rho = 0.0
                    for l in mr['line']:
                        acc_theta += l['ang']
                        acc_rho += l['rho']
                    ln = len(mr['line'])
                    acc_theta /= ln
                    acc_rho /= ln
                    find = True
                    break

            if not find:
                merged.append({'tag':(line["ang"], line["rho"]), 'line': [line]})

        return merged


    def get_canvas(m, color=False):
        shape = (m.height, m.width) if not color else (m.height, m.width, 3)
        return np.zeros(shape=shape, dtype=np.uint8)

    def get_redeuce_contours(m, contours, xxsm):
        def size(contour):
            (x, y), (w, h), angle = cv2.minAreaRect(contour)
            return w > xxsm or h > xxsm
        return [contour for contour in contours if size(contour)]

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

                length = math.sqrt((x2 - x1) ** 2 + (iy2 - iy1) ** 2)

                theta = np.arctan2((y2 - y1), -(x2 - x1))
                rho = x1 * np.cos(theta) + y1 + np.sin(theta)

                line_data.append({
                    "idx": j,
                    "p1": (x1, y1),
                    "p2": (x2, y2),
                    "ang": deg,
                    "len": length,
                    "theta": theta,
                    "rho": rho
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


r = 모드.사진(main_proc, 500)
r.run()
