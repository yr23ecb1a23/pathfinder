//
// Created by yash on 10/17/24.
//

#include "MapInterfacer.h"
#include <iostream>
#include <memory>

namespace pathfinder {
    /**
     * 
     * @param n the number of rows inside of this map, meaning the length of the map
     * @param m the number of columns inside of this map, the width of this map
     */
    MapInterfacer::MapInterfacer(ll n, ll m):length(m), width(n) {
        map = new int_fast8_t*[n];
        for(int i = 0; i < n; i++) {
            map[i] = new int_fast8_t[m];
        }
    }

    MapInterfacer::~MapInterfacer() {
        std::cout << "Destroying the Map interface class";
    }

    bool MapInterfacer::setDestination(long long a, long long b) {
        return true;
    }
} // pathfinder