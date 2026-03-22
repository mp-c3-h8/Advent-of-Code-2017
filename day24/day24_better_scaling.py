import os.path
import os
import sys
from collections import deque, defaultdict, Counter

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa

type Port = int
type Component = tuple[Port, Port]


def create_components(data: str) -> list[Component]:
    components = []
    for line in data.splitlines():
        p1, p2 = map(int, line.split("/"))
        components.append((p1, p2))
    return components


type Bridge = Counter[Component]
type Item = tuple[int, int, Port, Bridge, frozenset[Port]]
type BridgeState = frozenset[tuple[Port, Port, int]]
type State = tuple[Port, BridgeState, frozenset[Port]]  # (port,bridge,ext_used)


def strongest_bridge(components: list[Component]) -> tuple[int, int]:
    port_to_component: defaultdict[int, set[Component]] = defaultdict(set)
    component_count: Counter[Component] = Counter()
    extensions: Counter[Port] = Counter()
    for p1, p2 in components:
        if p1 == p2:
            extensions[p1] += 1
            continue
        if p1 > p2:
            low, high = p1, p2
        else:
            low, high = p2, p1

        comp = (low, high)

        port_to_component[low].add(comp)
        port_to_component[high].add(comp)
        component_count[comp] += 1

    # bridge doesnt include extensions
    # use (0,0) extensions
    ext_init = frozenset({0})
    length_init = extensions[0]
    init: Item = (0, length_init, 0, Counter(), ext_init)  # (strength,length,port,bridge,ext_used)
    q: deque[Item] = deque([init])
    best_strength: int = 0
    best_length: int = 0
    best_length_strength: int = 0

    seen: set[State] = set()

    while q:
        strength, length, port, bridge, ext_used = q.popleft()

        new_components = []
        for comp in port_to_component[port]:
            if comp in bridge and bridge[comp] == component_count[comp]:
                continue
            new_components.append(comp)
        n = len(new_components)

        if n == 0:
            best_strength = max(best_strength, strength)
            if length > best_length:
                best_length = length
                best_length_strength = strength
            elif length == best_length:
                best_length_strength = max(best_length_strength, strength)
            continue

        for new_comp in new_components:
            p1, p2 = new_comp
            new_strength = strength + p1 + p2
            new_length = length + 1
            new_port = p1 if port == p2 else p2
            new_bridge = bridge.copy()
            new_bridge[new_comp] += 1
            new_ext_used = ext_used

            # connect extensions immediately
            if new_port in extensions and new_port not in ext_used:
                num_extensions = extensions[new_port]
                new_length += num_extensions
                new_strength += num_extensions * 2 * new_port
                new_ext_used |= {new_port}

            bridge_state = frozenset((p1, p2, c) for (p1, p2), c in new_bridge.items())
            new_state = (new_port, bridge_state, new_ext_used)
            if new_state in seen:
                continue
            seen.add(new_state)

            new_item = (new_strength, new_length, new_port, new_bridge, new_ext_used)
            q.append(new_item)

    return best_strength, best_length_strength


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    components = create_components(data)
    p1, p2 = strongest_bridge(components)
    print("Part 1:", p1)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
