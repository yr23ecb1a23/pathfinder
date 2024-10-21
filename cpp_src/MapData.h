//
// Created by YASH RAMESHKUMAR on 10/20/2024.
//

#ifndef MAPDATA_H
#define MAPDATA_H
#include <cstdint>
#include <memory>
#include <vector>


using shared_ptr_intfast8_array = std::shared_ptr<int_fast8_t[]>;
namespace pathfinder {

class MapData {
public:
    int length;
    int width;
    int_fast8_t accuracy;
    std::shared_ptr<int_fast8_t[]> map;

    MapData(): length(0), width(0), accuracy(0) {

    }
    // EXPOSING THE STL VECTOR TO PYTHON LIST
    std::vector<int_fast8_t> getMapAsVector() const;
    inline void setValueInMap(int index, int_fast8_t val);
};
}


#endif //MAPDATA_H
