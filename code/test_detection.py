import cv2
import cvlib
from cvlib.object_detection import draw_bbox

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

def obj_detection():
 
    #frame = cv2.imread('C:\\Users\\ryan\\Desktop\\OpenCV Test\\Cute_dog.jpg')
    ret, frame = video.read()
    if not ret:
        print("Could not read frame")
        exit()

    box, label, conf = cvlib.detect_common_objects(frame, confidence=0.25, model='yolov3-tiny')
    image = draw_bbox(frame, box, label, conf)
    cv2.imshow("Camera Feed", image)


while True:
    obj_detection()
    
    #_, frame = video.read()
    #cv2.imshow("Camera Feed", frame)
    
    if(cv2.waitKey(1) == ord("q")):
        break
        
video.release()
cv2.destroyAllWindows()
