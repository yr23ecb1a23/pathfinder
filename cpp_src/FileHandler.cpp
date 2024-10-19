//
// Created by YASH RAMESHKUMAR on 10/19/2024.
//

#include "FileHandler.h"

#include <utility>

namespace pathfinder {
    FileHandler::FileHandler(std::string filename):filename(std::move(filename)) {

    }
    bool FileHandler::openFile () {
        FileHandler::outputFile = new std::ofstream(filename, std::ios::binary);
        isOpen = true;
        if(!*outputFile) {
            std::cerr << "Some error while opening the file";
            isOpen = false;
        }
        return isOpen;
    }

    std::ofstream *FileHandler::getOfstream() {
        return outputFile;
    }

    bool FileHandler::write(long long num) {
        (*outputFile).write(reinterpret_cast<const char*>(&num), sizeof(long long));
        return true;
    }

    bool FileHandler::write(int_fast8_t num) {
        (*outputFile).write(reinterpret_cast<const char*>(&num), sizeof(int_fast8_t));
        return true;
    }

    bool FileHandler::write(std::vector<int_fast8_t> arr) {
        (*outputFile).write(reinterpret_cast<const char*>(arr.data()), arr.size() * sizeof(int_fast8_t));
    }

    
} // pathfinder