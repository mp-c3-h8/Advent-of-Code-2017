import os.path
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa


def reach_exit(offsets: list[int], part2: bool = False) -> int:
    n = len(offsets)
    pt = 0  # pointer
    for i in range(10**10):
        if pt < 0 or pt >= n:
            break
        inc = -1 if part2 and offsets[pt] >= 3 else 1
        offsets[pt] += inc
        pt += offsets[pt] - inc
    else:
        raise ValueError("Max iterations reached.")

    return i


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    offsets = [int(c) for c in data.splitlines()]

    print("Part 1:", reach_exit(offsets.copy()))
    print("Part 2:", reach_exit(offsets, True))


if __name__ == "__main__":
    main()
