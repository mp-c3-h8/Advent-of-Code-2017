import os.path
import os
import sys
from typing import Any

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa

type Move = tuple[int, tuple[Any, ...]]  # 0=spin, 1=exchange, 2=partner
type Programs = list[str]


def create_moves(data: str) -> list[Move]:
    moves = []
    for move in data.split(","):
        if move.startswith("s"):
            x = int(move[1:])
            moves.append((0, (x,)))
        elif move.startswith("x"):
            left, right = move.split("/")
            a, b = int(left[1:]), int(right)
            moves.append((1, (a, b)))
        elif move.startswith("p"):
            name_a, name_b = move[1], move[3]
            moves.append((2, (name_a, name_b)))
        else:
            raise ValueError(f"Unknown move {move}")
    return moves


def dance(programs: Programs, moves: list[Move]) -> Programs:
    for code, params in moves:
        if code == 0:
            x = params[0]
            programs = programs[-x:] + programs[:-x]
        elif code == 1:
            a, b = params[0], params[1]
            programs[a], programs[b] = programs[b], programs[a]
        elif code == 2:
            name_a, name_b = params[0], params[1]
            a, b = programs.index(name_a), programs.index(name_b)
            programs[a], programs[b] = programs[b], programs[a]
        else:
            raise ValueError(f"Unknown code {code}")
    return programs


def dance_once(programs: Programs, moves: list[Move]) -> str:
    programs = dance(programs, moves)
    return "".join(programs)


def dance_a_lot(programs: Programs, moves: list[Move]) -> str:
    NUM_DANCES = 1_000_000_000
    seen: dict[str, int] = {}
    orders: list[str] = []

    # try to find a period
    for i in range(10**6):
        order = "".join(programs)
        if order in seen:
            break
        seen[order] = i
        orders.append(order)
        programs = dance(programs, moves)
    else:
        raise ValueError("No period found.")

    period = i - seen[order]
    dances_left = NUM_DANCES - i
    dances_left %= period

    # must have been seen already
    res = orders[dances_left]

    return res


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    SIZE = 16
    programs: Programs = [chr(97 + i) for i in range(SIZE)]  # 97 = a
    moves = create_moves(data)

    p1 = dance_once(programs[::], moves)
    print("Part 1:", p1)

    p2 = dance_a_lot(programs, moves)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
