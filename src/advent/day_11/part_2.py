from functools import cache
from pathlib import Path

from utils.load_file import File

def get_number_of_didigts(number: int) -> int:
    return len(str(number))

@cache
def get_number_of_stones(number: int, iterations: int) -> int:
    if iterations > 0:
        if number == 0:
            return get_number_of_stones(1, iterations - 1)
        elif get_number_of_didigts(number) % 2 == 0:
            first_half, second_half = str(number)[:len(str(number)) // 2], str(number)[len(str(number)) // 2:]
            return get_number_of_stones(int(first_half), iterations - 1) + get_number_of_stones(int(second_half), iterations - 1)
        else:
            return get_number_of_stones(number * 2024, iterations - 1)
    else:
        return 1

def solution(file_path: Path) -> int:
    numbers: list[int] = []
    
    for line in File(file_path).read():
        line = line.strip()
        if line == "":
            break

        numbers = list(map(int, line.split()))

    return sum(get_number_of_stones(number, 75) for number in numbers)

def main() -> None:
    assert solution("day_11/data_test.txt") == 65601038650482
    print(solution("day_11/data.txt"))

if __name__ == "__main__":
    main()