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

    angle = 99
    total_seconds = 60
    dt = 0.25
    start_time = time.time()
    while time.time() - start_time < total_seconds:
        theta = angle - 90
        speed = 0.35
        new_speed = 0.45
        if -5 <= theta <= 5:
            motor1.forward(speed)
            motor2.forward(speed)
            time.sleep(dt)
        elif 5 <= theta < 90:
            motor1.forward(speed)
            motor2.forward(new_speed)
            time.sleep(dt)
        elif -90 < theta < -5:
            motor1.forward(speed)
            motor2.backward(new_speed)
            time.sleep(dt)
    motor1.stop()
    motor2.stop()