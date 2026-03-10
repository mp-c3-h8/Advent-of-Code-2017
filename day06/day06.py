import os.path
import os
import sys
import re

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa

type Banks = list[int]


# check https://en.wikipedia.org/wiki/Cycle_detection
def reallocation_routine(banks: Banks) -> tuple[int, int]:
    n = len(banks)
    seen: dict[tuple[int, ...], int] = {tuple(banks): 0}
    for i in range(1, 10**6):
        max_blocks_idx = max(range(n), key=lambda i: (banks[i], -i))
        max_blocks = banks[max_blocks_idx]
        banks[max_blocks_idx] = 0
        div, mod = divmod(max_blocks, n)

        if div > 0:
            for k in range(n):
                banks[k] += div

        if mod > 0:
            for k in range(mod):
                banks[(max_blocks_idx+k+1) % n] += 1

        state = tuple(banks)
        if state in seen:
            cycles = i-seen[state]
            break
        seen[state] = i
    else:
        raise ValueError("Max iterations reached.")

    return i, cycles


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    banks = list(map(int, re.findall(r"\d+", data)))
    p1, p2 = reallocation_routine(banks)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
