import os.path
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa

type Pos = tuple[int, int]  # (x,y)
type Dir = tuple[int, int]  # (x,y)

DIRS: dict[str, Dir] = {
    "n": (-1, -1),
    "ne": (1, -1),
    "nw": (-2, 0),
    "s": (1, 1),
    "se": (2, 0),
    "sw": (-1, 1),
}


# see solution to https://adventofcode.com/2020/day/24
# again using "Doubled coordinates"
# see https://www.redblobgames.com/grids/hexagons/#neighbors-doubled
def walking_distance(data: str) -> tuple[int, int]:
    global DIRS
    ORIGIN: Pos = (0, 0)
    pos: Pos = (0, 0)
    max_dist = 0
    for d_str in data.split(","):
        d: Dir = DIRS[d_str]
        pos = (pos[0]+d[0], pos[1]+d[1])
        max_dist = max(max_dist, manhatten_hex(pos, ORIGIN))
    dist = manhatten_hex(pos, ORIGIN)
    return dist, max_dist


# https://www.redblobgames.com/grids/hexagons/#distances-doubled
def manhatten_hex(p1: Pos, p2: Pos) -> int:
    dx = abs(p1[0]-p2[0])
    dy = abs(p1[1]-p2[1])
    dist = dy + max(0, (dx-dy)//2)
    return dist


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    p1, p2 = walking_distance(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
