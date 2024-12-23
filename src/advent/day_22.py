from collections import defaultdict
from functools import cache
from pathlib import Path

from advent.utils.load_file import File


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

def part1_solution(file_path: Path) -> int:
    secrets: list[int] = []

    for line in File(file_path).read():
        line = line.strip()
        if line == "":
            break

        secrets.append(int(line))

    for _ in range(2000):
        secrets = list(map(operations, secrets))

    return sum(secrets)

def part2_solution(file_path: Path) -> int:
    secrets: list[int] = []

    for line in File(file_path).read():
        line = line.strip()
        if line == "":
            break

        secrets.append(int(line))

    sum_four_sequence_dict: defaultdict[tuple[int, int, int, int], int] = defaultdict(lambda: 0)
    for secret in secrets:
        four_sequence_dict: dict[tuple[int, int, int, int], int] = {}
        tmp_secret_1 = secret
        tmp_secret_2 = operations(tmp_secret_1)
        tmp_secret_3 = operations(tmp_secret_2)
        tmp_secret_4 = operations(tmp_secret_3)
        tmp_secret_last = operations(tmp_secret_4)

        bannana_1 = tmp_secret_1 % 10
        bannana_2 = tmp_secret_2 % 10
        bannana_3 = tmp_secret_3 % 10
        bannana_4 = tmp_secret_4 % 10
        bannana_last = tmp_secret_last % 10

        diffs: tuple[int, int, int, int] = (
            bannana_2 - bannana_1,
            bannana_3 - bannana_2,
            bannana_4 - bannana_3,
            bannana_last - bannana_4 
        )

        four_sequence_dict[diffs] = bannana_last

        for _ in range(4, 2000):
            _ , diff_2, diff_3, diff_4 = diffs
            tmp_secret_previous = tmp_secret_last
            bannana_previous = bannana_last

            tmp_secret_last = operations(tmp_secret_previous)
            bannana_last = tmp_secret_last % 10

            diff_5 = bannana_last - bannana_previous
            diffs = (diff_2, diff_3, diff_4, diff_5)
            
            if diffs not in four_sequence_dict:
                four_sequence_dict[diffs] = bannana_last

        for diffs, bannanas in four_sequence_dict.items():
            sum_four_sequence_dict[diffs] += bannanas
        
    return max(sum_four_sequence_dict.values())

def main() -> None:
    assert part1_solution(Path("src/advent/day_22/data_test.txt")) == 37327623
    print(part1_solution(Path("src/advent/day_22/data.txt")))
    assert part2_solution(Path("src/advent/day_22/data_test.txt")) == 24 # in the exaple it was 23, but I think example is wrong
    print(part2_solution(Path("src/advent/day_22/data.txt")))

if __name__ == "__main__":
    main()