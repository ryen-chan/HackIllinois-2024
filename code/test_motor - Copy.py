import numpy as np
from src import motor as motor_module
import time

if __name__ == '__main__':

    motor1 = motor_module.Motor({
        "pins": {
            "speed": 13,
            "control1": 5,
            "control2": 6
        }
    })

    motor2 = motor_module.Motor({
        "pins": {
            "speed": 12,
            "control1": 7,
            "control2": 8
        }
    })


    #angle is an input from a different module

    angle = 92
    theta = angle - 90
    speed = 0.5
    if -5 <= theta <= 5:
        motor1.forward(speed)
        motor2.forward(speed)
        time.sleep(5)
        motor1.stop()
        motor2.stop()
    elif 5 <= theta < 90:
        motor1.backward(speed)
        motor2.forward(speed)
        time.sleep(5)
        motor1.stop()
        motor2.stop()
    elif -90 < theta < -5:
        motor1.forward(speed)
        motor2.backward(speed)
        time.sleep(5)
        motor1.stop()
        motor2.stop()

motor1.stop()
motor2.stop()
        
        
