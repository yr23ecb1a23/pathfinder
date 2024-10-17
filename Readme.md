# Github repo for the delivery robot DT Project

### This code uses `C++` for many of its heavy computation part, as the memory on the Raspberry pi is much limited, and uses `Python` for most of its functioning , and interfacing with the sensors, and other things that might include *connecting to server to serve actual customers' requests*.

### This python code can call actual functions, classes, and other constructs written  in C++, from Python code itself.

Before running this code on your machine, make sure you have 
- python 3.11 and above installed
- pybind installed using pip `pip install pybind11`
- cmake 3.21 and above installed on your system

To run this code on your machine

first copy this code to your machine using

`git clone https://github.com/devyk100/pathfinder.git` or `git clone git@github.com:devyk100/pathfinder.git`

Then follow the instructions for the first time setup
1. `mkdir build`
2. `cd build`
3. `cmake ..`
4. `make`
5. `python main.py` or `python3 main.py`

If you are editing the cpp_src, or the main.cpp, make sure your changes reflect in the CmakeLists.txt too. And to test them make sure you compile to test them
1. `cd build`
2. `cmake ..`
3. `make`
And then run the main.py

If you are editing the python files, you need not do any of this, just run the main.py file again.
