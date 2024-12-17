import copy
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import re
import sys

from utils.load_file import File

@dataclass
class Register:
    A: int
    B: int
    C: int

class Instructions(Enum):
    # Eight instructions, determined by 3 bit number
    ADV = 0 # Perform division A/2^combo_operand and it is truncated to integer and stored in A.
    BXL = 1 # Perform B & literal_operand stores in B register.
    BST = 2 # Calculate combo_operand mod 8 and it is stored in B register.
    JNZ = 3 # Does nothing if register A is 0, but if not it jumps by setting instruction pointer to literal_operand. Instruction pointer after this jump is not increased by 2
    BXC = 4 # Calculate B & C, then store in B. Take operand but ignore it.
    OUT = 5 # Calculate combo_operand mod 8 and it is printed. If program print multiple values, then they are separated by comma.
    BDV = 6 # Like adv but stroed in B register.
    CDV = 7 # Like adv but stroed in C register.

class Operand(Enum):
    # Operand after each instruction, determined by 3 bit number
    # There are literar operands which produce itself value
    # There are combo operands which produce 0-3 for 0-3 itself, 4,5,6 produce A,B,C and 7 is reserved and will not appear in valid porgram
    LITERAL_0 = 0
    LITERAL_1 = 1
    LITERAL_2 = 2
    LITERAL_3 = 3
    A = 4 # Get value of A
    B = 5 # Get value of B
    C = 6 # Get value of C
    INVALID = 7

def get_combo_operand(operand: int, registers: Register) -> int:
    match operand:
        case Operand.LITERAL_0.value:
            return 0
        case Operand.LITERAL_1.value:
            return 1
        case Operand.LITERAL_2.value:
            return 2
        case Operand.LITERAL_3.value:
            return 3
        case Operand.A.value:
            return registers.A
        case Operand.B.value:
            return registers.B
        case Operand.C.value:
            return registers.C
        case Operand.INVALID.value:
            # TODO: Add something later
            return -1

def old_solution(program_steps: list[int], registers: Register, new_value: int) -> str:
    INSTRUCTION_POINTER: int = 0
    # Increase by 2 expect jump
    # It halts if try read after code scope
    output_list: list[int] = []
    original_registers: Register = copy.deepcopy(registers)
    registers.A = new_value

    while INSTRUCTION_POINTER < len(program_steps):
        instruction: int = int(program_steps[INSTRUCTION_POINTER])
        operand: int = int(program_steps[INSTRUCTION_POINTER + 1])

        if instruction == Instructions.ADV.value:
            combo_operand: int = get_combo_operand(operand, registers)
            registers.A = registers.A // (pow(2, combo_operand))
        elif instruction == Instructions.BXL.value:
            registers.B = registers.B ^ operand
        elif instruction == Instructions.BST.value:
            combo_operand: int = get_combo_operand(operand, registers)
            registers.B = combo_operand % 8
        elif instruction == Instructions.JNZ.value:
            if registers.A == 0:
                INSTRUCTION_POINTER += 2
            else:
                INSTRUCTION_POINTER = operand
        elif instruction == Instructions.BXC.value:
            registers.B = registers.B ^ registers.C
        elif instruction == Instructions.OUT.value:
            combo_operand: int = get_combo_operand(operand, registers)
            output_list.append(combo_operand % 8)
        elif instruction == Instructions.BDV.value:
            combo_operand: int = get_combo_operand(operand, registers)
            registers.B = registers.A // (pow(2, combo_operand))
        elif instruction == Instructions.CDV.value:
            combo_operand: int = get_combo_operand(operand, registers)
            registers.C = registers.A // (pow(2, combo_operand))

        if instruction != Instructions.JNZ.value:
            INSTRUCTION_POINTER += 2

    registers = copy.deepcopy(original_registers)
    
    return ",".join(map(str, output_list))

def solution(file_path: Path) -> str:
    REGISTER_A_MATCH = re.compile(r"Register A: (\d+)")
    REGISTER_B_MATCH = re.compile(r"Register B: (\d+)")
    REGISTER_C_MATCH = re.compile(r"Register C: (\d+)")
    PROGRAM_MATCH = re.compile(r"Program: (.*)")

    INSTRUCTION_POINTER: int = 0
    # Increase by 2 expect jump
    # It halts if try read after code scope

    registers: Register = Register(0, 0, 0)
    program_steps: list[int] = []
    output_list: list[int] = []

    for line in File(file_path).read():
        line = line.strip()
        if line == "":
            continue

        if match := REGISTER_A_MATCH.match(line):
            registers.A = int(match[1])
        elif match := REGISTER_B_MATCH.match(line):
            registers.B = int(match[1])
        elif match := REGISTER_C_MATCH.match(line):
            registers.C = int(match[1])
        elif match := PROGRAM_MATCH.match(line):
            program_steps = match[1].strip().split(",")

    guess_numbers: list[int] = [0]
    iteration: int = len(program_steps) - 1
    while iteration >= 0:
        next_guess_numbers: list[int] = []
        for guess_number in guess_numbers:
            section = guess_number * 8
            for new_value in range(section, section + 8):
                output = old_solution(program_steps, registers, new_value)
                if output == ",".join(program_steps[iteration:]):
                    next_guess_numbers.append(new_value)

        guess_numbers = copy.deepcopy(next_guess_numbers)
        iteration -= 1

    return min(guess_numbers)

def main() -> None:
    print("Assert")
    assert solution("day_17/data_test_2.txt") == 117440
    print("Solution")
    print(solution("day_17/data.txt"))

if __name__ == "__main__":
    main()