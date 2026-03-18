import os.path
import os
import sys
from collections import deque

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa


def spinlock(steps: int) -> int:
    buffer = deque([0])
    for i in range(1, 2017 + 1):
        rot = (steps+1) % i  # i == len(buffer)
        buffer.rotate(-rot)
        buffer.appendleft(i)
    buffer.rotate(-1)
    res = buffer.popleft()
    return res


def spinlock2(steps: int) -> int:
    res = 0
    pos = 0
    for i in range(1, 50*10**6+1):
        # only monitor value after 0
        pos = (pos+steps) % i + 1
        if pos == 1:
            res = i
    return res


@timed("All")
def main() -> None:

    STEPS = 394

    p1 = spinlock(STEPS)
    print("Part 1:", p1)

    p2 = spinlock2(STEPS)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
