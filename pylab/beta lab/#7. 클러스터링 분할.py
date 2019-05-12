import cv2
import numpy as np
import 모드
import 색


def main_proc(image):
    height, width = image.shape[:2]
    area = height * width
    height03 = height * 0.1
    width03 = width * 0.3

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    data = hsv.reshape((-1,3)).astype(np.float32)
    K = 2
    term_crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, labels, centers = cv2.kmeans(data, K, None, term_crit, 5, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    dst = res.reshape(image.shape)

    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    edged = cv2.Canny(blur, 30, 50)
    kernel = cv2.getStructuringElement(shape=cv2.MORPH_ELLIPSE, ksize= (5,5))
    dilated = cv2.dilate(edged, kernel, iterations=10)
    (_, contours, _) = cv2.findContours(dilated, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    score = []
    for cnt in contours:
        # cv2.drawContours(image, [cnt], -1, 색.파, 3)
        x, y, w, h = cv2.boundingRect(cnt)
        if (w * h) / area < 0.1 and not (w > width03 or h > height03): continue
        cv2.drawContours(image, [cnt], -1, 색.시안, 3)
        # cv2.rectangle(image, (x, y), (x + w, y + h), 색.빨, 3)
        #
        # poly = cv2.approxPolyDP(cnt, epsilon=20, closed=True)
        # cv2.drawContours(image, [poly], -1, 색.초, 3)

    # 출력
    return {
        'image': image,
        # 'gray': gray,
        # 'edged': edged,
        'dilated': dilated,
        'dst': dst
    }


r = 모드.사진(main_proc, 0.3)
r.run()

