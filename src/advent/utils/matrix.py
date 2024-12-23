from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, Self
from advent.utils.position import Position


@dataclass
class Matrix[T]:
    matrix: list[list[T]] = field(default_factory=list)

    def __str__(self) -> str:
        image: str = ""
        for row_list in self.matrix:
            for column in row_list:
                character: Optional[Any] = None
                if isinstance(column , Enum):
                    character = column.value
                else:
                    character = column

                if character is not None:
                    if hasattr(character, '__str__') or hasattr(character, '__repr__'):
                        image += str(character)
                    else:
                        raise Exception(f"Given character is of type {type(character)} which is not supported.")
                else:
                    raise Exception(f"Unknown character: {character}")
                image += " "
            image += "\n"
        return image

    def __repr__(self) -> str:
        return self.__str__()
    
    def __add__(self, other: Position, value: T) -> Self:
        new_matrix = deepcopy(self)
        new_matrix.set_element(other, value)
        return new_matrix
    
    def get_height(self) -> int:
        return len(self.matrix)

    def get_width(self) -> int:
        return len(self.matrix[0])

    def set_element(self, position: Position, value: T):
        self.matrix[position.row][position.column] = value

    def add_row(self, row: list[T]):
        self.matrix.append(row)

    def get_element(self, position: Position, default: Optional[T] = None) -> Optional[T]:
        if self.is_in_bounds(position):
            return self.matrix[position.row][position.column]
        if default is not None:
            return default
        return None
    
    def is_in_bounds(self, position: Position) -> bool:
        return 0 <= position.row < self.get_height() and 0 <= position.column < self.get_width()