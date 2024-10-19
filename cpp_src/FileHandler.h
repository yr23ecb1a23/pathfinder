//
// Created by YASH RAMESHKUMAR on 10/19/2024.
//

#ifndef FILEHANDLER_H
#define FILEHANDLER_H
#include <cstdint>
#include<fstream>
#include <iostream>
#include <vector>

namespace pathfinder {

class FileHandler {
private:
    static std::ofstream* outputFile;
    bool isOpen = false;
    std::string filename;
public:
    FileHandler(std::string filename);
    bool openFile();
    static inline std::ofstream* getOfstream();
    static inline bool write(long long num);
    static inline bool write(int_fast8_t num);
    static inline bool write(std::vector<int_fast8_t> arr);
};

} // pathfinder

#endif //FILEHANDLER_H
