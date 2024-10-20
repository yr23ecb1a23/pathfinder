//
// Created by YASH RAMESHKUMAR on 10/19/2024.
//

#include "FileHandler.h"

#include <utility>

namespace pathfinder {
    FileHandler::FileHandler(std::string filename, mode_t m):filename(std::move(filename)), mode(m) {
    }

#define read_from_file(file, data, size) file.read(reinterpret_cast<char*>(data), size)
    MapData FileHandler::getMapData() {
        MapData raw;
        if(mode == write) {
            std::cerr << "please use the file handler in the reading mode";
            return raw;
        }
        auto rfile = std::ifstream(filename, std::ios::binary);
        read_from_file(rfile, &raw.length, sizeof(raw.length));
        read_from_file(rfile, &raw.width, sizeof(raw.width));
        read_from_file(rfile, &raw.accuracy, sizeof(raw.accuracy));
        auto *rawMap = new int_fast8_t[raw.length * raw.width];
        read_from_file(rfile, rawMap, sizeof(rawMap[0])*raw.length*raw.width);
        raw.map = std::shared_ptr<int_fast8_t[]>(rawMap);
        rfile.close();
        return raw;
    }

#define write_to_file(file, data, size) file.write(reinterpret_cast<const char*>(data), size)
    bool FileHandler::writeMapData(MapData &mapData) {
        if(mode == read) {
            std::cerr << "The file handler was opened in the writing mode and not the reading mode";
            return false;
        }
        auto ofile = std::ofstream(filename, std::ios::binary);
        write_to_file(ofile, &mapData.length, sizeof(mapData.length));
        write_to_file(ofile, &mapData.width, sizeof(mapData.width));
        write_to_file(ofile, &mapData.accuracy, sizeof(mapData.accuracy));
        write_to_file(ofile, mapData.map.get(), sizeof(*(mapData.map.get()))*mapData.length*mapData.width);
        ofile.close();
        return true;
    }

} // pathfinder