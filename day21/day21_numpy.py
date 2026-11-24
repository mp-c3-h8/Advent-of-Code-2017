import os.path
import os
import sys
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa

type Key = bytes
type Image = np.ndarray
type Rules = dict[Key, Image]


def create_rules(data: str) -> Rules:
    rules: Rules = {}
    for line in data.splitlines():
        source, target = line.split(" => ", 2)

        source = source.replace("/", "")
        target = target.replace("/", "")

        source = np.array([1 if c == "#" else 0 for c in source], dtype=np.int8)
        target = np.array([1 if c == "#" else 0 for c in target], dtype=np.int8)

        if len(source) == 4:
            # 2x2
            source = source.reshape((2, 2))
            target = target.reshape((3, 3))
        elif len(source) == 9:
            # 3x3
            source = source.reshape((3, 3))
            target = target.reshape((4, 4))
        else:
            raise ValueError("Wrong dimension.")

        # flip
        flipped = np.flipud(source)

        # rotate four times by 90°
        for _ in range(4):
            rules[source.tobytes()] = target
            rules[flipped.tobytes()] = target

            source = np.rot90(source)
            flipped = np.rot90(flipped)

    # number of rules should be 2^4 + 2^9 = 528
    assert len(rules) == 528

    return rules


def enhance(source: Image, rules: Rules) -> Image:
    size = len(source)
    if size <= 3:
        return rules[source.tobytes()]

    m = 2 if size % 2 == 0 else 3  # 2x2 or 3x3 blocks to replace
    n = m+1  # new blocks are larger by 1
    div = size // m

    new_image = np.zeros((div*n, div*n), dtype=np.int8)
    for i in range(div):
        for j in range(div):
            block = source[m*i:m*i+m, m*j:m*j+m]
            new_block = rules[block.tobytes()]
            new_image[n*i:n*i+n, n*j:n*j+n] = new_block

    return new_image


def count_on(image: Image) -> int:
    res = int(np.sum(image))
    return res


# improvements:
# - 3x3 turns into 3x3 of 3x3's after 3 iterations ( 9x9 matrix )
# - iterate them independently
# - use indices for every 2x2 and 3x3 and dont work with grids

@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    RULES = create_rules(data)
    P1_ITER = 5
    P2_ITER = 18

    image = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]], dtype=np.int8)

    for _ in range(P1_ITER):
        image = enhance(image, RULES)
    p1 = count_on(image)
    print("Part 1:", p1)

    for _ in range(P2_ITER - P1_ITER):
        image = enhance(image, RULES)
    p2 = count_on(image)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
