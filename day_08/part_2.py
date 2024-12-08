from collections import defaultdict
from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path
from typing import Self

from utils.load_file import File

@dataclass(frozen=True)
class Vector:
    add_row: int
    add_column: int

    def reverse(self) -> Self:
        return Vector(-self.add_row, -self.add_column)

@dataclass(frozen=True)
class Position: 
    row: int
    column: int

    def all_antinode_positions_on_line(self, antenna_position: Self, height: int, width: int) -> list[Self]:
        antinode_positions: list[Self] = []

        first_position = self
        second_position = antenna_position

        diff_vector = Vector(second_position.row - first_position.row, second_position.column - first_position.column)

        while first_position.is_in_bounds(height, width):
            antinode_positions.append(first_position)
            first_position = first_position.get_new_position(diff_vector.reverse())

        while second_position.is_in_bounds(height, width):
            antinode_positions.append(second_position)
            second_position = second_position.get_new_position(diff_vector)

        return antinode_positions

    def get_new_position(self, vector: Vector) -> Self:
        return Position(self.row + vector.add_row, self.column + vector.add_column)
        
    def is_in_bounds(self, height: int, width: int) -> bool:
        return self.row >= 0 and self.row < height and self.column >= 0 and self.column < width
    
@dataclass
class Matrix():
    matrix: list[list[str]] = field(default_factory=list)
    
    def height(self) -> int:
        return len(self.matrix)
    
    def width(self) -> int:
        return len(self.matrix[0])

    def get_element(self, position: Position) -> str:
        return self.matrix[position.row][position.column]
    
    def set_element(self, position: Position, value: str):
        self.matrix[position.row][position.column] = value
    
    def add_row(self, row: list[str]):
        self.matrix.append(row)

    def get_grouped_antennas(self) -> dict[str, list[Position]]:
        antennas: defaultdict[str, list[Position]] = defaultdict(list)
        for row in range(self.height()):
            for column in range(self.width()):
                antenna_name: str = self.get_element(Position(row, column))
                if antenna_name != '.':
                    antennas[antenna_name].append(Position(row, column))

        return antennas

def solution(file_path: Path) -> int:
    matrix: Matrix = Matrix()

    for line in File(file_path).read():
        line = line.strip()
        if line == "":
            break

        matrix.add_row(list(line))

    grouped_antennas: dict[str, list[Position]] = matrix.get_grouped_antennas()

    unique_antinodes: set[Position] = set()
    for _, antennas in grouped_antennas.items():
        for first_antenna_position, second_antenna_position in combinations(antennas, 2):
            unique_antinodes.update(first_antenna_position.all_antinode_positions_on_line(second_antenna_position, matrix.height(), matrix.width()))

    return len(unique_antinodes)

def main() -> None:
    assert solution("day_08/data_test.txt") == 34
    print(solution("day_08/data.txt"))

if __name__ == "__main__":
    main()