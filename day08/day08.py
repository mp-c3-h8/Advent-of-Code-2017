import os.path
import os
import sys
from collections import defaultdict
from operator import lt, gt, le, ge, eq, ne
from typing import Callable

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa

CONDS: dict[str, Callable[[int, int], bool]] = {
    "<": lt, ">": gt,
    "<=": le, ">=": ge,
    "==": eq, "!=": ne
}


def run_program(data: str) -> tuple[int, int]:
    global CONDS
    registers: defaultdict[str, int] = defaultdict(int)
    p2 = 0

    for line in data.splitlines():
        reg, op, amount, _, c1, cond, c2 = line.split(" ")
        c1 = registers[c1] if c1.isalpha() else int(c1)
        c2 = registers[c2] if c2.isalpha() else int(c2)
        if CONDS[cond](c1, c2):
            registers[reg] += int(amount) if op == "inc" else -int(amount)
            p2 = max(p2, registers[reg])

    p1 = max(registers.values())
    return p1, p2


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    p1, p2 = run_program(data)
    print("Part 1:", p1)
    print("Part 1:", p2)


if __name__ == "__main__":
    main()
