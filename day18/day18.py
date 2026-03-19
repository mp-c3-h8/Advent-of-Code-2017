import os.path
import os
import sys
from collections import defaultdict, deque


dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, '..', 'utils'))
from utils import timed  # noqa


type OpCode = str
type Parameter = str
type Instruction = tuple[OpCode, list[Parameter]]


def parse(data: str) -> list[Instruction]:
    instr = []
    for line in data.splitlines():
        inst, *params = line.split(" ")
        instr.append((inst, params))
    return instr


class Program:
    def __init__(self, instr: list[Instruction], p: int) -> None:
        self.registers: defaultdict[str, int] = defaultdict(int, {"p": p})
        self.instructions: list[Instruction] = instr
        self.pt: int = 0
        self.output: list[int] = []
        self.input: deque[int] = deque([])

    def get_value(self, param: Parameter) -> int:
        return self.registers[param] if param.isalpha() else int(param)

    def run(self) -> None:
        n = len(self.instructions)
        for _ in range(10**6):
            if self.pt < 0 or self.pt >= n:
                break
            op, params = self.instructions[self.pt]
            if op == "snd":
                self.output.append(self.registers[params[0]])
            elif op == "set":
                self.registers[params[0]] = self.get_value(params[1])
            elif op == "add":
                self.registers[params[0]] += self.get_value(params[1])
            elif op == "mul":
                self.registers[params[0]] *= self.get_value(params[1])
            elif op == "mod":
                self.registers[params[0]] %= self.get_value(params[1])
            elif op == "rcv":
                if len(self.input) == 0:
                    break
                self.registers[params[0]] = self.input.popleft()
            elif op == "jgz":
                x, y = self.get_value(params[0]), self.get_value(params[1])
                if x > 0:
                    self.pt += y
                    self.pt -= 1  # negate increment
            else:
                raise ValueError(f"Opcode {op} unknown")
            self.pt += 1
        else:
            raise ValueError("Max iterations reached.")


def part1(instr: list[Instruction]) -> int:
    prog = Program(instr, 0)
    prog.run()
    return prog.output.pop()


def part2(instr: list[Instruction]) -> int:
    prog_0 = Program(instr, 0)
    prog_1 = Program(instr, 1)
    res = 0

    for _ in range(10**6):
        prog_0.run()
        prog_1.run()

        if len(prog_0.output) == 0 and len(prog_1.output) == 0:
            return res

        res += len(prog_1.output)
        prog_0.input.extend(prog_1.output)
        prog_1.input.extend(prog_0.output)
        prog_0.output = []
        prog_1.output = []
    else:
        raise ValueError("Max iterations reached.")


@timed("All")
def main() -> None:
    input_path = os.path.join(dir_path, "input.txt")
    with open(input_path) as f:
        data = f.read()

    instr = parse(data)
    p1 = part1(instr)
    print("Part 1:", p1)

    p2 = part2(instr)
    print("Part 2:", p2)


if __name__ == "__main__":
    main()
