from collections import defaultdict
from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path
from typing import Self

from utils.load_file import File


@dataclass(frozen=True)
class Position: 
    row: int
    column: int

    def antinode_positions(self, antenna_position: Self) -> tuple[Self, Self]:
        diff_row: int = self.row - antenna_position.row
        diff_column: int = self.column - antenna_position.column

        first_position: Position = Position(antenna_position.row - diff_row, antenna_position.column - diff_column)
        second_position: Position = Position(self.row + diff_row, self.column + diff_column)

        return first_position, second_position
        
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
            first_antinode_position, second_antinode_position = first_antenna_position.antinode_positions(second_antenna_position)

            if first_antinode_position.is_in_bounds(matrix.height(), matrix.width()):
                unique_antinodes.add(first_antinode_position)
            
            if second_antinode_position.is_in_bounds(matrix.height(), matrix.width()):
                unique_antinodes.add(second_antinode_position)

    return len(unique_antinodes)

def main() -> None:
    assert solution("day_08/data_test.txt") == 14
    print(solution("day_08/data.txt"))

if __name__ == "__main__":
    main()