import os.path
import os
import sys
import re
from math import prod, gcd
from itertools import combinations

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
    # create dict of rules our solution x must satisfy
    # x % div in mods   for every key-value-pair (div,mods)
    div_to_mods: dict[int, set[int]] = {}
    for depth, rang in firewall:
        div = 2*(rang-1)
        index_0 = (-depth % div)
        mods = set(j for j in range(div) if j != index_0)
        if div in div_to_mods:
            # suppose we have
            # x % 3 in {0,1}   and   x % 3 in {1,2}
            # to satisfy both   x % 3 in {1}   must hold
            div_to_mods[div].intersection_update(mods)
        else:
            div_to_mods[div] = mods

    # simplify
    sorted_by_div: list[tuple[int, set[int]]] = sorted(div_to_mods.items())
    n = len(sorted_by_div)
    coprimes, rems = [], []

    for i, (div, mods) in enumerate(sorted_by_div):
        for j in range(i):
            other_div, other_mods = sorted_by_div[j]
            # div > other_div by construction
            if div % other_div == 0:
                # mods and other_mods reference same sets in div_to_mods
                mods.difference_update(m for m in mods.copy() if m % other_div not in other_mods)

            # check if CRT is applicable
            # div is always even -> divide by 2
            if len(mods) == 1:
                d = div // 2
                if any(gcd(d, c) != 1 for c in coprimes):  # coprime check
                    continue
                m, = mods  # hacky unpacking
                if m % 2 == 1:
                    continue
                coprimes.append(d)
                rems.append(m//2)

                del div_to_mods[div]

    print(div_to_mods)
    print(sorted_by_div)
    print(coprimes)

    # apply CRT
    # bruteforce with stepsize of delay_mult
    # defaults to delay=0, delay_mult=1 if CRT fails
    delay = 2*find_min_x(coprimes, rems)  # times 2, cuz we divided by 2 earlier
    delay_mult = prod(coprimes)
    for _ in range(10**6):
        if all(delay % mult in mods for mult, mods in div_to_mods.items()):
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
