import os.path
import os
import sys
from collections import defaultdict

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa


type Action = tuple[int, int, int]  # (write,move,next_state)
type State = tuple[Action, Action]  # index in list serves as id


def create_states(data: str) -> tuple[list[State], int, int]:
    states = []
    init, *states_str = data.split("\n\n")
    line1, line2 = init.splitlines()
    state_start = ord(line1[-2:-1]) - 65  # A = 65
    steps = int(line2.split(" ")[-2])

    for state_str in states_str:
        split = state_str.splitlines()
        actions = []
        for i in range(2):
            offset = 1 + i*4
            write = int(split[offset+1][-2:-1])
            move = 1 if split[offset+2].split()[-1] == "right." else -1
            next_state = ord(split[offset+3][-2:-1]) - 65  # A = 65
            action = (write, move, next_state)
            actions.append(action)
        state = (actions[0], actions[1])
        states.append(state)
    return states, state_start, steps


def turing(states: list[State], state_start: int, steps: int) -> int:
    tape: defaultdict[int, int] = defaultdict(int)
    curr_state: int = state_start
    curr_tape: int = 0

    for _ in range(steps):
        curr_val = tape[curr_tape]
        write, move, next_state = states[curr_state][curr_val]
        tape[curr_tape] = write
        curr_tape += move
        curr_state = next_state

    p1 = sum(tape.values())
    return p1


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    states, state_start, steps = create_states(data)
    p1 = turing(states, state_start, steps)
    print("Part 1:", p1)


if __name__ == "__main__":
    main()
