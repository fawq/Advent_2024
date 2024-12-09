from collections import deque
from pathlib import Path

from utils.load_file import File

def get_disk_map_flat(blocks: list[int]) -> list[str | int]:
    disk_map_flat: list[str | int] = []
    file_id: int = 0
    for index, block_length in enumerate(blocks):
        if index % 2 == 0:
            if block_length > 0:
                disk_map_flat.extend([file_id] * block_length)
            file_id += 1
        else:
            if block_length > 0:
                disk_map_flat.extend(['.'] * block_length)

    return disk_map_flat

def solution(file_path: Path) -> int:
    disk_map: str = ""

    for line in File(file_path).read():
        line = line.strip()
        if line == "":
            break

        disk_map = line

    blocks: list[int] = list(map(int, disk_map))
    disk_map_flat: list[str | int] = get_disk_map_flat(blocks)
    disk_deque: deque[str | int] = deque(disk_map_flat)

    while True:
        try:
            first_index_of_dot: int = disk_deque.index('.')
        except ValueError:
            break

        block_on_the_last_index: int = disk_deque.pop()
        while block_on_the_last_index == '.':
            block_on_the_last_index = disk_deque.pop()

        disk_deque[first_index_of_dot] = block_on_the_last_index

    checksum: int = 0
    for index, block in enumerate(disk_deque):
        if block != '.':
            checksum += index * block

    return checksum

def main() -> None:
    assert solution("day_09/data_test.txt") == 1928
    print(solution("day_09/data.txt"))

if __name__ == "__main__":
    main()