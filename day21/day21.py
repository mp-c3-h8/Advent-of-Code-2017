import os.path
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa

type KeyRow = tuple[str, ...]
type KeyImage = tuple[KeyRow, ...]
type Row = list[str]
type Image = list[Row]
type Rules = dict[KeyImage, Image]


def create_rules(data: str) -> Rules:
    rules: Rules = {}
    for line in data.splitlines():
        source, target = line.split(" => ", 2)
        image_source = tuple(map(tuple, source.split("/")))
        image_target = list(map(list, target.split("/")))

        # flip
        flipped = tuple(image_source[::-1])

        # rotate four times by 90°
        for _ in range(4):
            rules[image_source] = image_target
            rules[flipped] = image_target

            image_source = tuple(zip(*image_source[::-1]))
            flipped = tuple(zip(*flipped[::-1]))

    # number of rules should be 2^4 + 2^9 = 528
    assert len(rules) == 528

    return rules


def enhance(source: Image, rules: Rules) -> Image:
    size = len(source)
    if size <= 3:
        return rules[tuple(tuple(row) for row in source)]

    blocks = []
    if size % 2 == 0:
        div = size // 2
        for i in range(div):
            block_row = []
            for j in range(div):
                row1 = (source[2*i][2*j], source[2*i][2*j+1])
                row2 = (source[2*i+1][2*j], source[2*i+1][2*j+1])
                lookup = (row1, row2)
                block_row.append(rules[lookup])
            blocks.append(block_row)
    else:
        div = size // 3
        for i in range(div):
            block_row = []
            for j in range(div):
                row1 = (source[3*i][3*j], source[3*i][3*j+1], source[3*i][3*j+2])
                row2 = (source[3*i+1][3*j], source[3*i+1][3*j+1], source[3*i+1][3*j+2])
                row3 = (source[3*i+2][3*j], source[3*i+2][3*j+1], source[3*i+2][3*j+2])
                lookup = (row1, row2, row3)
                block_row.append(rules[lookup])
            blocks.append(block_row)

    # reshape
    new_image = []
    for block_row in blocks:
        for row_as_lists in zip(*block_row):
            new_row = sum(row_as_lists, [])
            new_image.append(new_row)

    return new_image


def count_on(image: Image) -> int:
    res = sum(c == "#" for row in image for c in row)
    return res


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    RULES = create_rules(data)
    P1_ITER = 5
    P2_ITER = 18

    image = [list(".#."), list("..#"), list("###")]

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
