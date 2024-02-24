from . import base
import cv2
import cvlib
from cvlib.object_detection import draw_bbox

class Config(base.Config):
    pass


class Brain(base.Brain):

    """The autonomous Brain object, drives the vehicle autonomously based on information gathered by the sensors"""

    def __init__(self, config: Config, *arg):
        super().__init__(config, *arg)
        video = cv2.VideoCapture(0)

    def obj_detection(self):
        _, frame = self.video.read()
        box, label, conf = cvlib.detect_common_objects(frame)
        image = draw_bbox(frame, box, label, conf)

        cv2.imshow("Camera Feed", image)
    def logic(self):
        
        self.obj_detection()
        """If anything is detected by the distance_sensors, stop the car"""
        """
        # if anything is detected by the sensors, stop the car
        stop = False
        for distance_sensor in self.distance_sensors:
            if distance_sensor.distance < 0.25:
                self.vehicle.stop()
                stop = True

        if not stop:
            self.vehicle.drive_forward()"""
