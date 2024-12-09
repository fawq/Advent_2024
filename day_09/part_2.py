from collections import deque
from dataclasses import dataclass
from pathlib import Path

from utils.load_file import File

@dataclass()
class Block:
    file_id: int
    start_index: int
    end_index: int
    length: int

def get_all_data(blocks: list[int]) -> tuple[list[Block], list[Block]]:
    number_blocks: list[Block] = []
    dot_blocks: list[Block] = []
    global_index: int = 0
    file_id: int = 0
    for index, block_length in enumerate(blocks):
        if index % 2 == 0:
            if block_length > 0:
                number_blocks.append(Block(file_id, global_index, global_index + block_length - 1, block_length))
            file_id += 1
        else:
            if block_length > 0:
                dot_blocks.append(Block(-1, global_index, global_index + block_length - 1, block_length))
        global_index += block_length

    return number_blocks, dot_blocks

def get_suitable_dot_block_index(dot_blocks: list[Block], size: int, max_index: int) -> int:
    for index, dot_block in enumerate(dot_blocks):
        if dot_block.start_index > max_index:
            return -1

        if dot_block.length >= size:
            return index
    return -1

def solution(file_path: Path) -> int:
    disk_map: str = ""

    for line in File(file_path).read():
        line = line.strip()
        if line == "":
            break

        disk_map = line

    blocks: list[int] = list(map(int, disk_map))
    number_blocks, dot_blocks = get_all_data(blocks)

    for number_block in reversed(number_blocks):
        suitable_dot_block_index = get_suitable_dot_block_index(dot_blocks, number_block.length, number_block.start_index)
        if suitable_dot_block_index != -1:
            dot_block = dot_blocks[suitable_dot_block_index]
            
            new_dot_block = Block(-1, number_block.start_index, number_block.end_index, number_block.length)
            number_block.start_index = dot_block.start_index
            number_block.end_index = dot_block.start_index + number_block.length - 1

            if number_block.length < dot_block.length:
                dot_block = Block(-1, dot_block.start_index + number_block.length, dot_block.end_index, dot_block.length - number_block.length)
                dot_blocks[suitable_dot_block_index] = dot_block
            else:
                dot_blocks.pop(suitable_dot_block_index)

            dot_blocks.append(new_dot_block)

    sorted_blocks: list[Block] = sorted(number_blocks + dot_blocks, key=lambda block: block.start_index)

    checksum: int = 0
    global_index: int = 0
    for block in sorted_blocks:
        for _ in range(block.length):
            if block.file_id != -1:
                checksum += block.file_id * global_index
            global_index += 1
    return checksum

def main() -> None:
    assert solution("day_09/data_test.txt") == 2858
    print(solution("day_09/data.txt"))

if __name__ == "__main__":
    main()