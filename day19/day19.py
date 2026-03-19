import os.path
import os
import sys


dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa


type Pos = complex  # x + 1j*y, y downwards
type Dir = complex
type Grid = dict[Pos, str]


def create_grid(data: str) -> tuple[Grid, Pos]:
    split = data.splitlines()
    start = split[0].index("|")
    grid = {x+1j*y: c for y, line in enumerate(split) for x, c in enumerate(line) if c != " "}
    return grid, start


def follow_path(grid: Grid, start: Pos) -> tuple[str, int]:
    pos = start
    d = 1j
    p1 = ""
    p2 = 1

    for _ in range(10**6):
        for new_d in (d, d*1j, -d*1j):
            new_pos = pos + new_d
            if new_pos in grid:
                d = new_d
                pos = new_pos
                p2 += 1
                if grid[pos].isalpha():
                    p1 += grid[pos]
                break
        else:  # cant go forward or left or right
            return p1, p2
    else:
        raise ValueError("Max iterations reached.")


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    grid, start = create_grid(data)
    p1, p2 = follow_path(grid, start)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
