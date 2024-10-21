#include <iostream>
#include <pybind11/pybind11.h>

#include "cpp_src/FileHandler.h"
#include "cpp_src/MapInterfacer.h"

namespace py = pybind11;


void something() {
    std::cout << "HEllo world something\n" << std::endl;
    // return;
}

float addFloat(float a, float b) {
    std::cout << a+b << "Hello world" << std::endl;
    return a+b;
}

PYBIND11_MODULE(pathfinder_mod, handle) {
    handle.doc() = "Some shitty documentation for this purpose";
    handle.def("cpp_addFloat", &addFloat);
    py::class_<pathfinder::MapData>(handle, "MapData")
        .def(py::init<>())
        .def_readwrite("length", &pathfinder::MapData::length)
        .def_readwrite("width", &pathfinder::MapData::width)
        .def_readwrite("accuracy", &pathfinder::MapData::accuracy)
        .def("get_map_as_vector", &pathfinder::MapData::getMapAsVector)
        .def("setValueInMap", &pathfinder::MapData::setValueInMap);
    py::class_<pathfinder::FileHandler>(handle, "FileHandler")
        .def(py::init<std::string, pathfinder::mode_t>(), py::arg("filename"), py::arg("mode"))
        .def("getMapData", &pathfinder::FileHandler::getMapData)
        .def("writeMapData", &pathfinder::FileHandler::writeMapData);
    py::enum_<pathfinder::mode_t>(handle, "Mode")
        .value("read", pathfinder::mode_t::read)
        .value("write", pathfinder::mode_t::write)
        .export_values();
}


