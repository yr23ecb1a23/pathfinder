//
// Created by yash on 10/17/24.
//

#include "MapInterfacer.h"
#include <iostream>

namespace pathfinder {
    MapInterfacer::MapInterfacer() {
        std::cout << "Initialised the Map interface class";
    }

    MapInterfacer::~MapInterfacer() {
        std::cout << "Destroying the Map interface class";
    }

    bool MapInterfacer::setDestination(long long a, long long b) {
        return true;
    }
} // pathfinder