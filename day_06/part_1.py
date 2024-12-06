import enum
from typing import Counter
from utils.load_file import File

class Direction(enum.Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)

def turn_right(direction: Direction) -> Direction:
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

    for row, line in enumerate(File("day_06/data.txt").read()):
        line = line.strip()
        if line == "":
            break

        if '^' in line:
            start_point = (row, line.index('^'))        
        matrix.append(list(line))

    direction: Direction = Direction.UP
    height: int = len(matrix)
    width: int = len(matrix[0])
    row, column = start_point
    while is_in_bounds(row + direction.value[0], column + direction.value[1], height, width):
        matrix[row][column] = 'X'

        if matrix[row + direction.value[0]][column + direction.value[1]] == '#':
            direction = turn_right(direction)
        else:
            row += direction.value[0]
            column += direction.value[1]
    matrix[row][column] = 'X'

    count_elements: Counter[int] = Counter()
    for row in matrix:
        count_elements.update(row)

    print(count_elements['X'])

if __name__ == "__main__":
    main()