import os.path
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa


def total_score(data: str) -> tuple[int, int]:
    depth = score = garbage_count = 0
    stream = iter(data)

    for curr in stream:
        if curr == "{":
            depth += 1
        elif curr == "}":
            score += depth
            depth -= 1
        elif curr == "<":
            while (curr := next(stream)) != ">":
                if curr == "!":
                    next(stream)
                    continue
                garbage_count += 1
        elif curr == ",":
            continue
        else:
            raise ValueError("Stream of characters malformed.")

    assert depth == 0
    return score, garbage_count


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    score, garbage_count = total_score(data)
    print("Part 1:", score)
    print("Part 2:", garbage_count)


if __name__ == "__main__":
    main()
