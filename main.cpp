#include <iostream>
#include <pybind11/pybind11.h>


namespace py = pybind11;


class trial {
    public:
    trial(){
        std::cout << "Trial of the classes;";
    }
};


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
}


