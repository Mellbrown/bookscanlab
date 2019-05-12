import cv2
import numpy as np
import cvcolor

def coords2contour(coords):
    return np.array([ [[ point['x'], point['y'] ]] for point in coords])

def contour2coords(contour):
    return [ { 'x': int(point[0,0]), 'y': int(point[0,1])} for point in contour]

# 원본이미지
image = np.zeros(shape=(300, 300), dtype=np.uint8)
cv2.rectangle(image, (100, 100), (200, 200), cvcolor.white, 3)

# 컨투어
contours, _ = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
print('type(contours)', type(contours))
print(str(contours).replace('\n\n', '\n'))
print('contours[0].shape', contours[0].shape)

# 폴리
tpoly = [cv2.approxPolyDP(contour, 2, True) for contour in contours]
print('tpoly[0].shape', tpoly[0].shape)

fpoly = [cv2.approxPolyDP(contour, 2, False) for contour in contours]
print('fpoly[0].shape', fpoly[0].shape)

ccc = coords2contour(contour2coords(tpoly[0]))
print('ccc.shape', ccc.shape)

rect = cv2.minAreaRect(ccc)
((x, y), (w, h), angle) = rect
area = (0, h) if w < h else (w, 0)
box = cv2.boxPoints(((x, y), area, angle))
box = np.int32([ [box[1]], [box[2]]] if (box[0][0] == box[1][0] and box[0][1] == box[1][1]) else [[box[0]], [box[1]]])
print('box shape', box.shape)

cv2.waitKey()
cv2.destroyAllWindows()