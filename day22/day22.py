import os.path
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa


type Pos = complex  # x+1j*y  ,  y downwards
type Grid = dict[Pos, int]


def create_grid(data: str) -> tuple[Grid, Pos]:
    split = data.splitlines()
    start = len(split[0])//2 + 1j * (len(split)//2)
    grid = {x+1j*y: 1 for y, line in enumerate(split) for x, c in enumerate(line) if c == "#"}
    return grid, start


def infection(grid: Grid, start: Pos, bursts: int) -> int:
    pos = start
    d = -1j  # facing up
    p1 = 0

    for _ in range(bursts):
        if pos in grid:
            d *= 1j
            del grid[pos]
        else:
            p1 += 1
            d *= -1j
            grid[pos] = 1
        pos += d

    return p1


# not in grid = clean
# 0 = weakened
# 1 = infected
# 2 = flagged
def evolution(grid: Grid, start: Pos, bursts: int) -> int:
    pos = start
    d = -1j  # facing up
    p2 = 0

    for _ in range(bursts):
        if pos in grid:
            status = grid[pos]
            if status == 0:  # weakened
                p2 += 1
                grid[pos] = 1
            elif status == 1:  # infected
                d *= 1j
                grid[pos] = 2
            elif status == 2:  # flagged
                d *= -1
                del grid[pos]
        else:  # clean
            d *= -1j
            grid[pos] = 0
        pos += d

    return p2


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    grid, start = create_grid(data)
    p1 = infection(grid.copy(), start, 10_000)
    print("Part 1:", p1)

    p2 = evolution(grid, start, 10_000_000)
    print("Part 1:", p2)


if __name__ == "__main__":
    main()
