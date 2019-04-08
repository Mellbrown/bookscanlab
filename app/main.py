from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import mdata as md

import bender
import mfilter


# 앱 설정
app = Flask(__name__,
            static_folder=md.appstatic,
            template_folder=md.appstatic)
app.config['UPLOAD_FOLDER'] = md.src
cors = CORS(app, resources= {
    r"*": {"origin": "*"}
})

# 앱 프론트 전송
@app.route("/")
def front():
    return render_template("index.html")

# 이미지 디렉토리 조회
@app.route("/list-source")
def img_listing():
    return jsonify(md.listing(md.src))

#이미지 밴
@app.route('/image-banding', methods = ['GET', 'POST'])
def img_banding():
    data = md.jsonparse(request.data)
    result = bender.bend(data['image'], data['coord'], data['bound'])

    send = []
    for key in result:
        md.wipetemp(key, data['image'])
        tmp = md.savetemp(key, data['image'], result[key])
        send.append(key + '/' + tmp)

    return jsonify(send)

#필터이미지 생성
@app.route('/run-filter', methods = ['GET', 'POST'])
def img_filter():
    data = md.jsonparse(request.data)
    result = mfilter.run_filter(data['image'], data['filter-param'])
    return jsonify([result])


for name in md.listing(md.uploads):
    print(name)
    img = md.loadimg(md.uploads, name)
    md.saveimg(md.src, name.split('.')[0] + '.png', img)

# 앱 구동
if __name__ == "__main__":
    # Only for debugging while developing

    app.run(host='0.0.0.0', debug=True, port= 80)
