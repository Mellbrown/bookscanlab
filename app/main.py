from flask import Flask, render_template, request, jsonify
import json
import cv2
import os
import numpy as np
import random

red = (0,0,255)
green = (0,255,0)
blue = (255,0,0)
cyan = (255,255,0)
yellow = (0,255,255)
white = (255,255,255)
black = (0,0,0)
gray = (100,100,100)

def genTempTar (filename):
    return filename.split('.')[0] + '-' + hex(random.getrandbits(128)) + '.png'

def removeOtherTempTar (path, filename):
    ls = os.listdir(path)
    fn = filename.split('.')[0]
    for l in ls:
        if not l.find(fn) == -1:
            print('remove file', path + '/' + l)
            os.remove(path + '/' + l)

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

def bending(image_path, paths, bound):
    img = cv2.imread(image_path)
    height, width = img.shape[:2]

    controus = jsonPath2controus(paths)
    corners = pathsGetConer(paths)

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
    cv2.drawContours(canvas, [controus], -1, white, 2)
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
                cv2.circle(canvas, (i, y), 5, white, 2)
                ver.append([[i, y]])
                break
        for y in range(bottom + top - 1, -1, -1):
            if not canvas[y, i] == 0:
                cv2.circle(canvas, (i, y), 5, white, 2)
                ver.append([[i, y]])
                break
        verline.append(ver)

    rects = [np.array([verline[i][0], verline[i+1][0], verline[i+1][1], verline[i][1]]) for i in range(0, len(verline)-1)]
    cv2.drawContours(canvas, rects, -1, white, 2)

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



UPLOAD_PATH = '/app/static/uploads'
SRC_PATH = '/app/static/source'
STATIC_PATH = '/app/static'

# 앱 설정
app = Flask(__name__,
            static_folder="./static",
            template_folder="./static")
app.config['UPLOAD_FOLDER'] = SRC_PATH

# 앱 프론트 전송
@app.route("/")
def hello():
    return render_template("index.html")

# 이미지 디렉토리 조회
@app.route("/list-source")
def listSourceImages():
    file_list = os.listdir(SRC_PATH)
    file_list.sort()
    return jsonify(file_list)


# 앱 업로드
@app.route('/fileUpload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        file_uri = SRC_PATH + '/' +f.filename
        f.save(file_uri)
        return '완료'

@app.route('/image-banding', methods = ['GET', 'POST'])
def imagebanding():
    json_data = json.loads(request.data, encoding='utf-8')
    target = json_data['image-target']
    path = json_data['path']
    bound = json_data['bound']
    result = bending(SRC_PATH + '/' + target, path, bound)

    send = []
    for key in result:
        impath = STATIC_PATH + '/' + key
        if (not os.path.isdir(impath)):
            os.mkdir(impath)
            print('gen dir: ', impath)

        removeOtherTempTar(impath, target)
        tempimg = genTempTar(target)
        cv2.imwrite(impath + '/' + tempimg, result[key])
        print('gen img: ', impath + '/' + tempimg)
        send.append(key + '/' + tempimg)

    return jsonify(send)


def convertImageSimple():
    uploades = os.listdir(UPLOAD_PATH)
    print('=' *  10)
    print(uploades)
    for upload_filename in uploades:
        print(upload_file)
        img = cv2.imread(UPLOAD_PATH + '/' + upload_filename)
        sp = upload_filename.split('.')
        cv2.imwrite(SRC_PATH + '/' + sp[0] + '.png', img)
        os.remove(UPLOAD_PATH + '/' + upload_filename)

convertImageSimple()

# 앱 구동
if __name__ == "__main__":
    # Only for debugging while developing

    app.run(host='0.0.0.0', debug=True, port= 80)
