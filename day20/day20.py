import os.path
import os
import sys
import re
from math import isqrt
from itertools import combinations
from collections import defaultdict

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa


type Vec3 = tuple[int, int, int]  # (x,y,z)
type Pos = Vec3
type Vel = Vec3
type Acc = Vec3
type Particle = tuple[Pos, Vel, Acc]


def create_particles(data: str) -> list[Particle]:
    regexp = re.compile(r"-?\d+")
    particles = []
    for line in data.splitlines():
        px, py, pz, vx, vy, vz, ax, ay, az = map(int, regexp.findall(line))
        particle = ((px, py, pz), (vx, vy, vz), (ax, ay, az))
        particles.append(particle)
    return particles


def man(x: Vec3) -> int:
    return abs(x[0]) + abs(x[1]) + abs(x[2])


# t > 0  =  tick
# a = a_0 = const
# p_t = a * t^2/2 + t * (a/2+v_0) + p_0
# p_t gets dominated by:
#  1.  a
#  2.  a/2 + v_0
#  3.  p_0
def cmp(par: Particle) -> tuple[float, float, float]:
    man_p, man_v, man_a = map(man, par)
    return (man_a, man_a/2+man_v, man_p)


def long_run(particles: list[Particle]) -> int:
    n = len(particles)
    idx = min(range(n), key=lambda i: cmp(particles[i]))
    return idx


# inputs are scalar!
# we only allow positive integer solutions
def solve_for_t(dp: int, dv: int, da: int) -> list[int] | None:
    # abc formula
    a = da
    b = da + 2*dv
    c = 2*dp

    if a == b == 0:
        if c == 0:
            # da = dv = dp = 0   =>  identical
            # collision for every t
            return []
        else:
            # c != 0   =>  no solution
            return None

    if a == 0:
        # b*x + c = 0
        # b!=0
        if -c % b != 0:
            return None
        sol = -c//b
        if sol < 0:
            return None
        return [sol]

    radical = b*b - 4*a*c

    # negative radical
    if radical < 0:
        return None

    # isqrt is used here
    sq = isqrt(radical)

    if sq*sq != radical:
        return None

    sols: list[int] = []
    for pari in (1, -1):
        nom = -b + pari*sq
        den = 2*a
        if nom % den != 0:
            continue

        sol = nom//den
        if sol < 0:
            continue

        sols.append(sol)

    sols.sort()
    return sols


def particle_pos_at_tick(par: Particle, t: int) -> Pos:
    p, v, a = par
    return tuple(p[i] + t*v[i] + t*(t+1)//2 * a[i] for i in range(3))  # type: ignore


def collisions(particles: list[Particle]) -> int:

    colls: defaultdict[int, set[Particle]] = defaultdict(set)

    for par1, par2 in combinations(particles, 2):
        p1, v1, a1 = par1
        p2, v2, a2 = par2
        dp = (p1[0]-p2[0], p1[1]-p2[1], p1[2]-p2[2])
        dv = (v1[0]-v2[0], v1[1]-v2[1], v1[2]-v2[2])
        da = (a1[0]-a2[0], a1[1]-a2[1], a1[2]-a2[2])

        for i in range(3):
            found = False
            sols = solve_for_t(dp[i], dv[i], da[i])
            if sols is None:
                break
            elif len(sols) == 0:  # solution exists for every t
                continue
            else:
                for t in sols:
                    if particle_pos_at_tick(par1, t) == particle_pos_at_tick(par2, t):
                        colls[t].update((par1, par2))
                        found = True
                        break
            if found:
                break

    colliders_list: list[set[Particle]] = [colls[k] for k in sorted(colls.keys())]
    seen: set[Particle] = set()
    num_coll = 0

    for colliders in colliders_list:
        diff = colliders.difference(seen)
        num_coll += len(diff)
        seen.update(diff)

    p2 = len(particles) - num_coll
    return p2


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    particles = create_particles(data)
    p1 = long_run(particles)
    print("Part 1:", p1)

    p2 = collisions(particles)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
