from dataclasses import dataclass
from pathlib import Path
import re

from utils.load_file import File


@dataclass(frozen=True)
class Equation:
    a1: int
    a2: int
    b1: int
    b2: int
    c1: int
    c2: int

def solution(file_path: Path) -> int:
    button_a_match = re.compile(r"Button A: X\+(\d+), Y\+(\d+)")
    button_b_match = re.compile(r"Button B: X\+(\d+), Y\+(\d+)")
    prize_match = re.compile(r"Prize: X=(\d+), Y=(\d+)")

    equations: list[Equation] = []

    a1 = a2 = b1 = b2 = c1 = c2 = -1
    for line in File(file_path).read():
        line = line.strip()
        if line == "":
            continue

        if match := button_a_match.match(line):
            a1 = int(match.group(1))
            a2 = int(match.group(2))
        elif match := button_b_match.match(line):
            b1 = int(match.group(1))
            b2 = int(match.group(2))
        elif match := prize_match.match(line):
            c1 = int(match.group(1))
            c2 = int(match.group(2))

        if a1 != -1 and a2 != -1 and b1 != -1 and b2 != -1 and c1 != -1 and c2 != -1:
            equations.append(Equation(a1, a2, b1, b2, c1, c2))
            a1 = a2 = b1 = b2 = c1 = c2 = -1

    tokens: int = 0
    for equation in equations:
        x_numerator = equation.b2 * equation.c1 - equation.b1 * equation.c2
        y_numerator = equation.a1 * equation.c2 - equation.a2 * equation.c1
        denominator = equation.a1 * equation.b2 - equation.a2 * equation.b1

        if denominator != 0 and x_numerator % denominator == 0 and y_numerator % denominator == 0:
            x = x_numerator // denominator
            y = y_numerator // denominator
            tokens += 3 * x + y
    
    return tokens

def main() -> None:
    assert solution("day_13/data_test.txt") == 480
    print(solution("day_13/data.txt"))

if __name__ == "__main__":
    main()