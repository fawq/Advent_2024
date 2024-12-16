from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
import heapq
from pathlib import Path
import sys
from typing import Self

from utils.load_file import File

class Direction(Enum):
    EAST = (0, 1)
    WEST = (0, -1)
    NORTH = (-1, 0)
    SOUTH = (1, 0)

    def __lt__(self, other: Self) -> bool:
        if self.value[0] < other.value[0]:
            return True
        elif self.value[0] == other.value[0]:
            return self.value[1] < other.value[1]
        else:
            return False

def turn_counter_clockwise(direction: Direction) -> Direction:
    match direction:
        case Direction.EAST:
            return Direction.NORTH
        case Direction.NORTH:
            return Direction.WEST
        case Direction.WEST:
            return Direction.SOUTH
        case Direction.SOUTH:
            return Direction.EAST
        
def turn_clockwise(direction: Direction) -> Direction:
    match direction:
        case Direction.EAST:
            return Direction.SOUTH
        case Direction.SOUTH:
            return Direction.WEST
        case Direction.WEST:
            return Direction.NORTH
        case Direction.NORTH:
            return Direction.EAST

@dataclass(frozen=True)
class Point:
    row: int
    column: int

    def next_position(self, direction: Direction) -> Self:
        return Point(self.row + direction.value[0], self.column + direction.value[1])
    
    def __lt__(self, other: Self) -> bool:
        if self.row < other.row:
            return True
        elif self.row == other.row:
            return self.column < other.column
        else:
            return False

@dataclass
class Matrix:
    matrix: list[list[int]] = field(default_factory=list)

    def get_element(self, point: Point) -> str:
        return self.matrix[point.row][point.column]
    
    def add_row(self, row: list[int]):
        self.matrix.append(row)

def solution(file_path: Path) -> int:
    matrix: Matrix = Matrix()
    start_point: Point = Point(-1, -1)
    end_point: Point = Point(-1, -1)
    start_direction: Direction = Direction.EAST
    
    for line in File(file_path).read():
        line = line.strip()
        if line == "":
            break

        matrix.add_row(list(line))

        if 'S' in line:
            start_point = Point(len(matrix.matrix) - 1, line.index('S'))
        if 'E' in line:
            end_point = Point(len(matrix.matrix) - 1, line.index('E'))

    priority_nodes: list[tuple[int, Point, Direction]] = []
    heapq.heappush(priority_nodes, (0, start_point, start_direction))

    visited: dict[tuple[Point, Direction], int] = {}
    distance_to_end: int = sys.maxsize

    while priority_nodes:
        current_distance, point, direction = heapq.heappop(priority_nodes)
        if current_distance > distance_to_end:
            break

        if (point, direction) in visited and visited[(point, direction)] < current_distance:
            continue
        visited[(point, direction)] = current_distance

        if point == end_point:
            distance_to_end = current_distance

        if matrix.get_element(point.next_position(direction)) != '#':
            heapq.heappush(priority_nodes, (current_distance + 1, point.next_position(direction), direction))

        heapq.heappush(priority_nodes, (current_distance + 1000, point, turn_counter_clockwise(direction)))
        heapq.heappush(priority_nodes, (current_distance + 1000, point, turn_clockwise(direction)))

    return distance_to_end

def main() -> None:
    assert solution("day_16/data_test.txt") == 7036
    assert solution("day_16/data_test_2.txt") == 11048
    print(solution("day_16/data.txt"))

if __name__ == "__main__":
    main()