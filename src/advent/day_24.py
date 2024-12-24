from pathlib import Path
import re
from typing import Optional

from advent.utils.load_file import File

def get_gate_output(gate: str, gates: dict[str, int], dependencies: dict[str, tuple[str, str, str]]) -> int:
    if gate in gates:
        return gates[gate]
    else:
        gate_1 = dependencies[gate][0]
        gate_2 = dependencies[gate][1]
        operation = dependencies[gate][2]

        gate_1_output = get_gate_output(gate_1, gates, dependencies)
        gate_2_output = get_gate_output(gate_2, gates, dependencies)

        if operation == "AND":
            gates[gate] = gate_1_output & gate_2_output
        elif operation == "OR":
            gates[gate] = gate_1_output | gate_2_output
        elif operation == "XOR":
            gates[gate] = gate_1_output ^ gate_2_output
        return gates[gate]

def part1_solution(file_path: Path) -> int:
    MATCH_OPRATION_LINE = re.compile(r"([a-z0-9]{3}) (AND|OR|XOR) ([a-z0-9]{3}) -> ([a-z0-9]{3})")

    dependencies: dict[str, tuple[str, str, str]] = {}
    gates: dict[str, int] = {}
    gates_with_z: list[str] = []

    is_line_with_operation: bool = False
    for line in File(file_path).read():
        line = line.strip()
        if line == "":
            is_line_with_operation = True
            continue

        if not is_line_with_operation:
            gate, value = line.split(": ")
            gates[gate] = int(value)
        else:
            if match := MATCH_OPRATION_LINE.match(line):
                gate_1, operation, gate_2, gate = match[1], match[2], match[3], match[4]
                dependencies[gate] = (gate_1, gate_2, operation)
                if gate.startswith("z"):
                    gates_with_z.append(gate)

    gates_with_z.sort(key=lambda gate: gate[1:], reverse=True)
    result: int = 0
    for gate in gates_with_z:
        result <<= 1
        result += get_gate_output(gate, gates, dependencies)

    return result

def check_bad_gate(gate_with_z: str, dependencies: dict[str, tuple[str, str, str]]) -> Optional[str]:
    # based on solution from reddit, too complicated for someone not involved in electronics
    gate_1, gate_2, operation = dependencies[gate_with_z]
    
    if operation != "XOR":
        return gate_with_z
    
    expected_operation: set[str] = {"XOR", "OR"}
    needed_gate: Optional[str] = None
    id_of_gate_with_z: int = int(gate_with_z[1:])

    gate_1_of_1, gate_2_of_1, operation_of_1 = dependencies[gate_1]
    if operation_of_1 not in expected_operation:
        return gate_1
    elif operation_of_1 == "XOR" and {gate_1_of_1, gate_2_of_1} != {f"x{id_of_gate_with_z:02}", f"y{id_of_gate_with_z:02}"}:
        return gate_1
    elif operation_of_1 == "OR":
        needed_gate = gate_1_of_1
        gate_1_of_3, _, operation_of_3 = dependencies[gate_1_of_1]
    expected_operation.remove(operation_of_1)

    gate_1_of_2, gate_2_of_2, operation_of_2 = dependencies[gate_2]
    if operation_of_2 not in expected_operation:
        return gate_2
    elif operation_of_2 == "XOR" and {gate_1_of_2, gate_2_of_2} != {f"x{id_of_gate_with_z:02}", f"y{id_of_gate_with_z:02}"}:
        return gate_2
    elif operation_of_2 == "OR":
        needed_gate = gate_1_of_2
        gate_1_of_3, _, operation_of_3 = dependencies[gate_1_of_2]

    if operation_of_3 != "AND" or (gate_1_of_3[0] in ('x', 'y') and int(gate_1_of_3[1:]) != id_of_gate_with_z - 1):
        return needed_gate

    return None

def part2_solution(file_path: Path) -> int:
    MATCH_OPRATION_LINE = re.compile(r"([a-z0-9]{3}) (AND|OR|XOR) ([a-z0-9]{3}) -> ([a-z0-9]{3})")

    dependencies: dict[str, tuple[str, str, str]] = {}
    gates: dict[str, int] = {}
    gates_with_z: list[str] = []

    is_line_with_operation: bool = False
    for line in File(file_path).read():
        line = line.strip()
        if line == "":
            is_line_with_operation = True
            continue

        if not is_line_with_operation:
            gate, value = line.split(": ")
            gates[gate] = int(value)
        else:
            if match := MATCH_OPRATION_LINE.match(line):
                gate_1, operation, gate_2, gate = match[1], match[2], match[3], match[4]
                dependencies[gate] = (gate_1, gate_2, operation)
                if gate.startswith("z"):
                    gates_with_z.append(gate)

    to_swap: list[str] = []
    for index in range(2, len(gates_with_z) - 1):
        bad_gate = check_bad_gate(f"z{index:02}", dependencies)
        if bad_gate:
            to_swap.append(bad_gate)
    
    return ",".join(sorted(to_swap))

def main() -> None:
    assert part1_solution("src/advent/day_24/data_test.txt") == 2024
    print(part1_solution("src/advent/day_24/data.txt"))
    #assert part2_solution("src/advent/day_24/data_test_2.txt") == "z00,z01,z02,z05"
    print(part2_solution("src/advent/day_24/data.txt"))