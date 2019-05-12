import json
import cv2
import os
import random
import numpy as np

appstatic = '/app/static'
src = 'source'
uploads = 'uploads'

def scalingWdith(img, width):
    ratio = width / img.shape[1]
    return cv2.resize(img, None, fx=ratio, fy=ratio)

def coords2contour(coords):
    return np.array([ [[ point['x'], point['y'] ]] for point in coords])

def contour2coords(contour):
    return [ { 'x': int(point[0,0]), 'y': int(point[0,1])} for point in contour]

def contour2list(contours):
    return [ [ [ [point[0], point[1] ]  for point in poly ] for poly in contour] for contour in contours]

def STATIC_PATH(dir, name = None):
    return appstatic + '/' + dir + ('/' + name if name != None else '')

def jsonparse (data):
    return json.loads(data, encoding='utf-8')

def loadjson (name):
    jdata = None
    try:
        with open(name + '.txt', 'r') as f:
            jdata = json.load(f)
    except:
        pass

    return jdata if jdata != None else {}

def savejson (name, data):
    with open(name + '.txt', 'w') as f:
        f.write(json.dump(data))

def loadimg(dir, name):
    return cv2.imread(STATIC_PATH(dir, name))

def saveimg(dir, name, img):
    if (not os.path.isdir(STATIC_PATH(dir))):
        os.mkdir(STATIC_PATH(dir))
    cv2.imwrite(STATIC_PATH(dir,name), img)

def savetemp(dir, name, img):
    prev, extn = name.split('.')
    tmp = prev + '-' + hex(random.getrandbits(128)) + '.' + extn
    saveimg(dir, tmp, img)
    return tmp

def wipetemp(dir, name):
    prev, extn = name.split('.')
    if (os.path.isdir(STATIC_PATH(dir))):
        for l in os.listdir(STATIC_PATH(dir)):
            if prev in l and extn in l:
                os.remove(STATIC_PATH(dir, l))

def listing (dir):
    return os.listdir(STATIC_PATH(dir))

def coords_split(coords):
    lines = {'ver':[], 'hor': []}
    prevcoord = coords[0]
    prevstate = 'ver'
    line = [prevcoord]

    for coord in coords:
        x1, y1 = prevcoord.values()
        x2, y2 = coord.values()

        angle = np.arctan2(y2 - y1, x2 - x1) * 180.0 / np.pi

        state = 'ver' if 60 <= angle <= 120 or -120 <= angle <= -60 else 'hor'

        if state == prevstate:
            line.append(coord)
        else:
            lines[prevstate].append(line)
            line = [prevcoord, coord]

        prevstate = state
        prevcoord = coord

    lines[prevstate].append(line)
    if len(lines['ver']) == 1: lines['ver'].pop(0)

    return lines