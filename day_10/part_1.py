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

    def get_element(self, position: Position) -> int:
        return self.matrix[position.row][position.column]
    
    def set_element(self, position: Position, value: int):
        self.matrix[position.row][position.column] = value
    
    def add_row(self, row: list[int]):
        self.matrix.append(row)

    def get_possible_trailhead_positions(self) -> list[Position]:
        positions: list[Position] = []
        for row in range(self.height()):
            for column in range(self.width()):
                if self.get_element(Position(row, column)) == 0:
                    positions.append(Position(row, column))
        return positions
    
def trail_score(position: Position, matrix: Matrix) -> int:
    score: int = 0
    directions: list[Direction] = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]

    explored_positions: set[Position] = set()
    explored_positions.add(position)

    bfs_queue: Queue[Position] = Queue()
    bfs_queue.put(position)

    while not bfs_queue.empty():
        current_position: Position = bfs_queue.get()
        current_position_value: int = matrix.get_element(current_position)

        if current_position_value == 9:
            score += 1

        for direction in directions:
            next_position: Position = current_position.next_position(direction)

            if next_position.is_in_bounds(matrix.height(), matrix.width()):
                next_position_value: int = matrix.get_element(next_position)

                if next_position not in explored_positions and next_position_value == current_position_value + 1:
                    explored_positions.add(next_position)
                    bfs_queue.put(next_position)
    
    return score

def solution(file_path: Path) -> int:
    matrix: Matrix = Matrix()

    for line in File(file_path).read():
        line = line.strip()
        if line == "":
            break

        matrix.add_row(list(map(int, line)))
    
    trailhead_positions: list[Position] = matrix.get_possible_trailhead_positions()

    return sum(trail_score(position, matrix) for position in trailhead_positions)

def main() -> None:
    assert solution("day_10/data_test.txt") == 36
    print(solution("day_10/data.txt"))

if __name__ == "__main__":
    main()