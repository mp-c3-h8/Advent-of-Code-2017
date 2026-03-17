import os.path
import os
import sys
from typing import Iterator

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa


def gen(val: int, mult: int, picky: int = 1) -> Iterator[int]:
    MOD = 2147483647
    while True:
        val *= mult
        val %= MOD
        if val % picky == 0:
            yield val


def jugde(data: str, max_iter: int, pickyA: int = 1, pickyB: int = 1) -> int:
    MULT_A = 16807
    MULT_B = 48271
    MASK = (1 << 16) - 1
    lineA, lineB = data.splitlines()
    initA = int(lineA.split(" ")[-1])
    initB = int(lineB.split(" ")[-1])

    genA = gen(initA, MULT_A, pickyA)
    genB = gen(initB, MULT_B, pickyB)

    res = 0
    for _ in range(max_iter):
        if (next(genA) & MASK) == (next(genB) & MASK):
            res += 1

    return res


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    p1 = jugde(data, 40*10**6)
    print("Part 1:", p1)

    p2 = jugde(data, 5*10**6, 4, 8)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
