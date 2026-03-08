import os.path
import os
import sys
from itertools import pairwise

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    digits = [int(c) for c in data]
    captcha = sum(d1 for d1, d2 in pairwise(digits) if d1 == d2)
    captcha += digits[-1] if digits[0] == digits[-1] else 0
    print("Part 1:", captcha)

    n = len(digits)
    captcha2 = sum(digits[i] for i in range(n) if digits[i] == digits[(i+n//2) % n])
    print("Part 2:", captcha2)


if __name__ == "__main__":
    main()
