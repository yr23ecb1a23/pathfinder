from src import test, robot_state, motor
import os
import sys
import threading
from time import sleep

module_path = os.path.abspath("./build")
test.someRandomTest()
if module_path not in sys.path:
    sys.path.append(module_path)

#from pathfinder_mod import *


#print(cpp_addFloat(102,123))

is_on = True


def staller():
    global is_on
    is_on = True
    print("inside")
    sleep(0.6)
    is_on = False


rightMotor = motor.Motor(24, 23, 25, 100, 0)  # left motor
leftMotor = motor.Motor(17, 27, 22, 100, 0)
state = robot_state.RobotState()
rightMotor.move_forward()
rightMotor.set_motor_speed(50)
leftMotor.move_forward()
leftMotor.set_motor_speed(50)

# for i in range(10):
#     print(state.getAngleDegrees())
#     sleep(0.34)
inp = True
while inp:
    number_thread = threading.Thread(target=staller)
    leftMotor.move_forward()
    rightMotor.move_forward()
    number_thread.start()
    while is_on:
        angle = state.getAngleDegrees()
        print(angle)
        if angle > 0.17:
            #print("burst left")
            leftMotor.set_motor_speed(100-40)
            rightMotor.set_motor_speed(50-40)
        elif angle < -0.17:
            #print("burst right")
            leftMotor.set_motor_speed(50-40)
            rightMotor.set_motor_speed(100-40)
        else:
            rightMotor.set_motor_speed(50)
            leftMotor.set_motor_speed(50)
    number_thread.join()
    rightMotor.stop_motor()
    leftMotor.stop_motor()
    a = int(input())
    if a == 1:
        pass
    else:
        print("exiting")
        inp = False
state.destroy()
