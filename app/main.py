from flask import Flask, render_template, request, jsonify
import json
import cv2
import os
import numpy as np

red = (0,0,255)
green = (0,255,0)
blue = (255,0,0)
cyan = (255,255,0)
yellow = (0,255,255)
white = (255,255,255)
black = (0,0,0)
gray = (100,100,100)

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
    M = cv2.getPerspectiveTransform(
        np.float32([[p['x'], p['y']] for p in corners]),
        np.float32([
            [bound['left'], bound['top']],
            [bound['left'] + bound['width'], bound['top']],
            [bound['left'] + bound['width'], bound['top'] + bound['height']],
            [bound['left'], bound['top'] + bound['height']]
        ])
    )

    canvas = np.zeros(shape=(height, width), dtype=np.uint8)
    cv2.drawContours(canvas, [controus], -1, white, 2)
    canvas = cv2.warpPerspective(canvas, M, (
        bound['width'] + bound['left'] * 2,
        bound['height'] + bound['height'] * 2
    ))
    canvas = canvas[
             bound['top']: bound['top'] + bound['height'],
             bound['left']: bound['left'] + bound['width'] + 1
         ]

    return {
        'skelecton': canvas
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
    for key in result:
        if (not os.path.isdir(STATIC_PATH + '/' + key)):
            os.mkdir(STATIC_PATH + '/' + key)
            print('gen dir: ', STATIC_PATH + '/' + key)
        cv2.imwrite(STATIC_PATH + '/' + key + '/' + target, result[key])
        print('gen img: ', STATIC_PATH + '/' + key + '/' + target, result[key])

    r = jsonify([
        '/' + key + '/' + target
    ])
    print('result: ', r)

    return r


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
