import numpy as np
import cv2
import time

class Camera_Process:
    def __init__(self, id):
        self.id=id
        self.cap = cv2.VideoCapture(self.id)
        self.Image_width,self.Image_Height = self.set_camera() #设置摄像头参数
    def set_camera(self, width=640, height=480):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        return width, height
    def main(self):
        self.set_camera(width=640, height=480)
        while self.cap.isOpened():
            ret, image0 = self.cap.read()
            if (ret):
                time_1 = time.time()
                frame_gray = cv2.cvtColor(image0, cv2.COLOR_BGR2GRAY)
                frame_median = cv2.medianBlur(frame_gray,5)
                circles = cv2.HoughCircles(
                    frame_median,
                    cv2.HOUGH_GRADIENT,
                    1,
                    120,
                    param1=100,
                    param2=30,
                    minRadius=30,
                    maxRadius=90
                )
                best_circle = [0, 0, 0]
                if circles is None:
                    print("none")
                else:
                    circles = np.uint16(np.around(circles))
                    for i in circles[0, :]:
                        cv2.circle(image0, (i[0], i[1]), i[2], (0, 255, 0), 2)
                        cv2.circle(image0, (i[0], i[1]), 2, (0, 0, 255), 3)
                print('time:{0:.3f}ms'.format(((time.time() - time_1) * 1000)))
                cv2.imshow("out", image0)
                if cv2.waitKey(1)==27:
                    self.cap.release()
                    break
if __name__ == '__main__':
    camera = Camera_Process(0)
    camera.main()
