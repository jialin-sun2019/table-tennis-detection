import numpy as np
import cv2
import time

class Camera_Process:
    def __init__(self, id):
        self.id=id
        self.cap = cv2.VideoCapture(self.id)
        self.Image_width,self.Image_Height = self.set_camera() #设置摄像头参数
        self.kernel = np.ones((5, 5), np.uint8)
        self.Low_H =5
        self.High_H=26
        self.Low_S = 110
        self.High_S = 245
        self.Low_V = 154
        self.High_V = 255
        self.Image_Window_Name="YelloBarTracker"
        self.Control_Window_Name='Control'
        self.Mask_Window_Nane='Mask'
    def __del__(self):
        self.cap.release()
    def set_camera(self, width=640, height=480):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        return width, height
    def nothing(self):
        pass
    def make_hsv_adjustment(self):
        cv2.namedWindow(self.Control_Window_Name)
        cv2.resizeWindow(self.Control_Window_Name,640,360)
        cv2.createTrackbar('Low_H', self.Control_Window_Name, self.Low_H, 255, self.nothing)
        cv2.createTrackbar('High_H', self.Control_Window_Name, self.High_H, 255, self.nothing)
        cv2.createTrackbar('Low_S', self.Control_Window_Name, self.Low_S, 255, self.nothing)
        cv2.createTrackbar('High_S', self.Control_Window_Name, self.High_S, 255, self.nothing)
        cv2.createTrackbar('Low_V', self.Control_Window_Name, self.Low_V, 255, self.nothing)
        cv2.createTrackbar('High_V', self.Control_Window_Name, self.High_V, 255, self.nothing)
    def main(self):
        self.make_hsv_adjustment()
        while self.cap.isOpened():
            ret, image0 = self.cap.read()
            if (ret):
                time_1 = time.time()
                hsv = cv2.cvtColor(image0, cv2.COLOR_BGR2HSV)
                self.Low_H = cv2.getTrackbarPos('Low_H', self.Control_Window_Name)
                self.High_H = cv2.getTrackbarPos('High_H', self.Control_Window_Name)
                self.Low_S = cv2.getTrackbarPos('Low_S', self.Control_Window_Name)
                self.High_S = cv2.getTrackbarPos('High_S', self.Control_Window_Name)
                self.Low_V = cv2.getTrackbarPos('Low_V', self.Control_Window_Name)
                self.High_V = cv2.getTrackbarPos('High_V', self.Control_Window_Name)
                lower_yellow = np.array([self.Low_H, self.Low_S, self.Low_V])
                upper_yellow = np.array([self.High_H, self.High_S, self.High_V])
                mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
                cv2.imshow(self.Mask_Window_Nane, mask)
                e_mask = cv2.erode(mask, self.kernel, iterations=1)
                cv2.imshow("e_mask", e_mask)
                p_mask = cv2.dilate(e_mask, self.kernel, iterations=1)
                cv2.imshow("p_mask", p_mask)
                contours, hierarchy = cv2.findContours(p_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                contour = list()
                areas = [cv2.contourArea(contours[i]) for i in range(len(contours))]
                if len(areas) != 0:
                    contour.append(contours[areas.index(max(areas))])
                cv2.drawContours(image0, contour, -1, (0, 0, 255), 3)
                print('time{}'.format((time.time() - time_1)))
                cv2.imshow(self.Image_Window_Name, image0)
                if cv2.waitKey(1)==27:
                    self.cap.release()
                    break
if __name__ == '__main__':
    camera = Camera_Process(0)
    camera.main()
