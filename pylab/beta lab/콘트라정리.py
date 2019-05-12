import math
import cv2

class 콘트라정리:
    def __init__(self, cnt, height):
        self.poly = cv2.approxPolyDP(cnt, epsilon=3, closed=True)
        self.height = height
        self.cnt = cnt
        self.points = self.pointVector(cnt, height)

    def pointVector (self, cnt, height):
        l = len(cnt)
        points = []
        for i in range(0, l):
            x1, y1 = cnt[i][0]
            x2, y2 = cnt[i+1 if i+1 < l else 0][0]
            iy1, iy2 = height - y1, height - y2

            rad = math.atan2((iy2-iy1), (x2-x1))
            deg = rad * 180.0 / math.pi
            deg = deg if deg >= 0 else 360 + deg

            length = math.sqrt((x2-x1) ** 2 + (iy2-iy1) ** 2)

            points.append(((x1,y1),deg, length))


            lbi = int((deg + 22.5) / 45)
            lbi = lbi if lbi < 8 else 0
            deg_lb = ["→" , "↗", "↑", "↖", "←", "↙", "↓", "↘"]
            print('%s ,%d %d (%d, %d) -> (%d, %d)' % (deg_lb[lbi], deg, length, x1, y1, x2, y2))
        return points



    def fitLine(self, ctn, start, end, height):
        l = len(ctn)
        s = ctn[start][0]
        e = ctn[end if end < l else end - l][0]
        x1, y1 = s[0], height - s[1]
        x2, y2 = e[0], height - e[1]
        a = (y2-y1) / (x2-x1)
        y = a*x + b
        b = y1


    def growLine(self, start):
        # 직선 떨림
        초기갯수 = 10
        자람허용오차 = 10
        end = start + 초기갯수