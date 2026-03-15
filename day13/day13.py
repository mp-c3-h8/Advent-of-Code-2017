import os.path
import os
import sys
import re
from math import prod, gcd

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa

type Depth = int
type Range = int
type Layer = tuple[Depth, Range]
type Firewall = list[Layer]


def create_firewall(data: str) -> Firewall:
    firewall = []
    regexp = re.compile(r"-?\d+")
    for line in data.splitlines():
        depth, rang = map(int, regexp.findall(line))
        firewall.append((depth, rang))
    return firewall


def severity(firewall: Firewall) -> int:
    res = 0
    for depth, rang in firewall:
        if depth % (2*(rang-1)) == 0:
            res += depth*rang
    return res


def min_delay(firewall: Firewall) -> int:
    conds: dict[int, set[int]] = {}

    for depth, rang in firewall:
        mult = 2*(rang-1)
        skip = (-depth % mult)
        mods = set(j for j in range(mult) if j != skip)
        if mult in conds:
            conds[mult] = conds[mult].intersection(mods)
        else:
            conds[mult] = mods

    # simplify
    conds = {key: conds[key] for key in sorted(conds, reverse=True)}
    coprimes, rems = [], []
    for mult, mods in conds.items():
        for other_mult in conds:
            if mult > other_mult and mult % other_mult == 0:
                mods.difference_update(m for m in mods.copy() if m % other_mult not in conds[other_mult])

        # check if CRT is applicable
        # mult is always even -> divide by 2
        if len(mods) == 1:
            n = mult // 2
            if any(gcd(n, c) != 1 for c in coprimes):  # coprime check
                continue
            m, = mods  # hacky unpacking
            if m % 2 == 1:
                continue
            coprimes.append(n)
            rems.append(m//2)

    # apply CRT
    # bruteforce with stepsize of delay_mult
    # defaults to delay=0, delay_mult=1 if CRT fails
    delay = 2*find_min_x(coprimes, rems)  # times 2, cuz we divided by 2 earlier
    delay_mult = prod(coprimes)
    for _ in range(10**6):
        if all((depth+delay) % (2*rang-2) != 0 for depth, rang in firewall):
            break
        delay += delay_mult
    else:
        raise ValueError("Max iterations reached.")

    return delay


# https://www.geeksforgeeks.org/dsa/chinese-remainder-theorem-in-python/
def gcd_extended(a: int, b: int) -> tuple[int, int, int]:
    if a == 0:
        return (b, 0, 1)
    gcd, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return (gcd, x, y)


# https://www.geeksforgeeks.org/dsa/chinese-remainder-theorem-in-python/
def find_min_x(nums: list[int], rems: list[int]) -> int:
    N = prod(nums)
    result = 0
    for i in range(len(nums)):
        N_i = N // nums[i]
        _, inv_i, _ = gcd_extended(N_i, nums[i])
        result += rems[i] * N_i * inv_i

    return result % N


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    firewall = create_firewall(data)
    p1 = severity(firewall)
    print("Part 1:", p1)

    p2 = min_delay(firewall)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
