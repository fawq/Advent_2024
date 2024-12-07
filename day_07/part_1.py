from pathlib import Path
from utils.load_file import File


def parse_equation(line: str) -> tuple[int, list[int]]:
    result, numbers = line.split(':', 1)
    result = int(result)

    numbers = numbers.split()
    numbers = list(map(int, numbers))

    return result, numbers

def is_possible_to_solve(result: int, numbers: list[int]) -> bool:
    rest_numbers, last_number = numbers[:-1], numbers[-1]

    if len(rest_numbers) == 0:
        if result == last_number:
            return True
        return False

    if result - last_number > 0:
        if not is_possible_to_solve(result - last_number, rest_numbers):
           if result % last_number == 0:
               return is_possible_to_solve(result // last_number, rest_numbers)
        else:
            return True
    elif result == last_number:
        return is_possible_to_solve(1, rest_numbers)
    return False
    
def solution(file_path: Path) -> int:
    equations: list[tuple[int, list[int]]] = []

    for line in File(file_path).read():
        line = line.strip()
        if line == "":
            break

        equation: tuple[int, list[int]] = parse_equation(line)
        equations.append(equation)

    sum_valid_results: int = 0
    for equation in equations:
        result, numbers = equation
        if is_possible_to_solve(result, numbers):
            sum_valid_results += result

    return sum_valid_results

def main() -> None:
    assert solution(Path("day_07/data_test.txt")) == 3749
    print(solution(Path("day_07/data.txt")))

if __name__ == "__main__":
    main()