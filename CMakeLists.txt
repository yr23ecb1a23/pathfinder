cmake_minimum_required(VERSION 3.21)
project(pathfinder)
set(CMAKE_CXX_STANDARD 23)
add_subdirectory(lib/pybind11)
pybind11_add_module(pathfinder_mod main.cpp cpp_src/MapInterfacer.cpp cpp_src/MapInterfacer.h cpp_src/FileHandler.h cpp_src/FileHandler.cpp
        cpp_src/MapData.cpp cpp_src/MapData.h)