import cv2
import os
import pickle

class 매트플롯:
    def __init__(self, main_proc, req_width):
        self.main_proc = main_proc
        self.req_width = req_width
        self.imglst = os.listdir('../images')
        self.idx = 0
        try:
            with open('data.txt', 'rb') as f:
                self.idx = pickle.load(f)['idx']
        except:
            pass

    def run(self):

        while True:
            image = cv2.imread('../images/%s' % self.imglst[self.idx])
            height, width = image.shape[:2] # 이미지 크기 구하기
            rat = self.req_width / width if self.req_width != 0 else 1

            out = self.main_proc(image)
            for o in range(0, len(out)):
                cv2.imshow("img %d" % o, cv2.resize(out[o], dsize=(0, 0), fx=rat, fy=rat))

            key = cv2.waitKey()
            print(hex(key))

            if key == 0x1B:
                break;
            elif key == 0x270000: #right
                self.idx += 1
                if len(self.imglst) <= self.idx:
                    self.idx = 0

            elif key == 0x250000: #left
                self.idx -= 1
                if len(self.imglst) < 0:
                    self.idx = len(self.imglst) - 1

            with open('data.txt', 'wb') as f:
                pickle.dump({'idx': self.idx}, f)

        cv2.destroyAllWindows()

class 사진:
    def __init__(self, main_proc, req_width):
        self.main_proc = main_proc
        self.req_width = req_width
        self.imglst = os.listdir('../images')
        self.idx = 0
        try:
            with open('data.txt', 'rb') as f:
                self.idx = pickle.load(f)['idx']
        except:
            pass

    def run(self):

        while True:
            image = cv2.imread('../images/%s' % self.imglst[self.idx])
            height, width = image.shape[:2] # 이미지 크기 구하기
            rat = self.req_width / width if self.req_width != 0 else 1

            out = self.main_proc(image)
            if isinstance(out, dict):
                print(type(out))
                for o in out.keys():
                    cv2.imshow(o, cv2.resize(out[o], dsize=(0, 0), fx=rat, fy=rat))
            else:
                for o in range(0, len(out)):
                    cv2.imshow("img %d" % o, cv2.resize(out[o], dsize=(0, 0), fx=rat, fy=rat))
                    cv2.imwrite("img %d.png" % o, out[o])

            key = cv2.waitKeyEx()
            print(hex(key))
            if key == 0x1B:
                break;
            elif key == 0x270000: #right
                self.idx += 1
                if len(self.imglst) <= self.idx:
                    self.idx = 0

            elif key == 0x250000: #left
                self.idx -= 1
                if len(self.imglst) < 0:
                    self.idx = len(self.imglst) - 1

            with open('data.txt', 'wb') as f:
                pickle.dump({'idx': self.idx}, f)

        cv2.destroyAllWindows()

class 카메라:
    def __init__(self, main_proc, rat):
        self.main_proc = main_proc
        self.rat = rat

    def run (self):
        cap = cv2.VideoCapture('http://172.30.1.55:8080/video/mjpeg')

        while True:
            retval, image = cap.read()
            if not retval:
                break

            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)  # 회전

            out = self.main_proc(image)
            for o in out:
                cv2.imshow(o, cv2.resize(out[o], dsize=(0, 0), fx=self.rat, fy=self.rat))

            key = cv2.waitKey(25)
            if key == 27:
                break

        if cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()
