from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from functools import cache
from pathlib import Path
from typing import Self

from utils.load_file import File


@dataclass(frozen=True)
class Vector:
    add_row: int
    add_column: int

class Direction(Enum):
    UP = Vector(-1, 0)
    DOWN = Vector(1, 0)
    LEFT = Vector(0, -1)
    RIGHT = Vector(0, 1)

    def get_char(self) -> str:
        match self:
            case Direction.UP:
                return '^'
            case Direction.DOWN:
                return 'v'
            case Direction.LEFT:
                return '<'
            case Direction.RIGHT:
                return '>'

@dataclass(frozen=True)
class Position:
    row: int
    column: int

    def next_position(self, direction: Direction) -> Self:
        return self.__class__(self.row + direction.value.add_row, self.column + direction.value.add_column)

    def vector_to(self, position: Self) -> Vector:
        return Vector(position.row - self.row, position.column - self.column)

@dataclass(frozen=True)
class BasicKeyboard(ABC):
    keyboard: list[list[str]] = field(default_factory=list)

    def is_in_bounds(self, position: Position) -> bool:
        keyboard_rows = len(self.keyboard)
        keyboard_columns = len(self.keyboard[0])
        forbidden_position = self.get_character_position('F')

        return 0 <= position.row < keyboard_rows and 0 <= position.column < keyboard_columns and position != forbidden_position

    def get_element(self, position: Position) -> str:
        return self.keyboard[position.row][position.column]

    @abstractmethod
    def get_character_position(self, character: str) -> Position:
        ...

@dataclass(frozen=True)
class NumericKeyboard(BasicKeyboard):
    keyboard:list[list[str]] = field(
        default_factory=lambda: [['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3'], ['F', '0', 'A']])
    
    def get_character_position(self, character: str) -> Position:
        match character:
            case '7':
                return Position(0, 0)
            case '8':
                return Position(0, 1)
            case '9':
                return Position(0, 2)
            case '4':
                return Position(1, 0)
            case '5':
                return Position(1, 1)
            case '6':
                return Position(1, 2)
            case '1':
                return Position(2, 0)
            case '2':
                return Position(2, 1)
            case '3':
                return Position(2, 2)
            case 'F':
                return Position(3, 0)
            case '0':
                return Position(3, 1)
            case 'A':
                return Position(3, 2)
            case _:
                raise ValueError
            
@dataclass(frozen=True)
class DigitalKeyboard(BasicKeyboard):
    keyboard: list[list[str]] = field(default_factory=lambda: [['F', '^', 'A'], ['<', 'v', '>']])
    
    def get_character_position(self, character: str) -> Position:
        match character:
            case 'F':
                return Position(0, 0)
            case '^':
                return Position(0, 1)
            case 'A':
                return Position(0, 2)
            case '<':
                return Position(1, 0)
            case 'v':
                return Position(1, 1)
            case '>':
                return Position(1, 2)
            case _:
                raise ValueError
            
class Keyboard(Enum):
    NUMERIC = NumericKeyboard()
    DIGITAL = DigitalKeyboard()
    
@cache
def get_taxicab_paths(source: Position, destination: Position, type_of_keyboard: Keyboard) -> set[str]:
    paths: set[str] = set()
    vector_to_destination = source.vector_to(destination)
    add_row = vector_to_destination.add_row
    add_column = vector_to_destination.add_column

    if add_row == 0 and add_column == 0:
        return set(['A'])

    if add_row != 0:
        direction = Direction.DOWN if add_row > 0 else Direction.UP
        direction_char = direction.get_char()

        new_position = source.next_position(direction)
        if type_of_keyboard.value.is_in_bounds(new_position):
            for path in get_taxicab_paths(new_position, destination, type_of_keyboard):
                paths.add(direction_char + path)
    
    if add_column != 0:
        direction = Direction.RIGHT if add_column > 0 else Direction.LEFT
        direction_char = direction.get_char()

        new_position = source.next_position(direction)
        if type_of_keyboard.value.is_in_bounds(new_position):
            for path in get_taxicab_paths(new_position, destination, type_of_keyboard):
                paths.add(direction_char + path)    
    
    return paths

@cache
def get_complexity(sequence: str, keyboard: Keyboard, depth: int) -> int:
    if depth == 0:
        return len(sequence)
    
    current_character: str = 'A'
    min_length: int = 0
    for next_character in sequence:
        current_character_position_in_keyboard = keyboard.value.get_character_position(current_character)
        next_character_position_in_keyboard = keyboard.value.get_character_position(next_character)

        all_paths = get_taxicab_paths(current_character_position_in_keyboard, next_character_position_in_keyboard, keyboard)
        all_possible_paths_min_length = [get_complexity(sub_sequence, Keyboard.DIGITAL, depth - 1) for sub_sequence in all_paths]

        current_character = next_character
        min_length += min(all_possible_paths_min_length)

    if keyboard == Keyboard.NUMERIC:
        return min_length * int(sequence[:-1])
    return min_length

def solution(file_path: Path, depth: int = 26) -> int:
    sequences: list[str] = []
    
    for line in File(file_path).read():
        line = line.strip()
        if line == "":
            break

        sequences.append(line)
    
    sum_of_complexity: int = 0
    for sequence in sequences:
        complexity = get_complexity(sequence, Keyboard.NUMERIC, depth)
        sum_of_complexity += complexity

    return sum_of_complexity

def main() -> None:
    assert solution(Path("day_21/data_test.txt")) == 154115708116294
    print(solution(Path("day_21/data.txt")))

if __name__ == "__main__":
    main()