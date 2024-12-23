from utils.load_file import File

def is_increasing(levels: list[int], max_errors: int = 1) -> bool:
    for i in range(1, len(levels)):
        if levels[i - 1] >= levels[i] or levels[i] - levels[i - 1] > 3:
            if max_errors == 0:
                return False
            return is_increasing(levels[:i] + levels[i + 1:], 0) or is_increasing(levels[:i - 1] + levels[i:], 0)
    return True

def is_decreasing(levels: list[int], max_errors: int = 1) -> bool:
    for i in range(1, len(levels)):
        if levels[i - 1] <= levels[i] or levels[i - 1] - levels[i] > 3:
            if max_errors == 0:
                return False
            return is_decreasing(levels[:i] + levels[i + 1:], 0) or is_decreasing(levels[:i - 1] + levels[i:], 0)
    return True

def is_safe(levels: list[int]) -> bool:
    return is_increasing(levels) or is_decreasing(levels) 

def main() -> None:
    count_safe: int = 0

    for line in File("day_02/data.txt").read():
        line = line.strip()
        if line == "":
            break
        
        levels: list[int] = list(map(int, line.split()))
        if is_safe(levels):
            count_safe += 1

    print(count_safe)

if __name__ == "__main__":
    main()