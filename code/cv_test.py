#!/usr/bin/python3

import cv2

from picamera2 import Picamera2

# Grab images as numpy arrays and leave everything else to OpenCV.
cv2.startWindowThread()

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (320, 240)}))
picam2.start()

while True:
    im = picam2.capture_array()

    cv2.imshow("cam", im)
    key = cv2.waitKey(1)
    
    if key == 27:
     break

video.release()
cv2.destroyAllWindows()


  
