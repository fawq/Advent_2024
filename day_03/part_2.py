import re
from utils.load_file import File

MUL_PATTERN = re.compile(r"mul\((?P<first_number>\d{1,3}),(?P<second_number>\d{1,3})\)")

def get_segments(line: str, split_by: str = "don't()") -> list[str]:
    splitted_segments = line.split(split_by, maxsplit=1)
    if len(splitted_segments) == 1:
        return [splitted_segments[0]]
    return [splitted_segments[0]] + get_segments(splitted_segments[1], "do()" if split_by == "don't()" else "don't()")

def main() -> None:
    sum_of_muls: int = 0
    is_countable: bool = True
    lines: list[str] = []

    for line in File("day_03/data.txt").read():
        line = line.strip()
        if line == "":
            break
        lines.append(line)

    segments: list[str] = get_segments(" ".join(lines))
    for segment in segments:
        if not is_countable:
            is_countable = True
            continue

        muls = MUL_PATTERN.finditer(segment)
        for mul in muls:
            sum_of_muls += int(mul["first_number"]) * int(mul["second_number"])
        is_countable = False

    print(sum_of_muls)

if __name__ == "__main__":
    main()