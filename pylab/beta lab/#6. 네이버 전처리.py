import cv2
import 모드
import 색


def main_proc(image):
    height, width = image.shape[:2]
    area = height * width

    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    edged = cv2.Canny(blur, 0, 30)
    kernel = cv2.getStructuringElement(shape=cv2.MORPH_ELLIPSE, ksize= (5,5))
    dilated = cv2.dilate(edged, kernel, iterations=1)
    (_, contours, _) = cv2.findContours(dilated, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if not 0.5 < (w * h) / area < 0.95: continue
        cv2.rectangle(image, (x,y), (x+w, y+h), 색.빨, 3)
        cv2.drawContours(image, [cnt], -1, 색.파, 3)
        poly = cv2.approxPolyDP(cnt, epsilon=5, closed=True)
        cv2.drawContours(image, [poly], -1, 색.초, 3)

    # 출력
    return {
        'image': image,
        'gray': gray,
        'edged': edged,
        'dilated': dilated
    }


r = 모드.사진(main_proc, 0.3)
r.run()

