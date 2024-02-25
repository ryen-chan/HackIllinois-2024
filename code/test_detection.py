import cv2
import cvlib
from cvlib.object_detection import draw_bbox
from picamera2 import Picamera2

"""
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
"""

def obj_detection():
 
    #frame = cv2.imread('C:\\Users\\ryan\\Desktop\\OpenCV Test\\Cute_dog.jpg')
    frame = picam2.capture_array()
    #cv2.flip(picam2.capture_array(),-1)
    """
    ret, frame = video.read()
    if not ret:
        print("Could not read frame")
        exit()
    """
    box, label, conf = cvlib.detect_common_objects(frame) #, confidence=0.25, model='yolov3-tiny')
    image = draw_bbox(frame, box, label, conf)
    cv2.imshow("Camera Feed", image)

# Grab images as numpy arrays and leave everything else to OpenCV.
cv2.startWindowThread()

picam2 = Picamera2()
#'XRGB8888'
picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (320, 240)}))
picam2.start()

#video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    obj_detection()  
    if(cv2.waitKey(1) == ord("q")):
        break
        
picam2.release()
cv2.destroyAllWindows()



  
