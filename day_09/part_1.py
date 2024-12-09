from itertools import zip_longest
from pathlib import Path
from typing import Iterable

from utils.load_file import File

def get_splitted_blocks(blocks: list[int]) -> tuple[list[int], list[int]]:
    number_blocks: list[int] = []
    dot_blocks: list[int] = []

    for index, block_length in enumerate(blocks):
        if index % 2 == 0:
            number_blocks.append(block_length)
        else:
            dot_blocks.append(block_length)

    return number_blocks, dot_blocks

def iterate_next_number(number_blocks: list[int]) -> Iterable[int]:
    file_id: int = 0
    for number_block in number_blocks:
        for _ in range(number_block):
            yield file_id
        file_id += 1

def iterate_previous_number(number_blocks: list[int]) -> Iterable[int]:
    file_id: int = len(number_blocks) - 1
    for number_block in reversed(number_blocks):
        for _ in range(number_block):
            yield file_id
        file_id -= 1

def solution(file_path: Path) -> int:
    disk_map: str = ""

    for line in File(file_path).read():
        line = line.strip()
        if line == "":
            break

        disk_map = line

    blocks: list[int] = list(map(int, disk_map))
    number_blocks, dot_blocks = get_splitted_blocks(blocks)
    max_number_index: int = sum(number_blocks)

    checksum: int = 0
    index: int = 0
    next_iterator: Iterable[int] = iterate_next_number(number_blocks)
    previous_iterator: Iterable[int] = iterate_previous_number(number_blocks)
    for number_block_len, dot_block_len in zip_longest(number_blocks, dot_blocks, fillvalue=0):
        for _ in range(number_block_len):
            if index >= max_number_index:
                return checksum
            file_id = next(next_iterator)
            checksum += file_id * index
            index += 1
        
        for _ in range(dot_block_len):
            if index >= max_number_index:
                return checksum
            file_id = next(previous_iterator)
            checksum += file_id * index
            index += 1
    # Probably not possible to reach but if dot blocks would be with only 0 lengths values then this return should be reached
    return checksum

def main() -> None:
    assert solution("day_09/data_test.txt") == 1928
    print(solution("day_09/data.txt"))

if __name__ == "__main__":
    main()