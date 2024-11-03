from src import test, robot_state, motor
import os
import sys
import threading
from time import sleep
import cv2
import numpy as np

module_path = os.path.abspath("./build")
test.someRandomTest()
if module_path not in sys.path:
    sys.path.append(module_path)

is_on = True

# Initialize camera
cap = cv2.VideoCapture(0)  # Change 0 to the appropriate camera index if necessary

# Feature detector
orb = cv2.ORB_create()

# Define variables for visual odometry
prev_kp, prev_des = None, None
current_position = np.array([0.0, 0.0])  # Initialize position


def staller():
    global is_on
    is_on = True
    print("inside")
    sleep(1.6)
    is_on = False


rightMotor = motor.Motor(24, 23, 25, 100, 0)  # left motor
leftMotor = motor.Motor(17, 27, 22, 100, 0)
state = robot_state.RobotState()
rightMotor.move_forward()
rightMotor.set_motor_speed(50)
leftMotor.move_forward()
leftMotor.set_motor_speed(50)

iterations = 0

inp = True
while inp:
    number_thread = threading.Thread(target=staller)
    leftMotor.move_forward()
    rightMotor.move_forward()
    number_thread.start()

    while is_on:
        angle = state.getAngleDegrees()
        print(angle, state.getDisp())
        if angle > 0.17:
            leftMotor.set_motor_speed(100 - 40)
            rightMotor.set_motor_speed(50 - 40)
        elif angle < -0.17:
            leftMotor.set_motor_speed(50 - 40)
            rightMotor.set_motor_speed(100 - 40)
        else:
            rightMotor.set_motor_speed(50)
            leftMotor.set_motor_speed(50)

    number_thread.join()
    rightMotor.stop_motor()
    leftMotor.stop_motor()
    a = int(input())
    iterations += 1
    sleep(0.1)
    if iterations > 3:
        pass
    else:
        print("exiting")
        inp = False
state.destroy()
# pomafdspogpofas
