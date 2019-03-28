import json
import cv2
import numpy as np

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

json_file = open('./input.json', mode='r')
json_data = json.load(json_file)
img = cv2.imread(json_data['image-src'])

height, width = img.shape[:2]
width *= 0.3
height *= 0.3
width = int(width)
height = int(height)

controus = jsonPath2controus(json_data['image-path'])
corners = pathsGetConer(json_data['image-path'])
print(corners)

# 사진을 투영 변환을 해봤습니다.
M = cv2.getPerspectiveTransform(
    np.float32([[p['x'], p['y']] for p in corners]),
    np.float32([[100, 100], [600, 100], [600, 700], [100, 700]])
)

def g (x, y):
    return (M[0,0]*x + M[1,0]*y + M[2,0])/(M[0,2]*x + M[1,2]*y + M[2,2])

print(g(corners[0]['x'],corners[0]['y']))