from functools import cache
from pathlib import Path

from utils.load_file import File


@cache
def mix_and_prune(secret: int, number: int) -> int:
    PRUNE_PROCESS_AND: int = 16777215 # it is 2 to power 24 - 1. Exactly -1 from original modulo

    secret ^= number
    secret &= PRUNE_PROCESS_AND # it is the same as modulo but faster for powers of 2
    return secret

@cache
def operations(secret: int) -> int:
    FIRST_PROCESS_SHIFT: int = 6 # the same as * 64
    SECOND_PROCESS_SHIFT: int = 5 # the same as / 32
    THIRD_PROCESS_SHIFT: int = 11 # the same as * 2048

    first_number: int = (secret << FIRST_PROCESS_SHIFT)
    secret = mix_and_prune(secret, first_number)

    second_number: int = (secret >> SECOND_PROCESS_SHIFT)
    secret = mix_and_prune(secret, second_number)

    third_number: int = (secret << THIRD_PROCESS_SHIFT)
    secret = mix_and_prune(secret, third_number)

    return secret

def solution(file_path: Path) -> int:
    secrets: list[int] = []

    for line in File(file_path).read():
        line = line.strip()
        if line == "":
            break

        secrets.append(int(line))

    for _ in range(2000):
        secrets = list(map(operations, secrets))

    return sum(secrets)

if __name__ == "__main__":
    assert solution(Path("day_22/data_test.txt")) == 37327623
    print(solution(Path("day_22/data.txt")))
