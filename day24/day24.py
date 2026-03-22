import os.path
import os
import sys
from collections import deque, defaultdict, Counter

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa

type Port = int
type Pool = defaultdict[int, set[Component]]
type Bridge = frozenset[Component]
type State = tuple[Port, Bridge, frozenset[Port]]


class Component:
    __slots__ = ["ports"]

    def __init__(self, p1: Port, p2: Port) -> None:
        self.ports: tuple[Port, Port] = (p1, p2)


def create_components(data: str) -> list[Component]:
    components = []
    for line in data.splitlines():
        p1, p2 = map(int, line.split("/"))
        component = Component(p1, p2)
        components.append(component)
    return components


def strongest_bridge(components: list[Component]) -> tuple[int, int]:
    port_to_component: defaultdict[int, set[Component]] = defaultdict(set)
    extensions: Counter[Port] = Counter()
    for comp in components:
        p1, p2 = comp.ports
        if p1 == p2:
            extensions[p1] += 1
        else:
            port_to_component[p1].add(comp)
            port_to_component[p2].add(comp)

    # State = (port,bridge,ext_used)
    # bridge doesnt include extensions
    # use (0,0) extensions
    ext_init = frozenset({0})
    length_init = extensions[0]
    state_init: State = (0, frozenset(), ext_init)
    init: tuple[int, int, State] = (0, length_init, state_init)  # (strength,length,state)
    q: deque[tuple[int, int, State]] = deque([init])
    best_strength: int = 0
    best_length: int = 0
    best_length_strength: int = 0

    seen: set[State] = set()

    while q:
        strength, length, state = q.popleft()
        port, bridge, ext_used = state

        avail = port_to_component[port].difference(bridge)
        n = len(avail)

        if n == 0:
            best_strength = max(best_strength, strength)
            if length > best_length:
                best_length = length
                best_length_strength = strength
            elif length == best_length:
                best_length_strength = max(best_length_strength, strength)
            continue

        for _ in range(n):
            comp = avail.pop()
            p1, p2 = comp.ports
            new_strength = strength + p1 + p2
            new_length = length + 1
            new_port = p1 if port == p2 else p2
            new_bridge = bridge | {comp}
            new_ext_used = ext_used

            # connect extensions immediately
            if new_port in extensions and new_port not in ext_used:
                num_extensions = extensions[new_port]
                new_length += num_extensions
                new_strength += num_extensions * 2 * new_port
                new_ext_used |= {new_port}

            new_state = (new_port, new_bridge, new_ext_used)
            if new_state in seen:
                continue
            seen.add(new_state)

            q.append((new_strength, new_length, new_state))

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
