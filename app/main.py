from flask import Flask, render_template, request, jsonify

import bender
import mdata as md

# 앱 설정
app = Flask(__name__,
            static_folder=md.appstatic,
            template_folder=md.appstatic)
app.config['UPLOAD_FOLDER'] = md.src

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


for name in md.listing(md.uploads):
    print(name)
    img = md.loadimg(md.uploads, name)
    md.saveimg(md.src, name.split('.')[0] + '.png', img)

# 앱 구동
if __name__ == "__main__":
    # Only for debugging while developing

    app.run(host='0.0.0.0', debug=True, port= 80)


# # 앱 업로드
# @app.route('/fileUpload', methods = ['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         f = request.files['file']
#         file_uri = md.STATIC_PATH(md.src, f.filename)
#         f.save(file_uri)
#         return '완료'