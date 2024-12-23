from dataclasses import dataclass, field
import enum
from pathlib import Path
from queue import Queue
from typing import Self

from utils.load_file import File


@dataclass(frozen=True)
class Vector:
    add_row: int
    add_coulmn: int

class Direction(enum.Enum):
    UP = Vector(-1, 0)
    RIGHT = Vector(0, 1)
    DOWN = Vector(1, 0)
    LEFT = Vector(0, -1)

@dataclass(frozen=True)
class Position: 
    row: int
    column: int

    def next_position(self, direction: Direction) -> Self:
        return Position(self.row + direction.value.add_row, self.column + direction.value.add_coulmn)
        
    def is_in_bounds(self, height: int, width: int) -> bool:
        return self.row >= 0 and self.row < height and self.column >= 0 and self.column < width

@dataclass
class Matrix():
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

    def get_all_positions(self) -> list[Position]:
        positions: list[Position] = []
        for row in range(self.height()):
            for column in range(self.width()):
                positions.append(Position(row, column))
        return positions
    
    def get_neighbors(self, position: Position) -> list[Position]:
        neighbors: list[Position] = []
        for direction in Direction:
            next_position: Position = position.next_position(direction)
            if next_position.is_in_bounds(self.height(), self.width()) \
                and self.get_element(next_position) == self.get_element(position):
                neighbors.append(next_position)
        return neighbors
    
    def get_price(self) -> int:
        score: int = 0
        explored_positions: set[Position] = set()

        for position in self.get_all_positions():
            if position not in explored_positions:
                bfs_queue: Queue[Position] = Queue()
                bfs_queue.put(position)

                explored_positions.add(position)

                area: int = 0
                perimeter: int = 0

                while not bfs_queue.empty():
                    current_position: Position = bfs_queue.get()
                    possible_neighbor: list[Position] = self.get_neighbors(current_position)

                    area += 1
                    perimeter += (4 - len(possible_neighbor))

                    for neighbor in possible_neighbor:
                        if neighbor not in explored_positions:
                            explored_positions.add(neighbor)
                            bfs_queue.put(neighbor)

                score += area * perimeter
        
        return score

def solution(file_path: Path) -> int:
    matrix: Matrix = Matrix()

    for line in File(file_path).read():
        line = line.strip()
        if line == "":
            break

        matrix.add_row(list(line))

    return matrix.get_price()

def main():
    assert solution("day_12/data_test.txt") == 1930
    print(solution("day_12/data.txt"))

if __name__ == "__main__":
    main()