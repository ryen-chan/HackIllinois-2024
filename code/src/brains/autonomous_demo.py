from . import base
import cv2
import numpy as np
import math
import sys
import time
from picamera2 import Picamera2

class Config(base.Config):
    pass


class Brain(base.Brain):

    """The autonomous Brain object, drives the vehicle autonomously based on information gathered by the sensors"""

    def __init__(self, config: Config, *arg):
        super().__init__(config, *arg)

    def logic(self): #handles logic of car 
        
        # Grab images as numpy arrays via picam2 pass data to OpenCV.
        cv2.startWindowThread()

        picam2 = Picamera2()
        picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (360, 240)}))
        picam2.start()



        def detect_edges(frame):    #edge detection, convert to HSV
            # filter for blue lane lines
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            #cv2.imshow("HSV",hsv)
            lower_blue = np.array([90, 120, 0], dtype = "uint8")
            upper_blue = np.array([150, 255, 255], dtype="uint8")
            mask = cv2.inRange(hsv,lower_blue,upper_blue)
            #cv2.imshow("mask",mask)
            
            # detect edges
            edges = cv2.Canny(mask, 50, 100)    #canny detection
            #cv2.imshow("edges",edges)
            
            return edges

        def region_of_interest(edges):
            height, width = edges.shape
            mask = np.zeros_like(edges)

            # only focus lower half of the screen
            polygon = np.array([[
                (0, height),
                (0,  height/2),
                (width , height/2),
                (width , height),
            ]], np.int32)
            
            cv2.fillPoly(mask, polygon, 255)
            
            cropped_edges = cv2.bitwise_and(edges, mask)
            cv2.imshow("roi",cropped_edges)     #show region of interest
            
            return cropped_edges

        def detect_line_segments(cropped_edges):    #overlay line segments using HoughLinesP(robalistic)
            rho = 1    #resolution of r
            theta = np.pi / 180  #resolution of theta
            min_threshold = 10   #minimum number of intersections to count as line
            
            line_segments = cv2.HoughLinesP(cropped_edges, rho, theta, min_threshold, 
                                            np.array([]), minLineLength=5, maxLineGap=150)

            return line_segments

        def average_slope_intercept(frame, line_segments): #averge slope of Hough Lines
            lane_lines = []
            
            if line_segments is None:
                print("no line segments detected")
                return lane_lines

            height, width,_ = frame.shape
            left_fit = []
            right_fit = []

            boundary = 1/3
            left_region_boundary = width * (1 - boundary)
            right_region_boundary = width * boundary
            
            for line_segment in line_segments:
                for x1, y1, x2, y2 in line_segment:
                    if x1 == x2:
                        #print("skipping vertical lines (slope = infinity)")
                        continue
                    
                    fit = np.polyfit((x1, x2), (y1, y2), 1)
                    slope = (y2 - y1) / (x2 - x1)
                    intercept = y1 - (slope * x1)
                    
                    if slope < 0:
                        if x1 < left_region_boundary and x2 < left_region_boundary:
                            left_fit.append((slope, intercept))
                    else:
                        if x1 > right_region_boundary and x2 > right_region_boundary:
                            right_fit.append((slope, intercept))

            left_fit_average = np.average(left_fit, axis=0)
            if len(left_fit) > 0:
                lane_lines.append(make_points(frame, left_fit_average))

            right_fit_average = np.average(right_fit, axis=0)
            if len(right_fit) > 0:
                lane_lines.append(make_points(frame, right_fit_average))

            return lane_lines

        def make_points(frame, line):   #bounded coordinates of the lane lines (helper)
            height, width, _ = frame.shape
            
            slope, intercept = line
            
            y1 = height  # bottom of the frame
            y2 = int(y1 / 2)  # make points from middle of the frame down
            
            if slope == 0:
                slope = 0.1
                
            x1 = int((y1 - intercept) / slope)
            x2 = int((y2 - intercept) / slope)
            
            return [[x1, y1, x2, y2]]

        def display_lines(frame, lines, line_color=(0, 255, 0), line_width=6): #draw lines
            line_image = np.zeros_like(frame)
            
            if lines is not None:
                for line in lines:
                    for x1, y1, x2, y2 in line:
                        cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)
                        
            line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
            
            return line_image


        def display_heading_line(frame, steering_angle, line_color=(0, 0, 255), line_width=5 ):
            heading_image = np.zeros_like(frame)
            height, width, _ = frame.shape
            
            steering_angle_radian = steering_angle / 180.0 * math.pi
            
            x1 = int(width / 2)
            y1 = height
            x2 = int(x1 - height / 2 / math.tan(steering_angle_radian))
            y2 = int(height / 2)
            
            cv2.line(heading_image, (x1, y1), (x2, y2), line_color, line_width)
            heading_image = cv2.addWeighted(frame, 0.8, heading_image, 1, 1)
            
            return heading_image

        def get_steering_angle(frame, lane_lines):
            
            height,width,_ = frame.shape
            
            if len(lane_lines) == 2:    #both lines detected
                _, _, left_x2, _ = lane_lines[0][0]
                _, _, right_x2, _ = lane_lines[1][0]
                mid = int(width / 2)
                x_offset = (left_x2 + right_x2) / 2 - mid
                y_offset = int(height / 2)
                
            elif len(lane_lines) == 1:  #only one line
                x1, _, x2, _ = lane_lines[0][0]
                x_offset = x2 - x1
                y_offset = int(height / 2)
                
            elif len(lane_lines) == 0: #no lines (infinte)
                x_offset = 0
                y_offset = int(height / 2)
                
            angle_to_mid_radian = math.atan(x_offset / y_offset)
            angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / math.pi)  
            steering_angle = angle_to_mid_deg + 90
            
            return steering_angle

        time.sleep(1)
        self.leds[2].off()
        self.leds[3].off()
        while True:
            frame = picam2.capture_array()
            
            #cv2.imshow("original",frame)
            edges = detect_edges(frame)
            roi = region_of_interest(edges)
            line_segments = detect_line_segments(roi)
            lane_lines = average_slope_intercept(frame,line_segments)
            lane_lines_image = display_lines(frame,lane_lines)
            steering_angle = get_steering_angle(frame, lane_lines)
            heading_image = display_heading_line(lane_lines_image,steering_angle)
            cv2.imshow("heading line",heading_image)
            
            key = cv2.waitKey(1)
            if key == 27:
                self.vehicle.stop()
                break
            
            sens1 = self.distance_sensors[0].distance
            sens2 = self.distance_sensors[1].distance
            stop_dist = 0.16
            
            if sens1 < stop_dist or sens2 < stop_dist: 
                self.vehicle.stop()
                self.leds[2].on()
                self.leds[3].on()
                for count in range(5):
                    time.sleep(0.5)
                    if(not (sens1 < stop_dist or sens2 < stop_dist)):
                        continue
                
                if(count == 4):
                    self.vehicle.pivot_right(0.8)
                    time.sleep(0.83)
                    self.leds[2].off()
                    self.leds[3].off()
                    continue
                
                self.leds[2].off()
                self.leds[3].off()
                continue
                
            now = time.time() # current time variable
            dt = 0.1 # time interval
            deviation = steering_angle - 90 # equivalent to angle_to_mid_deg variable
            #error = abs(deviation) 
            speed = 0.50
            turn_speed = 0.32
            
            """
            new_speed = speed*(1 + 0.015*deviation)
            if (new_speed >=1):
                new_speed = 1
            """
            
            if deviation < 6 and deviation > -6: # do not steer if there is a 10-degree error range
                deviation = 0
                error = 0
                self.vehicle.drive(speed*0.86,True,speed,True)
                time.sleep(dt*1.8)

            elif deviation > 6: # steer right if the deviation is positive
                self.vehicle.pivot_right(turn_speed)
                time.sleep(dt/2)

            elif deviation < -6: # steer left if deviation is negative
                self.vehicle.pivot_left(turn_speed)
                time.sleep(dt/2)


        cv2.destroyAllWindows()
