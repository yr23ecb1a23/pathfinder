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

motor1 = motor.Motor(24, 23, 25, 100, 0)  # left motor
motor2 = motor.Motor(17, 27, 22, 100, 0)

motor1.move_forward()


state = robot_state.RobotState()
# for i in range(10):
#     print(state.getAngleDegrees())
#     sleep(0.34)

sleep(20)
motor1.stop_motor()
state.destroy()