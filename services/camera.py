import time

import cv2


def store_frame(frame):
    ts = int(time.time())
    filename = "{}.jpg".format(ts)

    return cv2.imwrite(filename, frame)


class Camera:

    def __init__(self):
        self.cam = cv2.VideoCapture(0)

    def capture_frame(self):
        return self.cam.read()
