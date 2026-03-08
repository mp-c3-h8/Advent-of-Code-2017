import os.path
import os
import sys
import re
from itertools import combinations

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa


def checksum(data: str) -> tuple[int, int]:
    p1 = p2 = 0
    for line in data.splitlines():
        row = [*map(int, re.findall(r"-?\d+", line))]
        row.sort(reverse=True)
        p1 += row[0] - row[-1]

        # part 2
        for d1, d2 in combinations(row, 2):
            div, mod = divmod(d1, d2)
            if mod == 0:
                p2 += div
                break
    return p1, p2


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    p1,p2 = checksum(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
