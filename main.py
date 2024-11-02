from src import test, robot_state
import os
import sys
from time import sleep

module_path = os.path.abspath("./build")
test.someRandomTest()
if module_path not in sys.path:
    sys.path.append(module_path)

#from pathfinder_mod import *


#print(cpp_addFloat(102,123))

state = robot_state.RobotState()
for i in range(10):
    print(state.getAngleDegrees())
    sleep(0.34)


state.destroy()