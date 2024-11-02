from src import test
import os
import sys

module_path = os.path.abspath("./build")
test.someRandomTest()
if module_path not in sys.path:
    sys.path.append(module_path)

#from pathfinder_mod import *


#print(cpp_addFloat(102,123))
