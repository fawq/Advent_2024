from dataclasses import dataclass
from enum import Enum
from typing import Self


@dataclass(frozen=True)
class Vector:
    add_row: int
    add_column: int

    def get_taxicab_distance(self) -> int:
        return abs(self.add_row) + abs(self.add_column)
    
class Direction(Enum):
    UP = Vector(-1, 0)
    DOWN = Vector(1, 0)
    LEFT = Vector(0, -1)
    RIGHT = Vector(0, 1)

@dataclass(frozen=True)
class Position:
    row: int
    column: int

    def next_position(self, direction: Direction) -> Self:
        return self.__class__(self.row + direction.value.add_row, self.column + direction.value.add_column)
    
    def vector_to(self, position: Self) -> Vector:
        return Vector(position.row - self.row, position.column - self.column)
    
@dataclass(frozen=True)
class PositionCost:
    position: Position
    distance: int