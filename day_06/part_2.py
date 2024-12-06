import enum
from typing import Counter
from utils.load_file import File

class Direction(enum.Enum):
    UP = (-1, 0, '^')
    RIGHT = (0, 1, '>')
    DOWN = (1, 0, 'v')
    LEFT = (0, -1, '<')

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
                row, column = start_point
                direction: Direction = Direction.UP
                visited_places: set[tuple[int, int, Direction]] = set()
                matrix[index_x][index_y] = '#'
                while is_in_bounds(row + direction.value[0], column + direction.value[1], height, width):
                    if (row, column, direction) in visited_places:
                        guards_count += 1
                        break
                    visited_places.add((row, column, direction))

                    if matrix[row + direction.value[0]][column + direction.value[1]] == '#':
                        direction = direction_on_right(direction)
                    else:
                        row += direction.value[0]
                        column += direction.value[1]
                matrix[index_x][index_y] = '.'
    print(guards_count)

if __name__ == "__main__":
    main()