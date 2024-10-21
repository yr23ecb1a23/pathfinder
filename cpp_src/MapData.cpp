//
// Created by YASH RAMESHKUMAR on 10/20/2024.
//

#include "MapData.h"

namespace pathfinder {
        std::vector<int_fast8_t> MapData::getMapAsVector() const {
                return std::vector<int_fast8_t>(map.get(), map.get() + (length * width));
        }

        void MapData::setValueInMap(int index, int_fast8_t val) {
                map[index] = val;
        }
}
