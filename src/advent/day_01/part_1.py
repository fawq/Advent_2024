from utils.load_file import File

def main() -> None:
    location_right: list[int] = []
    location_left: list[int] = []
    sum: int = 0

    for line in File("day_01/data.txt").read():
        line = line.strip()
        if line == "":
            break
        left, right = map(int, line.split())
        location_right.append(right)
        location_left.append(left)
    
    location_right.sort()
    location_left.sort()

    for right, left in zip(location_right, location_left):
        sum += abs(right - left)

    print(sum)        

if __name__ == "__main__":
    main()