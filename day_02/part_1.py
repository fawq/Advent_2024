from utils.load_file import File

def is_safe(levels: list[int]) -> bool:
    monotonic: str = ""
    
    for i in range(1, len(levels)):
        if levels[i - 1] < levels[i]:
            if monotonic == "decreasing":
                return False
            monotonic = "increasing"
        elif levels[i - 1] > levels[i]:
            if monotonic == "increasing":
                return False
            monotonic = "decreasing"
        else:
            return False
        
        if abs(levels[i - 1] - levels[i]) > 3:
            return False
    return True

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