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

    dt = 20
    time.time()
    angle = list(np.linspace(115,65,11))
    for x in angle:
        theta = angle - 90
        speed = 0.4
        if -5 <= theta <= 5:
            motor1.forward(speed)
            motor2.forward(speed)
        elif 5 <= theta < 90:
            motor1.backward(speed)
            motor2.forward(speed)
        elif -90 < theta < -5:
            motor1.forward(speed)
            motor2.backward(speed)