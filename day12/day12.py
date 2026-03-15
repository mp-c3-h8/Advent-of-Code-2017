import os.path
import os
import sys
from collections import deque

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa

type Node = int
type Graph = dict[Node, list[Node]]


def create_graph(data: str) -> Graph:
    graph = {}
    for line in data.splitlines():
        lhs, rhs = line.split(" <-> ")
        node_from = int(lhs)
        graph[node_from] = list(map(int, rhs.split(", ")))
    return graph


def connected_subgraph_for_node(graph: Graph, node: Node) -> set[Node]:
    q: deque[Node] = deque([node])
    connected: set[Node] = {node}
    while q:
        curr_node = q.popleft()
        for adj in graph[curr_node]:
            if adj in connected:
                continue
            connected.add(adj)
            q.append(adj)
    return connected


def num_connected_subgraphs(graph: Graph) -> int:
    num = 0
    all_nodes = set(graph)
    while len(all_nodes) != 0:
        curr = all_nodes.pop()
        subgraph = connected_subgraph_for_node(graph, curr)
        all_nodes.difference_update(subgraph)
        num += 1
    return num


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    graph = create_graph(data)
    connected_0 = connected_subgraph_for_node(graph, 0)
    print("Part 1:", len(connected_0))

    p2 = num_connected_subgraphs(graph)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
