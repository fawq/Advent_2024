from pathlib import Path
from typing import Optional

from advent.utils.load_file import File

def fill_key_or_lock(key_or_lock: tuple[int, int, int, int, int], line: str) -> tuple[int, int, int, int, int]:
    new_additional_key_or_lock: list[int] = [] 
    for character in line:
        if character == "#":
            new_additional_key_or_lock.append(1)
        else:
            new_additional_key_or_lock.append(0)
    return (key_or_lock[0] + new_additional_key_or_lock[0],
            key_or_lock[1] + new_additional_key_or_lock[1],
            key_or_lock[2] + new_additional_key_or_lock[2],
            key_or_lock[3] + new_additional_key_or_lock[3],
            key_or_lock[4] + new_additional_key_or_lock[4])

def check_overlap(key: tuple[int, int, int, int, int], lock: tuple[int, int, int, int, int], max_overlap: int = 7) -> bool:
    for i in range(5):
        if key[i] + lock[i] > max_overlap:
            return True
    return False

def part1_solution(file_path: Path) -> int:
    next_key_or_lock: bool = True
    actual_key_or_lock: tuple[int, int, int, int, int] = (0, 0, 0, 0, 0)
    is_key: Optional[bool] = None

    keys: set[tuple[int, int, int, int, int]] = set()
    locks: set[tuple[int, int, int, int, int]] = set()
    
    for line in File(file_path).read():
        line = line.strip()
        if line == "":
            next_key_or_lock = True
            continue

        if next_key_or_lock:
            next_key_or_lock = False
            if is_key is not None:
                if is_key:
                    keys.add(actual_key_or_lock)
                else:
                    locks.add(actual_key_or_lock)
            
            actual_key_or_lock = (0, 0, 0, 0, 0)
            if line == "#####":
                is_key = False
            else:
                is_key = True
        actual_key_or_lock = fill_key_or_lock(actual_key_or_lock, line)
    else:
        if is_key:
            keys.add(actual_key_or_lock)
        else:
            locks.add(actual_key_or_lock)

    founded_pairs: int = 0
    for key in keys:
        for lock in locks:
            if not check_overlap(key, lock):
                founded_pairs += 1

    return founded_pairs

def main() -> None:
    assert part1_solution("src/advent/day_25/data_test.txt") == 3
    print(f"Part 1: {part1_solution("src/advent/day_25/data.txt")}")