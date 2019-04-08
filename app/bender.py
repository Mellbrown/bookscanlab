import numpy as np
import cv2
import cvcolor
import mdata as md

def coords4corner(coords):
    avg = sum([p['y'] for p in coords]) / len(coords)
    t = sorted([p for p in coords if p['y'] < avg], key=lambda p: p['x'])
    b = sorted([p for p in coords if p['y'] > avg], key=lambda p: p['x'])

    return [t.pop(0), t.pop(), b.pop(), b.pop(0)]

def bend(name, coord, bound):
    img = md.loadimg(md.src, name)
    height, width = img.shape[:2]

    controus = md.coords2contour(coord)
    corners = coords4corner(coord)

    left = bound['left']
    top = bound['top']
    right = bound['left'] + bound['width']
    bottom = bound['top'] + bound['height']

    M = cv2.getPerspectiveTransform(
        np.float32([[p['x'], p['y']] for p in corners]),
        np.float32([
            [ left, top ],
            [ right, top],
            [right, bottom],
            [left, bottom]
        ])
    )

    canvas = np.zeros(shape=(height, width), dtype=np.uint8)
    cv2.drawContours(canvas, [controus], -1, cvcolor.white, 2)
    canvas = cv2.warpPerspective(canvas, M, (
        bound['width'] + bound['left'] * 2,
        bound['height'] + bound['top'] * 2
    ))
    img = cv2.warpPerspective(img, M, (
        bound['width'] + bound['left'] * 2,
        bound['height'] + bound['top'] * 2
    ))

    # 10간격으로 위선을 다시 잘라 봅니다.
    verline = []
    for i in range(left, right + 1, 10):
        ver = []
        for y in range(0, bottom + top):
            if not canvas[y, i] == 0:
                cv2.circle(canvas, (i, y), 5, cvcolor.white, 2)
                ver.append([[i, y]])
                break
        for y in range(bottom + top - 1, -1, -1):
            if not canvas[y, i] == 0:
                cv2.circle(canvas, (i, y), 5, cvcolor.white, 2)
                ver.append([[i, y]])
                break
        verline.append(ver)

    rects = [np.array([verline[i][0], verline[i+1][0], verline[i+1][1], verline[i][1]]) for i in range(0, len(verline)-1)]
    cv2.drawContours(canvas, rects, -1, cvcolor.white, 2)

    sp = []
    for rect in rects:
        M = cv2.getPerspectiveTransform(
            np.float32([[p[0][0], p[0][1]] for p in rect]),
            np.float32([[0, 0], [10, 0], [10, bottom - top], [0, bottom - top]])
        )
        sp.append(cv2.warpPerspective(img, M, (10, bottom - top)))

    return {
        'flat': np.hstack(sp),
        'frame': canvas
    }
