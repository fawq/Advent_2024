from dataclasses import dataclass
from functools import reduce
import operator
from pathlib import Path
import re
from typing import Counter, Iterable, Self

from utils.load_file import File

@dataclass(frozen=True)
class PositionAndVector:
    position_x: int
    position_y: int
    vector_x: int
    vector_y: int

    def get_new_position_and_vector(self, seconds: int, height: int, width: int) -> Self:
        new_position_x = (self.position_x + self.vector_x * seconds) % width
        new_position_y = (self.position_y + self.vector_y * seconds) % height

        return PositionAndVector(new_position_x, new_position_y, self.vector_x, self.vector_y)

def product(xs: Iterable[int]) -> int:
    return reduce(operator.mul, xs, 1)

def solution(file_path: Path, height: int, width: int, seconds: int = 100) -> int:
    position_and_vector_match = re.compile(r"p=(?P<position_x>\d+),(?P<position_y>\d+) v=(?P<vector_x>-?\d+),(?P<vector_y>-?\d+)")

    positions_and_vectors: list[PositionAndVector] = []
    quadrant: Counter[str] = Counter()

    for line in File(file_path).read():
        line = line.strip()
        if line == "":
            break

        if match := position_and_vector_match.match(line):
            position_x = int(match.group("position_x"))
            position_y = int(match.group("position_y"))
            vector_x = int(match.group("vector_x"))
            vector_y = int(match.group("vector_y"))

            positions_and_vectors.append(PositionAndVector(position_x, position_y, vector_x, vector_y))

    positions_and_vectors = list(map(lambda x: x.get_new_position_and_vector(seconds, height, width), positions_and_vectors))

    for position_and_vector in positions_and_vectors:
        new_position_x = position_and_vector.position_x
        new_position_y = position_and_vector.position_y

        if new_position_x < width // 2 and new_position_y < height // 2:
            quadrant["UL"] += 1
        elif new_position_x < width // 2 and new_position_y > height // 2:
            quadrant["DL"] += 1
        elif new_position_x > width // 2 and new_position_y < height // 2:
            quadrant["UR"] += 1
        elif new_position_x > width // 2 and new_position_y > height // 2:
            quadrant["DR"] += 1
    
    return product(quadrant.values())

def main() -> None:
    assert solution("day_14/data_test.txt", 7, 11) == 12
    print(solution("day_14/data.txt", 103, 101))

if __name__ == "__main__":
    main()