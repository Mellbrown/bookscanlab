import cv2
import os

def get_contours(image):
    # 그레이 스케일 먹이고, 가우시안 블루 먹인다.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    # 엣지 검출 시킨다.
    edged = cv2.Canny(blurred, 0, 30)

    # 윤곽선 검출 한다.
    (_, contours, _) = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    return contours

