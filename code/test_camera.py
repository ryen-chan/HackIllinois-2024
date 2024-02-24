"""

from src import camera as camera_module
import time

import cv2

cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)

#set dimensions
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)

    total_seconds = 60
    sample_hz = 10

    camera = camera_module.Camera({
        "show_preview": False
    })

start_time = time.time()

while time.time() - start_time < total_seconds:
    camera.capture()
    print(camera.image_array)
    #obj_detection()
    time.sleep(max(0, 1/sample_hz - (time.time() - start_time)))
"""

from picamera import PiCamera
from time import sleep

if __name__ == '__main__':
    camera = PiCamera()

    camera.start_preview()
    sleep(5)
    camera.stop_preview()
"""
    total_seconds = 60
    sample_hz = 10

    camera = camera_module.Camera({
        "show_preview": False
    })
    start_time = time.time()

    while time.time() - start_time < total_seconds:
        camera.capture()
        print(camera.image_array)

        time.sleep(max(0, 1/sample_hz -
                       (time.time() - start_time)))
"""
