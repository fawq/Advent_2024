from functools import cache
from pathlib import Path

from utils.load_file import File

@cache
def count_possible_ways_to_do_stripe(word: str, stripes: frozenset[str]) -> int:
    count_all_possibilities: int = 0
    
    if word != "":
        for stripe in stripes:
            if word.startswith(stripe):
                count_all_possibilities += count_possible_ways_to_do_stripe(word[len(stripe):], stripes)
        return count_all_possibilities
    return 1

def solution(file_path: Path) -> int:
    stripes: frozenset[str] = frozenset()
    words: list[str] = []
    is_data: bool = False

    for line in File(file_path).read():
        line = line.strip()
        if line == "":
            is_data = True
            continue
        
        if not is_data:
            stripes = frozenset(line.split(", "))
        else:
            words.append(line)

    count_possible_ways: int = 0
    for word in words:
        count_possible_ways += count_possible_ways_to_do_stripe(word, stripes)

    return count_possible_ways

def main() -> None:
    assert solution("day_19/data_test.txt") == 16
    print(solution("day_19/data.txt"))

if __name__ == "__main__":
    main()
