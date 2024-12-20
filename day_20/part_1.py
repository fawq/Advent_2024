from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from queue import Queue
from typing import Self

from utils.load_file import File


@dataclass(frozen=True)
class Vector:
    add_row: int
    add_column: int

    def get_taxicab_distance(self) -> int:
        return abs(self.add_row) + abs(self.add_column)

class Direction(Enum):
    UP = Vector(-1, 0)
    RIGHT = Vector(0, 1)
    DOWN = Vector(1, 0)
    LEFT = Vector(0, -1)

@dataclass(frozen=True)
class Position:
    row: int
    column: int

    def next_position(self, direction: Direction) -> Self:
        return Position(self.row + direction.value.add_row, self.column + direction.value.add_column)
    
    def vector_to(self, position: Self) -> Vector:
        return Vector(position.row - self.row, position.column - self.column)

class Element(Enum):
    WALL = "#"
    TRACK = "."
    START = "S"
    END = "E"

    def is_valid(self) -> bool:
        return self in [self.TRACK, self.START, self.END]

@dataclass
class Matrix:
    matrix: list[list[Element]] = field(default_factory=list)

    def set_element(self, position: Position, value: Element):
        self.matrix[position.row][position.column] = value

    def add_row(self, row: list[Element]):
        self.matrix.append(row)

    def get_element(self, position: Position) -> Element:
        if self.is_in_bounds(position):
            return self.matrix[position.row][position.column]
        else:
            return Element.WALL

    def height(self) -> int:
        return len(self.matrix)

    def width(self) -> int:
        return len(self.matrix[0])

    def __str__(self) -> str:
        return "\n".join(["".join([element.value for element in row]) for row in self.matrix])

    def __repr__(self) -> str:
        return self.__str__()
    
    def is_in_bounds(self, position: Position) -> bool:
        return 0 <= position.row < self.height() and 0 <= position.column < self.width()
    
    def get_neighbors(self, position: Position) -> list[Position]:
        neighbors: list[Position] = []
        for direction in Direction:
            next_position = position.next_position(direction)
            if self.get_element(next_position).is_valid():
                neighbors.append(next_position)
        return neighbors

    def _is_thin_wall(self, position: Position) -> bool:
        if self.get_element(position) != Element.WALL:
            return False

        south_element = self.get_element(position.next_position(Direction.DOWN))
        north_element = self.get_element(position.next_position(Direction.UP))
        west_element = self.get_element(position.next_position(Direction.LEFT))
        east_element = self.get_element(position.next_position(Direction.RIGHT))
        
        if (south_element.is_valid() and north_element.is_valid()) or (west_element.is_valid() and east_element.is_valid()):
            return True
        return False

    def get_thin_walls(self) -> list[Position]:
        positions: list[Position] = []
        for row in range(self.height()):
            for column in range(self.width()):
                current_position = Position(row, column)
                if self._is_thin_wall(current_position):
                    positions.append(current_position)
        return positions

@dataclass(frozen=True)
class PositionCost:
    position: Position
    distance: int

def bfs_with_visited_positions(matrix: Matrix, start_position: Position, end_position: Position) -> list[PositionCost]:
    visited: set[Position] = set()
    visited.add(start_position)
    
    queue: Queue[PositionCost] = Queue()
    queue.put(PositionCost(start_position, 0))

    all_position_costs: list[PositionCost] = []
    
    while not queue.empty():
        current_position_cost = queue.get()

        all_position_costs.append(current_position_cost)
        current_position = current_position_cost.position
        distance = current_position_cost.distance

        if current_position == end_position:
            return all_position_costs
        
        for neighbor in matrix.get_neighbors(current_position):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.put(PositionCost(neighbor, distance + 1))
    return all_position_costs

def solution(file_path: Path, min_gain: int = 100) -> int:
    matrix = Matrix()
    start_position: Position = Position(-1, -1)
    end_position: Position = Position(-1, -1)

    for line in File(file_path).read():
        line = line.strip()
        if line == "":
            break

        if "S" in line:
            start_position = Position(matrix.height(), line.index("S"))
        if "E" in line:
            end_position = Position(matrix.height(), line.index("E"))

        matrix.add_row(list(map(Element, line)))

    all_position_costs = bfs_with_visited_positions(matrix, start_position, end_position)
    cheats: int = 0
    for position_cost in deepcopy(all_position_costs):
        current_position = position_cost.position
        current_cost = position_cost.distance

        for possible_position_cost in all_position_costs:
            possible_position = possible_position_cost.position
            possible_cost = possible_position_cost.distance
            taxicab_distance = current_position.vector_to(possible_position).get_taxicab_distance()

            if 1 <= taxicab_distance <= 2:
                if abs(current_cost - possible_cost) - taxicab_distance >= min_gain:
                    cheats += 1
        all_position_costs.remove(position_cost)
    return cheats

def main() -> None:
    assert solution(Path("day_20/data_test.txt"), 20) == 5
    print(solution(Path("day_20/data.txt")))

if __name__ == "__main__":
    main()