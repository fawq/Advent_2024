from dataclasses import dataclass, field
import enum
from pathlib import Path
from typing import Self
from utils.load_file import File

@dataclass(frozen=True)
class Vector:
    add_row: int
    add_column: int
    symbol: str

class Direction(enum.Enum):
    UP = Vector(-1, 0, '^')
    RIGHT = Vector(0, 1, '>')
    DOWN = Vector(1, 0, 'v')
    LEFT = Vector(0, -1, '<')

    @enum.property
    def direction_on_right(self) -> Self:
        match self:
            case Direction.UP:
                return Direction.RIGHT
            case Direction.RIGHT:
                return Direction.DOWN
            case Direction.DOWN:
                return Direction.LEFT
            case Direction.LEFT:
                return Direction.UP

@dataclass(frozen=True)
class Position: 
    row: int
    column: int

    def next_position(self, direction: Direction) -> Self:
        return Position(self.row + direction.value.add_row, self.column + direction.value.add_column)
        
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

    def get_position_of_dots(self) -> list[Position]:
        positions: list[Position] = []
        for row in range(self.height()):
            for column in range(self.width()):
                if self.matrix[row][column] == '.':
                    positions.append(Position(row, column))
        return positions

def is_in_loop(matrix: Matrix, start_position: Position, hashtag_position: Position) -> bool:
    direction: Direction = Direction.UP
    visited_places: set[tuple[Position, Direction]] = set()
                
    actual_position: Position = start_position
    next_position: Position = actual_position.next_position(direction)
    while next_position.is_in_bounds(matrix.height(), matrix.width()):
        if (actual_position, direction) in visited_places:
            return True
        visited_places.add((actual_position, direction))

        if matrix.get_element(next_position) == '#' or next_position == hashtag_position:
            direction = direction.direction_on_right
        else:
            actual_position = next_position
                    
        next_position = actual_position.next_position(direction)

    return False

def solution(file_path: Path) -> int:
    matrix: Matrix = Matrix()
    start_position: Position = Position(-1, -1)
    guards_count: int = 0

    for row, line in enumerate(File(file_path).read()):
        line = line.strip()
        if line == "":
            break

        if '^' in line:
            start_position = Position(row, line.index('^'))        
        matrix.add_row(list(line))

    for dot_position in matrix.get_position_of_dots():
        if is_in_loop(matrix, start_position, dot_position):
            guards_count += 1

    return guards_count

def main() -> None:
    assert solution("day_06/data_test.txt") == 6
    print(solution("day_06/data.txt"))

if __name__ == "__main__":
    main()