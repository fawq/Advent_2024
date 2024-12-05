from collections import Counter

from utils.load_file import File

def main() -> None:
    location_right: Counter[int] = Counter()
    location_left: list[int] = []
    similaritiy_score: int = 0

    for line in File("day_01/data.txt").read():
        line = line.strip()
        if line == "":
            break
        left, right = map(int, line.split())
        location_right.update([right])
        location_left.append(left)

    for left in location_left:
        similaritiy_score += left * location_right[left]

    print(similaritiy_score)

if __name__ == "__main__":
    main()