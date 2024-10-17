//
// Created by yash on 10/17/24.
//

#ifndef MAPINTERFACER_H
#define MAPINTERFACER_H
#define ll long long
#include <climits>

namespace pathfinder {

class MapInterfacer {
    ll dest_x = LONG_MIN;
    ll dest_y = LONG_MIN;
public: MapInterfacer();
    ~MapInterfacer();

    static bool setDestination(ll a, ll b);
private:
};

} // pathfinder

#endif //MAPINTERFACER_H
