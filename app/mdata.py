import json
import cv2
import os
import random

appstatic = '/app/static'
src = 'source'
uploads = 'uploads'

def STATIC_PATH(dir, name = None):
    return appstatic + '/' + dir + ('/' + name if name != None else '')

def jsonparse (data):
    return json.loads(data, encoding='utf-8')

def loadjson (name):
    data = None
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