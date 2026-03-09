import os.path
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa


def number_valid(data: str) -> tuple[int, int]:
    p1 = p2 = 0
    for line in data.splitlines():
        words = line.split(" ")
        p1 += len(set(words)) == len(words)
        p2 += len(set("".join(sorted(word)) for word in words)) == len(words)
    return p1, p2


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    p1, p2 = number_valid(data)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
