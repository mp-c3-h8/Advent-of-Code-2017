import os.path
import os
import sys
from itertools import batched
from functools import reduce
from operator import xor
from collections import deque

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa

type Pos = tuple[int, int]  # (y,x) y downwards
type Grid = set[Pos]


def knotting(lengths: list[int], rounds: int = 1) -> list[int]:
    SIZE = 256
    marks = list(range(SIZE))
    sum_rotated = 0
    skip = 0
    # current position will always be index 0 of marks
    for _ in range(rounds):
        for l in lengths:
            if l > 0:
                # marks[l-1::-1] == marks[:l][::-1]
                marks = marks[l:] + marks[l-1::-1]  # implicit rotation by l
            marks = marks[skip:] + marks[:skip]  # rotate by skip
            sum_rotated += skip+l
            skip = (skip+1) % SIZE

    # reverse rotations
    rev = SIZE - (sum_rotated % SIZE)
    marks = marks[rev:] + marks[:rev]

    return marks


def create_grid(key: str) -> Grid:
    grid = set()
    row_base = [ord(c) for c in f"{key}-"]
    for y in range(128):
        row_suffix = [ord(c) for c in str(y)]
        lengths = row_base + row_suffix + [17, 31, 73, 47, 23]
        marks = knotting(lengths, 64)
        dense_hash = [reduce(xor, batch) for batch in batched(marks, 16)]
        for i, num in enumerate(dense_hash):
            div, mod = divmod(num, 16)
            binary_block = f"{div:04b}" + f"{mod:04b}"
            for k, c in enumerate(binary_block):
                if c == "1":
                    x = i*8+k
                    grid.add((y, x))
    return grid


def connected_region_for_pos(grid: Grid, pos: Pos) -> set[Pos]:
    DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    q: deque[Pos] = deque([pos])
    connected: set[Pos] = {pos}
    while q:
        curr = q.popleft()
        for d in DIRS:
            adj = (curr[0]+d[0], curr[1]+d[1])
            if adj not in grid:
                continue
            if adj in connected:
                continue
            connected.add(adj)
            q.append(adj)
    return connected


def num_connected_regions(grid: Grid) -> int:
    num = 0
    while len(grid) != 0:
        pos = grid.pop()
        region = connected_region_for_pos(grid, pos)
        grid.difference_update(region)
        num += 1
    return num


@timed("All")
def main() -> None:

    KEY = "xlqgujun"
    grid = create_grid(KEY)
    print("Part 1:", len(grid))

    p2 = num_connected_regions(grid)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
