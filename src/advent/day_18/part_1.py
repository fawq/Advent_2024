from queue import Queue
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Self

from utils.load_file import File


@dataclass(frozen=True)
class Vector:
    add_row: int
    add_column: int

class Direction(Enum):
    UP = Vector(-1, 0)
    RIGHT = Vector(0, 1)
    DOWN = Vector(1, 0)
    LEFT = Vector(0, -1)

@dataclass(frozen=True)
class Position:
    row: int
    column: int

    def is_in_bounds(self, height: int, width: int) -> bool:
        return 0 <= self.row < height and 0 <= self.column < width
    
    def next_position(self, direction: Direction) -> Self:
        return Position(self.row + direction.value.add_row, self.column + direction.value.add_column)

@dataclass
class Matrix:
    matrix: list[list[str]] = field(default_factory=list)

    def height(self) -> int:
        return len(self.matrix)
    
    def width(self) -> int:
        return len(self.matrix[0])

    def get_element(self, position: Position) -> str:
        return self.matrix[position.row][position.column]
    
    def set_element(self, position: Position, value: str) -> None:
        self.matrix[position.row][position.column] = value

    def prepare_matrix(self, height: int, width: int) -> None:
        for _ in range(height):
            self.matrix.append(['.'] * width)

    def get_neighbors(self, position: Position) -> list[Position]:
        neighbors: list[Position] = []
        for direction in Direction:
            next_position: Position = position.next_position(direction)
            if (next_position.is_in_bounds(self.height(), self.width()) and self.get_element(next_position) == "."):
                neighbors.append(next_position)
        return neighbors

@dataclass(frozen=True)
class PositionDistance:
    position: Position
    distance: int

def solution(file_path: Path, height: int, width: int, simulate_bytes: int) -> int:
    matrix: Matrix = Matrix()
    start_position: Position = Position(0, 0)
    end_position: Position = Position(height - 1, width - 1)
    cross_positions: list[Position] = []

    matrix.prepare_matrix(height, width)

    for line in File(file_path).read():
        line = line.strip()
        if line == "":
            break

        X, Y = map(int, line.split(","))
        cross_position: Position = Position(Y, X)
        cross_positions.append(cross_position)

    for index in range(simulate_bytes):
        matrix.set_element(cross_positions[index], "#")

    node_queue: Queue[PositionDistance] = Queue()
    node_queue.put(PositionDistance(start_position, 0))

    visited_positions: set[Position] = set()
    visited_positions.add(start_position)

    steps: int = 0
    while not node_queue.empty():
        current_position_and_distance: PositionDistance = node_queue.get()
        current_position = current_position_and_distance.position
        distance = current_position_and_distance.distance

        if current_position == end_position:
            steps = distance
            break

        distance += 1
        for neighbor in matrix.get_neighbors(current_position):
            if neighbor not in visited_positions:
                visited_positions.add(neighbor)
                node_queue.put(PositionDistance(neighbor, distance))

    return steps

def main() -> None:
    assert solution("src/advent/day_18/data_test.txt", 7, 7, 12) == 22
    print(solution("src/advent/day_18/data.txt", 71, 71, 1024))

if __name__ == "__main__":
    main()