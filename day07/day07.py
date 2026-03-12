import os.path
import os
import sys
from collections import defaultdict, Counter

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa


class Node:
    def __init__(self, name: str, weight: int) -> None:
        self.name: str = name
        self.weight: int = weight
        self.childs: list[Node] = []
        self.sum: int = 0  # own weight + sum of childs weights
        self.childs_are_balanced: bool = True


def calc_sum(node: Node) -> int:
    node.sum = node.weight
    if len(node.childs) > 0:
        seen: set[int] = set()
        for child in node.childs:
            child_sum = calc_sum(child)
            node.sum += child_sum
            seen.add(child_sum)
        node.childs_are_balanced = len(seen) < 2
    return node.sum


def find_unbalanced(node: Node) -> int | None:
    unbalanced_childs: list[Node] = [child for child in node.childs if not child.childs_are_balanced]
    if len(unbalanced_childs) == 0:
        # one of the direct childs is the baddy
        sum_to_childs: defaultdict[int, list] = defaultdict(list)
        for child in node.childs:
            sum_to_childs[child.sum].append(child)
        assert len(sum_to_childs) == 2  # otherwise undetermined
        target = next(chield_sum for chield_sum, childs in sum_to_childs.items() if len(childs) > 1)
        baddy = next(child for child in node.childs if child.sum != target)
        diff = baddy.sum - target
        return baddy.weight - diff

    assert len(unbalanced_childs) == 1
    return find_unbalanced(unbalanced_childs[0])


def create_tree(data: str) -> Node:
    in_degree: Counter[Node] = Counter()
    name_to_node: dict[str, Node] = {}
    for line in data.splitlines():
        split = line.split(" -> ")

        # LHS
        lhs = split[0]
        from_name, from_weight = lhs.split(" ")
        if from_name in name_to_node:
            from_node = name_to_node[from_name]
            from_node.weight = int(from_weight[1:-1])
        else:
            from_node = Node(from_name, int(from_weight[1:-1]))
            name_to_node[from_name] = from_node
        in_degree[from_node] += 0  # hacky: add the key

        # RHS
        if len(split) == 2:
            rhs = split[1]
            for to_name in rhs.split(", "):
                if to_name in name_to_node:
                    to_node = name_to_node[to_name]
                else:
                    to_node = Node(to_name, -1)
                    name_to_node[to_name] = to_node
                from_node.childs.append(to_node)
                in_degree[to_node] += 1
    # find root
    roots = [node for node, count in in_degree.items() if count == 0]
    assert len(roots) == 1, "Invalid input"
    return roots[0]


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    root = create_tree(data)
    print("Part 1:", root.name)

    calc_sum(root)
    p2 = find_unbalanced(root)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
