from src import test, robot_state, motor
import os
import sys
from time import sleep

module_path = os.path.abspath("./build")
test.someRandomTest()
if module_path not in sys.path:
    sys.path.append(module_path)

#from pathfinder_mod import *


#print(cpp_addFloat(102,123))

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

while True:
    if(state.getAngleDegrees() > 1):
        print("burst left")
        leftMotor.set_motor_speed(70)
        rightMotor.set_motor_speed(0)
    elif(state.getAngleDegrees() < -1):
        print("burst right")
        leftMotor.set_motor_speed(0)
        rightMotor.set_motor_speed(70)
    else:
        rightMotor.set_motor_speed(50)
        leftMotor.set_motor_speed(50)
sleep(20)
rightMotor.stop_motor()
leftMotor.stop_motor()
state.destroy()
