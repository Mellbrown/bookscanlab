import cv2
import 모드

class Boundary(object):
    def __init__(self, image):
        self.out = []
        self.frame = image
        self.DefineBounds()


    def DefineBounds(self):

        # convert the image to grayscale, blur it, and detect edges
        # other options are four point detection, white color detection to search for the board?

        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 35, 125)

        # find the contours in the edged image and keep the largest one;
        # we'll assume that this is our piece of paper in the image
        # (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        th, contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        c = max(contours, key=cv2.contourArea)

        # compute the bounding box of the of the paper region and return it
        cv2.drawContours(self.frame, c, -1, (0, 255, 0), 3)
        # cv2.imshow("B and W", edged)
        # cv2.imshow("capture", self.frame)
        self.out.append(edged)
        self.out.append(self.frame)
        # cv2.waitKey(0)

        # minAreaRect returns (center (x,y), (width, height), angle of rotation )
        # width = approx 338 (x-direction
        # height = 288.6 (y-direction)

        self.CenterBoundBox = cv2.minAreaRect(c)[0]
        print("Center location of bounding box is {}".format(self.CenterBoundBox))
        CxBBox = cv2.minAreaRect(c)[0][1]
        CyBBox = cv2.minAreaRect(c)[0][0]

        # prints picture resolution
        self.OGImageHeight, self.OGImageWidth = self.frame.shape[:2]
        #print("OG width {} and height {}".format(self.OGImageWidth, self.OGImageHeight))

        print(cv2.minAreaRect(c))
        BboxWidth = cv2.minAreaRect(c)[1][1]
        BboxHeight = cv2.minAreaRect(c)[1][0]

        self.Px2CmWidth = BboxWidth / 21.5  # 1cm = x many pixels
        self.Px2CmHeight = BboxHeight / 18  # 1cm = x many pixels
        print("Bbox diemensions {}  x  {}".format(BboxHeight, BboxWidth))
        print("Conversion values Px2Cm width {}, Px2Cm height {}".format(self.Px2CmWidth, self.Px2CmHeight))

        self.TopLeftCoords = (abs(CxBBox - BboxWidth/2), abs(CyBBox - BboxHeight/2))
        x = int(round(self.TopLeftCoords[0]))
        y = int(round(self.TopLeftCoords[1]))
        print("X AND Y COORDINATES")
        print(x)
        print(y)
        cv2.rectangle(self.frame, (x, y), (x+10, y+10), (0, 255, 0), 3)
        print(self.TopLeftCoords)

        # cv2.imshow("BOX",self.frame)

        # cv2.waitKey(0)

def main_proc(src):
    return Boundary(src).out

r = 모드.사진(main_proc, 500)
r.run()
