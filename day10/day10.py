import os.path
import os
import sys
from itertools import batched
from functools import reduce
from operator import xor

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa


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


def knot_hash(data: str) -> str:
    lengths = [ord(c) for c in data] + [17, 31, 73, 47, 23]
    marks = knotting(lengths, 64)

    dense_hash = [reduce(xor, batch) for batch in batched(marks, 16)]
    hex_string = "".join(f"{num:02x}" for num in dense_hash)

    return hex_string


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    lengths = list(map(int, data.split(",")))
    knotted = knotting(lengths)
    p1 = knotted[0]*knotted[1]
    print("Part 1:", p1)

    p2 = knot_hash(data)
    print("Part 1:", p2)


if __name__ == "__main__":
    main()
