import json
import cv2
import numpy as np
from app import cvcolor


def jsonPath2controus(jsonPath:list):
    return np.array([[[point['x'], point['y']]] for point in jsonPath])

if __name__ == '__main__':
    json_file = open('./input.json', mode='r')
    json_data = json.load(json_file)
    img = cv2.imread(json_data['image-src'])

    height, width = img.shape[:2]
    width *= 0.3
    height *= 0.3
    width = int(width)
    height = int(height)

    controus = jsonPath2controus(json_data['image-path'])
    corners = [json_data['image-path'][json_data['image-corner'][key]]  for key in json_data['image-corner']]
    box = jsonPath2controus(corners)
    cv2.drawContours(img, [controus], -1, cvcolor.red, 3)
    cv2.drawContours(img, [box], -1, cvcolor.green, 8)

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow("image", img)
    cv2.resizeWindow("image", height, height)
    cv2.waitKey()
