import mdata as mdt
import cvcolor
import numpy as np
import cv2

class bookline:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.x1, self.y1 = p1
        self.x2, self.y2 = p2
        self.l = np.sqrt(np.power(self.y2 - self.y1, 2) + np.power(self.x2 - self.x1))
        self.direct = np.arctan2(self.y2 - self.y1, self.x2 - self.x1) * np.pi * 180.0

    def __str__(self):
        return '[%d,%d->%d,%d:%d(%d)]' % (self.x1, self.y1, self.x2, self.y2, self.l, self.direct)

class bookpoly:
    pass


class bookTempalte:
    def __init__(self, contours):
        self.contour_list = [[bookline(contour[idx][0], bookline(contour[idx+1][0])) for idx in range(0, len(contour) - 2)] for contour in contours]


def proccess2 (name):
    src = mdt.loadimg(mdt.src, name)
    sample = mdt.scalingWdith(src, 500)

    gblur = cv2.GaussianBlur(sample,(5, 5), 1)
    gray = cv2.cvtColor(gblur, cv2.COLOR_BGR2GRAY)
    cany = cv2.Canny(gray, 30, 230)
    contours, _ = cv2.findContours(cany, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    polies = [cv2.approxPolyDP(con, 5, True) for con in contours]
    polies = [poly for poly in polies if len(poly) >= 2]
    polies_canvas = np.zeros(shape=cany.shape, dtype=np.uint8)
    cv2.drawContours(polies_canvas, polies, -1, cvcolor.white, 1)

    vlines = [mdt.coords2contour(ver) for poly in polies for ver in
                mdt.coords_split(mdt.contour2coords(poly))['ver']]
    vlines = [poly for poly in vlines if len(poly) >= 2]
    vline_canvas = np.zeros(shape=cany.shape, dtype=np.uint8)
    cv2.drawContours(vline_canvas, vlines, -1, cvcolor.white, 1)

    def vline_merge(contour):
        if len(contour) == 2: return contour
        else:
            rect = cv2.minAreaRect(contour)
            ((x, y), (w, h), angle) = rect
            area = (0, h) if w < h else (w, 0)
            box = cv2.boxPoints(((x, y), area, angle))
            box = np.int32([ [box[1]], [box[2]]] if (box[0][0] == box[1][0] and box[0][1] == box[1][1]) else [[box[0]], [box[1]]])
            return box

    merged_vlines = [vline_merge(ver) for ver in vlines]
    mvlines_canvas = np.zeros(shape=cany.shape, dtype=np.uint8)
    cv2.drawContours(mvlines_canvas, merged_vlines, -1, cvcolor.white, 1)

    return  {
        'images': [
            {'name': key, 'image': mdt.savetemp('gorun', key + '-' + name, img)} for key, img in {
                'gblur': gblur,
                'gray': gray,
                'cany': cany,
                'polies': polies_canvas,
                'vlines': vline_canvas,
                'mergerd_vlines': mvlines_canvas
            }.items()
        ],
        'contours': [
            { 'name': key, 'contours': contours} for key, contours in {
                'controus': [contour.tolist() for contour in contours],
                'polies': [poly.tolist() for poly in polies],
                'vlines': [vline.tolist() for vline in vlines],
                'merged_vlines': [vline.tolist() for vline in merged_vlines]
            }.items()
        ]
    }

def proccess1 (name):
    src = mdt.loadimg(mdt.src, name)
    height, width = src.shape[:2]  # 이미지 크기 구하기
    mn = min(height, width)
    xxsm = int(mn * 0.01)
    xsm = int(mn * 0.05)
    sm = int(mn * 0.1)
    smm = int(mn * 0.3)
    md = int(mn * 0.4)
    xmd = int(mn * 0.4)

    gblur = cv2.GaussianBlur(src, (7, 7), 1)
    mblur = cv2.medianBlur(gblur, 7)
    mgray = cv2.cvtColor(mblur, cv2.COLOR_BGR2GRAY)
    mcany = cv2.Canny(mgray, 30, 40)
    dkernel = np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0]], dtype=np.uint8)
    dilate = cv2.dilate(mcany, dkernel, iterations=3)
    contours, _ = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # cpoly = np.zeros(shape=(height, width), dtype=np.uint8)
    polies = [cv2.approxPolyDP(con, 2, True) for con in contours]
    # cv2.drawContours(cpoly, polies, -1, cvcolor.white, 1)

    # dpoly = np.zeros(shape=(height, width), dtype=np.uint8)
    dpolies = [poly for poly in polies if len(poly) >= 2]
    # cv2.drawContours(dpoly, dpolies, -1, cvcolor.white, 1)

    verlines = [mdt.coords2contour(ver) for poly in dpolies for ver in mdt.coords_split(mdt.contour2coords(poly))['ver']]
    cverline = np.zeros(shape=(height, width), dtype=np.uint8)
    cv2.drawContours(cverline, verlines, -1, cvcolor.white, 1)

    dverline = np.zeros(shape=(height, width, 3), dtype=np.uint8)
    for ver in verlines:
        if len(ver) == 1:
            cv2.drawContours(dverline, [ver], -1, cvcolor.red, 1)
            pass
        elif len(ver) == 2:
            cv2.drawContours(dverline, [ver], -1, cvcolor.cyan, 1)
        else:
            cv2.drawContours(dverline, [ver], -1, cvcolor.gray, 1)

    for ver in verlines:
        if len(ver) > 2:
            rect = cv2.minAreaRect(ver)
            ((x, y), (w, h), angle) = rect
            area = (0, h) if w < h else (w, 0)
            box = cv2.boxPoints(((x, y), area, angle))
            box = np.int32([box[1], box[2]] if (box[0][0] == box[1][0] and box[0][1] == box[1][1]) else [box[0], box[1]])
            cv2.drawContours(dverline, [box], -1, cvcolor.yellow, 1)

    def 뭉치기(contour):
        if len(contour) == 2: return contour
        else:
            rect = cv2.minAreaRect(contour)
            ((x, y), (w, h), angle) = rect
            area = (0, h) if w < h else (w, 0)
            box = cv2.boxPoints(((x, y), area, angle))
            box = np.int32([ [box[1]], [box[2]]] if (box[0][0] == box[1][0] and box[0][1] == box[1][1]) else [[box[0]], [box[1]]])
            return box

    verlines = [뭉치기(ver) for ver in verlines if len(ver) > 1]
    comcan = np.zeros(shape=(height, width), dtype=np.uint8)
    cv2.drawContours(comcan, verlines, -1, cvcolor.white, 1)

    wcany = cv2.Canny(mgray, 30, 230)

    return {
        'images': [
            {'name': key, 'image': mdt.savetemp('gorun', key + '-' + name, img)} for key, img in {
                'mcany': mcany,
                'dilate': dilate,
                # 'cpoly': cpoly,
                # 'dpoly': dpoly,
                'cverline': cverline,
                'dverline': dverline,
                'comcan': comcan,
                'wcany': wcany
            }.items()
        ],
        'contours': [
            { 'name': key, 'contours': contours} for key, contours in {
                'polies': [poly.tolist() for poly in polies],
                'dpolies': [dpoly.tolist() for dpoly in dpolies],
                'verlines': [ver.tolist() for ver in verlines].sort()
            }.items()
        ]
    }

def proccess(name):
    return proccess2(name)