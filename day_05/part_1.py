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
        if check_if_ordered(line, order_connections):
            sum_of_middles += line[len(line) // 2]
    
    print(sum_of_middles)

if __name__ == "__main__":
    main()