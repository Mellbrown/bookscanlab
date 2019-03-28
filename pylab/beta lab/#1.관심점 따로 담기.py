import cv2
import numpy as np
import 모드 as mode
import 색

def resolution_info(image): # 사진 해상도 조사
    height, width = image.shape[:2]
    clp = height if height < width else width
    clp_small = clp * 0.3
    clp_large = clp * 0.5
    return height, width, clp_small, clp_large


def box_info (con): # 박스 조사
    rect = cv2.minAreaRect(con)
    origin, size, angle = rect
    box = cv2.boxPoints(rect)
    box = np.int32(box)
    return box, origin, size, angle


def main_proc(image, contours):
    height, width, clp_small, clp_large = resolution_info(image)
    canvas = np.zeros(shape=(height, width, 3), dtype=np.uint8)

    filtered_con = []
    for con in contours:
        box, origin, (h, w), angle = box_info(con)

        if h > clp_large and w > clp_large: # 큰사이즈
            filtered_con.append(con)
            cv2.drawContours(image, filtered_con, -1, 색.시안, 1)

        elif h > clp_small or w > clp_small: # 중간 사이즈
            # 세로선
            vx, vy, x, y = cv2.fitLine(con, cv2.DIST_L2, 0, 0.01, 0.01)
            if vx > 0.3: continue
            cv2.drawContours(image, filtered_con, -1, 색.노, 2)
            filtered_con.append(con)


    print(len(filtered_con))

    # 출력
    return {
        'image': image
    }


r = mode.PictureMode(main_proc)
r.run(3)

