from flask import Flask, render_template, request, jsonify
import cv2
import os

UPLOAD_PATH = '/app/static/uploads'
SRC_PATH = '/app/static/source'

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
