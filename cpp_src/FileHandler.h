//
// Created by YASH RAMESHKUMAR on 10/19/2024.
//

#ifndef FILEHANDLER_H
#define FILEHANDLER_H
#include <cstdint>
#include<fstream>
#include <iostream>
#include <vector>

#include "MapData.h"
namespace pathfinder {
    enum mode_t {
        read, write
    };
    class FileHandler {
    private:
        bool isOpen = false;
        mode_t mode;
        std::string filename;
    public:
        FileHandler(std::string filename, mode_t mode);
        MapData getMapData();
        bool writeMapData(MapData &mapData);
    };

} // pathfinder

#endif //FILEHANDLER_H
