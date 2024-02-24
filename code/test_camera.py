from src import camera as camera_module
import time

import cv2
import cvlib
from cvlib.object_detection import draw_bbox

def obj_detection():
        _, frame = video.read()
        box, label, conf = cvlib.detect_common_objects(frame)
        image = draw_bbox(frame, box, label, conf)
        cv2.imshow("Camera Feed", image)

if __name__ == '__main__':

    video = cv2.VideoCapture(0)

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
        time.sleep(max(0, 1/sample_hz -
                       (time.time() - start_time)))
