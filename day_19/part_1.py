from functools import cache
from pathlib import Path

from utils.load_file import File

@cache
def is_possible_to_do_stripe(word: str, stripes: frozenset[str]) -> bool:
    if word in stripes:
        return True
    
    for index in range(1, len(word)):
        first_word = word[:index]
        second_word = word[index:]
        is_possible_first_word = is_possible_to_do_stripe(first_word, stripes)
        is_possible_second_word = is_possible_to_do_stripe(second_word, stripes)
        if is_possible_first_word and is_possible_second_word:
            return True

    return False

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

    count_possible: int = 0
    for word in words:
        if is_possible_to_do_stripe(word, stripes):
            count_possible += 1

    return count_possible

def main() -> None:
    assert solution("day_19/data_test.txt") == 6
    print(solution("day_19/data.txt"))

if __name__ == "__main__":
    main()

