from dataclasses import dataclass
from enum import Enum
from itertools import combinations
from pathlib import Path
from queue import Queue

from advent.utils.load_file import File
from advent.utils.matrix import Matrix
from advent.utils.position import Direction, Position, PositionCost


class Element(Enum):
    WALL = "#"
    TRACK = "."
    START = "S"
    END = "E"
    PLAYER = "P"

    def is_valid(self) -> bool:
        return self in [self.TRACK, self.START, self.END]

@dataclass
class NewMatrix(Matrix[Element]):
    def get_neighbors(self, position: Position) -> list[Position]:
        neighbors: list[Position] = []
        for direction in Direction:
            next_position = position.next_position(direction)
            if self.get_element(next_position).is_valid():
                neighbors.append(next_position)
        return neighbors

def bfs_with_visited_positions(matrix: NewMatrix, start_position: Position, end_position: Position) -> list[PositionCost]:
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

def solution(file_path: Path, max_taxicab_distance: int, min_gain: int) -> int:
    matrix = NewMatrix()
    start_position: Position = Position(-1, -1)
    end_position: Position = Position(-1, -1)

    for line in File(file_path).read():
        line = line.strip()
        if line == "":
            break

        if "S" in line:
            start_position = Position(matrix.get_height(), line.index("S"))
        if "E" in line:
            end_position = Position(matrix.get_height(), line.index("E"))

        matrix.add_row(list(map(Element, line)))

    all_position_costs = bfs_with_visited_positions(matrix, start_position, end_position)
    cheats: int = 0
    for position_cost_1, position_cost_2 in combinations(all_position_costs, 2):
        first_position = position_cost_1.position
        first_position_distance = position_cost_1.distance

        second_position = position_cost_2.position
        second_position_distance = position_cost_2.distance

        taxicab_distance = first_position.vector_to(second_position).get_taxicab_distance()

        if (2 <= taxicab_distance <= max_taxicab_distance and 
            abs(first_position_distance - second_position_distance) - taxicab_distance >= min_gain):
            cheats += 1
    return cheats

def part1_solution(file_path: Path, min_gain: int = 100) -> int:
    return solution(file_path, 2, min_gain)

def part2_solution(file_path: Path, min_gain: int = 100) -> int:
    return solution(file_path, 20, min_gain)

def main() -> None:
    assert part1_solution(Path("src/advent/day_20/data_test.txt"), 20) == 5
    print(part1_solution(Path("src/advent/day_20/data.txt")))
    assert part2_solution(Path("src/advent/day_20/data_test.txt"), 74) == 7
    print(part2_solution(Path("src/advent/day_20/data.txt")))

if __name__ == "__main__":
    main()