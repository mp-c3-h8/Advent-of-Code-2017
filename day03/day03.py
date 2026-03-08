import os.path
import os
import sys
from math import sqrt
from collections import defaultdict

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa

type Pos = tuple[int, int]  # (y,x) y downwards


def steps(data: int) -> int:
    if data == 1:
        return 0

    s = int((sqrt(data)-1)/2)  # number of square
    while (2*s+1)**2 < data:
        s += 1
    w = (2*s+1)  # width and height of the square
    m = w**2  # bottom right number in the square (largest) at position (s,s)

    # calc positions in terms of s
    diff = m - data
    div, mod = divmod(diff, (w-1))
    if div == 0:  # S edge
        x = s - mod
        y = s
    elif div == 1:  # W edge
        x = -s
        y = s - mod
    elif div == 2:  # N edge
        x = s - mod
        y = -s
    elif div == 3:  # E edge
        x = s
        y = s - mod
    else:
        raise ValueError("error :(")

    res = abs(x) + abs(y)
    return res


def neighborhood_spiral(data: int) -> int:
    y = x = 0
    grid: defaultdict[Pos, int] = defaultdict(int, {(0, 0): 1})

    for s in range(1, 10**6):
        w = (2*s+1)  # width and height of the square

        # east edge
        x += 1  # step right into next bigger square onto its east edge
        for _ in range(w-1):
            val = sum(grid[y+dy, x+dx] for dy, dx in ((1, 0), (-1, 0), (0, -1), (1, -1), (-1, -1)))
            if val > data:
                return val
            grid[y, x] = val
            y -= 1
        y += 1  # fix for post increment

        # north edge
        for _ in range(w-1):
            x -= 1
            val = sum(grid[y+dy, x+dx] for dy, dx in ((0, 1), (0, -1), (1, 0), (1, -1), (1, 1)))
            if val > data:
                return val
            grid[y, x] = val

        # west edge
        for _ in range(w-1):
            y += 1
            val = sum(grid[y+dy, x+dx] for dy, dx in ((1, 0), (-1, 0), (0, 1), (1, 1), (-1, 1)))
            if val > data:
                return val
            grid[y, x] = val

        # south edge
        for _ in range(w-1):
            x += 1
            val = sum(grid[y+dy, x+dx] for dy, dx in ((0, 1), (0, -1), (-1, 0), (-1, -1), (-1, 1)))
            if val > data:
                return val
            grid[y, x] = val

    else:
        raise ValueError("Max iterations reached.")


@timed("All")
def main() -> None:
    DATA = 368078

    p1 = steps(DATA)
    print("Part 1:", p1)

    p2 = neighborhood_spiral(DATA)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
