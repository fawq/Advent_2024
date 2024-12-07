from dataclasses import dataclass
import enum
from typing import Counter
from utils.load_file import File

@dataclass
class Vector:
    add_row: int
    add_column: int
    symbol: str

class Direction(enum.Enum):
    UP = Vector(-1, 0, '^')
    RIGHT = Vector(0, 1, '>')
    DOWN = Vector(1, 0, 'v')
    LEFT = Vector(0, -1, '<')

def direction_on_right(direction: Direction) -> Direction:
    match direction:
        case Direction.UP:
            return Direction.RIGHT
        case Direction.RIGHT:
            return Direction.DOWN
        case Direction.DOWN:
            return Direction.LEFT
        case Direction.LEFT:
            return Direction.UP
        
def next_position(row: int, column: int, direction: Direction) -> tuple[int, int]:
    return row + direction.value.add_row, column + direction.value.add_column
        
def is_in_bounds(row: int, column: int, height: int, width: int) -> bool:
    return row >= 0 and row < height and column >= 0 and column < width

def main() -> None:
    matrix: list[list[str]] = []
    start_point: tuple[int, int] = (-1, -1)
    guards_count: int = 0

    for row, line in enumerate(File("day_06/data.txt").read()):
        line = line.strip()
        if line == "":
            break

        if '^' in line:
            start_point = (row, line.index('^'))        
        matrix.append(list(line))

    height: int = len(matrix)
    width: int = len(matrix[0])
    for index_x in range(height):
        for index_y in range(width):
            if matrix[index_x][index_y] == '.':
                direction: Direction = Direction.UP
                visited_places: set[tuple[int, int, Direction]] = set()
                matrix[index_x][index_y] = '#'
                
                row, column = start_point
                next_row, next_column = next_position(row, column, direction)
                while is_in_bounds(next_row, next_column, height, width):
                    if (row, column, direction) in visited_places:
                        guards_count += 1
                        break
                    visited_places.add((row, column, direction))

                    if matrix[next_row][next_column] == '#':
                        direction = direction_on_right(direction)
                    else:
                        row = next_row
                        column = next_column
                    
                    next_row, next_column = next_position(row, column, direction)
                
                matrix[index_x][index_y] = '.'
    print(guards_count)

if __name__ == "__main__":
    main()