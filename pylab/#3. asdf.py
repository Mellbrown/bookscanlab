from flask import jsonify

key = "asdf"
target = 'asdf.png'

print (jsonify({
    'img': '/' + key + '/' + target
}))