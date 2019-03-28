import json
import cv2
import numpy as np
from app import cvcolor
import math


def jsonPath2controus(jsonPath:list):
    return np.array([ [[ point['x'], point['y'] ]] for point in jsonPath])

def pathsGetConer(path:list):
    avg = sum([p['y'] for p in path]) / len(path)
    toplist = [p for p in path if p['y'] < avg]
    toplist.sort(key=lambda p: p['x'])
    botlist = [p for p in path if p['y'] > avg]
    botlist.sort(key=lambda p: p['x'])

    return [
        toplist.pop(0),
        toplist.pop(),
        botlist.pop(),
        botlist.pop(0)
    ]

if __name__ == '__main__':
    json_file = open('./input.json', mode='r')
    json_data = json.load(json_file)
    img = cv2.imread(json_data['image-src'])

    height, width = img.shape[:2]
    width *= 0.3
    height *= 0.3
    width = int(width)
    height = int(height)

    controus = jsonPath2controus(json_data['image-path'])
    # corners = [json_data['image-path'][json_data['image-corner'][key]]  for key in json_data['image-corner']]
    # print(corners)
    corners = pathsGetConer(json_data['image-path'])
    print(corners)

    # 사진을 투영 변환을 해봤습니다.
    M = cv2.getPerspectiveTransform(
        np.float32([[p['x'], p['y']] for p in corners]),
        np.float32([[100, 100], [600, 100], [600, 700], [100, 700]])
    )
    dst = cv2.warpPerspective(img, M, (1000, 1000))
    # cv2.rectangle(dst, (100, 60), (600, 720), cvcolor.red, 1)
    dst = dst[60: 720, 100:600]

    # 라인을 투영 변환 해봤습니다.
    canvas = np.zeros(shape=(img.shape[0], img.shape[1], 3), dtype=np.uint8)
    cv2.drawContours(canvas, [controus], -1, cvcolor.green, 2)
    canvas = cv2.warpPerspective(canvas, M, (1000, 1000))
    canvas = canvas[60: 720, 100:601]
    canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    # canvas = cv2.threshold(canvas, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)

    # 10간격으로 위선을 다시 잘라 봅니다.
    verline = []
    for i in range(0, 501, 10):
        ver = []
        for y in range(0, 660):
            if not canvas[y, i] == 0:
                cv2.circle(canvas, (i, y), 3, cvcolor.white, 1)
                ver.append([[i, y]])
                break
        for y in range(660 - 1, -1, -1):
            if not canvas[y, i] == 0:
                cv2.circle(canvas, (i, y), 3, cvcolor.white, 1)
                ver.append([[i, y]])
                break
        verline.append(ver)

    rects = [np.array([verline[i][0], verline[i+1][0], verline[i+1][1], verline[i][1]]) for i in range(0, len(verline)-1)]
    cv2.drawContours(canvas, rects, -1, cvcolor.white, 1)

    sp = []
    for rect in rects:
        M = cv2.getPerspectiveTransform(
            np.float32([ [ p[0][0], p[0][1] ] for p in rect]),
            np.float32([[0, 0], [10, 0], [10, 600], [0, 600]])
        )
        sp.append(cv2.warpPerspective(dst, M, (10, 600)))

    cv2.imshow('1', cv2.resize(img, None, fx=0.3, fy=0.3))
    cv2.imshow('2', dst)
    cv2.imshow('3', canvas)
    cv2.imshow('4', np.hstack(sp))
    cv2.waitKey()