from collections import defaultdict
from enum import Enum
from utils.load_file import File

class Order(Enum):
    BEFORE = "before"
    AFTER = "after"
    SAME = "same"

def check_if_ordered(line: list[int], order_connections: defaultdict[tuple[int, int], Order]) -> bool:
    for i in range(len(line) - 1):
        for j in range(i + 1, len(line)):
            if order_connections[(line[i], line[j])] == Order.AFTER:
                return False
    return True

def update_ordered_line(number: int, line: list[int], order_connections: defaultdict[tuple[int, int], Order]) -> list[int]:
    last_index_before: int = len(line)
    for i in reversed(range(len(line))):
        if order_connections[(number, line[i])] == Order.BEFORE:
            last_index_before = i
    return line[:last_index_before] + [number] + line[last_index_before:]

def main() -> None:
    order_connections: defaultdict[tuple[int, int], Order] = defaultdict(lambda: Order.SAME)
    lines: list[list[int]] = []
    sum_of_middles: int = 0

    for line in File("day_05/data_2.txt").read():
        line = line.strip()
        if line == "":
            break
        
        lines.append(list(map(int, line.split(","))))

    for line in File("day_05/data_1.txt").read():
        line = line.strip()
        if line == "":
            break
        
        x, y = map(int, line.split("|"))
        order_connections[(x, y)] = Order.BEFORE
        order_connections[(y, x)] = Order.AFTER

    for line in lines:
        if not check_if_ordered(line, order_connections):
            new_line: list[int] = []
            for number in line:
                new_line = update_ordered_line(number, new_line, order_connections)
            sum_of_middles += new_line[len(new_line) // 2]
    
    print(sum_of_middles)

if __name__ == "__main__":
    main()