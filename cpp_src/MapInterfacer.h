//
// Created by yash on 10/17/24.
//

#ifndef MAPINTERFACER_H
#define MAPINTERFACER_H
#define ll long long
#include <climits>
#include <cstdint>
#include <memory>
#include <vector>

namespace pathfinder {

enum Direction { UP=-1, DOWN=+1, LEFT=-2, RIGHT=+2 };

class MapInterfacer {
private:
    ll dest_x = LONG_MIN;
    ll dest_y = LONG_MIN;
    ll length = LONG_MIN;
    ll width = LONG_MIN;
    int_fast8_t **map = nullptr;
    std::vector<Direction> path;
public:
    MapInterfacer(ll n, ll m); // the size of the map
    ~MapInterfacer();
    static bool setDestination(ll a, ll b);
    std::vector<int_fast8_t> getNeighbours(ll x, ll y);
    void computePath(ll x, ll y);
};

} // pathfinder

#endif //MAPINTERFACER_H
