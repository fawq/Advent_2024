from dataclasses import dataclass, field
from functools import cache
from pathlib import Path
from queue import Queue
from typing import Optional

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

@dataclass(frozen=True)
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

    def get_real_position_of_box(self, position: Position) -> Position:
        return position if self.get_element(position) == "[" else position.next_position(Direction.LEFT)
    
    def get_boxes_to_move(self, position: Position, direction: Direction) -> tuple[set[tuple[Position, str]], bool]:
        real_position_of_box: Position = self.get_real_position_of_box(position)
        position_left: Position = real_position_of_box
        position_right: Position = real_position_of_box.next_position(Direction.RIGHT)
        boxes_to_move: set[tuple[Position, str]] = set([
            (position_left, "["),
            (position_right, "]")
        ])

        next_unknown_position: Optional[Position] = None
        next_unknown_positions: Optional[list[Position]] = None
        if direction == Direction.RIGHT:
            next_unknown_position: Position = position_right.next_position(direction)
        elif direction == Direction.LEFT:
            next_unknown_position: Position = position_left.next_position(direction)
        elif direction == Direction.UP or direction == Direction.DOWN:
            next_unknown_positions: Position = [position_right.next_position(direction), position_left.next_position(direction)]

        if next_unknown_position is not None:
            if self.get_element(next_unknown_position) == "#":
                return set([]), False
            elif self.get_element(next_unknown_position) == ".":
                return boxes_to_move, True
            elif self.get_element(next_unknown_position) in "[]":
                new_boxes_to_move, is_possible_to_move = self.get_boxes_to_move(next_unknown_position, direction)
                    
                if is_possible_to_move:
                    boxes_to_move.update(new_boxes_to_move)
                    return boxes_to_move, True
                else:
                    return set([]), False

        if next_unknown_positions is not None:
            if self.get_element(next_unknown_positions[0]) == "#" or self.get_element(next_unknown_positions[1]) == "#":
                return set([]), False
            elif self.get_element(next_unknown_positions[0]) == "." and self.get_element(next_unknown_positions[1]) == ".":
                return boxes_to_move, True
            else:
                is_possible_to_move_left = True
                is_possible_to_move_right = True
                new_boxes_to_move_left: set[tuple[Position, str]] = set([])
                new_boxes_to_move_right: set[tuple[Position, str]] = set([])

                if self.get_element(next_unknown_positions[0]) in "[]":
                    new_boxes_to_move_left, is_possible_to_move_left = self.get_boxes_to_move(next_unknown_positions[0], direction)
                if self.get_element(next_unknown_positions[1]) in "[]":
                    new_boxes_to_move_right, is_possible_to_move_right = self.get_boxes_to_move(next_unknown_positions[1], direction)
                    
                if is_possible_to_move_left and is_possible_to_move_right:
                    boxes_to_move.update(new_boxes_to_move_left)
                    boxes_to_move.update(new_boxes_to_move_right)
                    return boxes_to_move, True
                else:
                    return set([]), False

    def try_move(self, position: Position, direction: Direction) -> Position:
        next_position: Position = position.next_position(direction)
        
        if self.get_element(next_position) == "#":
            return position
        elif self.get_element(next_position) == ".":
            return next_position
        elif self.get_element(next_position) in "[]":
            boxes_to_move, is_possible_to_move = self.get_boxes_to_move(next_position, direction)

            if is_possible_to_move:
                for box_to_move in boxes_to_move:
                    self.set_element(box_to_move[0], ".")
                
                for box_to_move in boxes_to_move:
                    self.set_element(box_to_move[0].next_position(direction), box_to_move[1])

                return next_position
            else:
                return position

        return next_position
    
    def get_position_of_boxes(self) -> list[Position]:
        positions: list[Position] = []
        for row in range(self.height()):
            for column in range(self.width()):
                if self.get_element(Position(row, column)) == "[":
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
            new_line: list[str] = []
            for char in line:
                if char == ".":
                    new_line.append("..")
                elif char == "#":
                    new_line.append("##")
                elif char == "@":
                    new_line.append("@.")
                elif char == "O":
                    new_line.append("[]")

            full_line: str = "".join(new_line)
            matrix.add_row(list(full_line))
            
            if '@' in full_line:
                start_position = Position(matrix.height() - 1, full_line.index('@'))
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
    assert solution("day_15/small_data_test_2.txt") == 618
    assert solution("day_15/data_test.txt") == 9021
    print(solution("day_15/data.txt"))

if __name__ == "__main__":
    main()