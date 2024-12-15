from dataclasses import dataclass, field
from pathlib import Path

from utils.load_file import File

@dataclass(frozen=True)
class Vector:
    add_row: int
    add_column: int

@dataclass
class Direction:
    UP: Vector = Vector(-1, 0)
    RIGHT: Vector = Vector(0, 1)
    DOWN: Vector = Vector(1, 0)
    LEFT: Vector = Vector(0, -1)   

@dataclass
class Position:
    row: int
    column: int

    def next_position(self, direction: Direction):
        return Position(self.row + direction.add_row, self.column + direction.add_column)

@dataclass
class Matrix:
    matrix: list[list[int]] = field(default_factory=list)

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

    def try_move(self, position: Position, direction: Direction) -> Position:
        next_position: Position = position.next_position(direction)
        
        if self.get_element(next_position) == "#":
            return position
        elif self.get_element(next_position) == ".":
            return next_position
        elif self.get_element(next_position) == "O":
            box_position: Position = next_position
            first_not_box_position: Position = next_position.next_position(direction)

            while self.get_element(first_not_box_position) == "O":
                first_not_box_position = first_not_box_position.next_position(direction)

            if self.get_element(first_not_box_position) == "#":
                return position
            elif self.get_element(first_not_box_position) == ".":
                self.set_element(box_position, ".")
                self.set_element(first_not_box_position, "O")

                return next_position

        return next_position
    
    def get_position_of_boxes(self) -> list[Position]:
        positions: list[Position] = []
        for row in range(self.height()):
            for column in range(self.width()):
                if self.get_element(Position(row, column)) == "O":
                    positions.append(Position(row, column))
        return positions

def solution(file_path: Path) -> int:
    matrix: Matrix = Matrix()
    start_position: Position = Position(-1, -1)
    moves: str = ""

    is_parse_map: bool = True
    for line in File(file_path).read():
        line = line.strip()
        if line == "":
            is_parse_map = False

        if is_parse_map:
            matrix.add_row(list(line))
            
            if '@' in line:
                start_position = Position(matrix.height() - 1, line.index('@'))
        else:
            moves += line

    matrix.set_element(start_position, ".")

    for move in moves:
        if move == '^':
            start_position = matrix.try_move(start_position, Direction.UP)
        elif move == '>':
            start_position = matrix.try_move(start_position, Direction.RIGHT)
        elif move == 'v':
            start_position = matrix.try_move(start_position, Direction.DOWN)
        elif move == '<':
            start_position = matrix.try_move(start_position, Direction.LEFT)

    result: int = 0
    for position in matrix.get_position_of_boxes():
        result += 100 * position.row + position.column

    return result

def main() -> None:
    assert solution("day_15/small_data_test.txt") == 2028
    assert solution("day_15/data_test.txt") == 10092
    print(solution("day_15/data.txt"))

if __name__ == "__main__":
    main()