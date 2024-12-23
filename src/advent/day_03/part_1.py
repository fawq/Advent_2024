import re
from utils.load_file import File

MUL_PATTERN = re.compile(r"mul\((?P<first_number>\d{1,3}),(?P<second_number>\d{1,3})\)")

def main() -> None:
    sum_of_muls: int = 0

    for line in File("day_03/data.txt").read():
        line = line.strip()
        if line == "":
            break

        muls = MUL_PATTERN.finditer(line)
        for mul in muls:
            sum_of_muls += int(mul["first_number"]) * int(mul["second_number"])

    print(sum_of_muls)

if __name__ == "__main__":
    main()