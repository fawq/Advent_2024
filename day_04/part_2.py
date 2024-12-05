from utils.load_file import File

def main() -> None:
    count_valid: int = 0
    vertical_lines: list[str] = []

    for line in File("day_04/data.txt").read():
        line = line.strip()
        if line == "":
            break
        
        vertical_lines.append(line)

    for row in range(len(vertical_lines) - 2):
        for col in range(len(vertical_lines[0]) - 2):
            if vertical_lines[row][col] == "M":
                if vertical_lines[row + 2][col] == "M":
                    if vertical_lines[row][col + 2] == "S" and vertical_lines[row + 2][col + 2] == "S" and vertical_lines[row + 1][col + 1] == "A":
                        count_valid += 1
                elif vertical_lines[row + 2][col] == "S":
                    if vertical_lines[row][col + 2] == "M" and vertical_lines[row + 2][col + 2] == "S" and vertical_lines[row + 1][col + 1] == "A":
                        count_valid += 1
            elif vertical_lines[row][col] == "S":
                if vertical_lines[row + 2][col] == "M":
                    if vertical_lines[row][col + 2] == "S" and vertical_lines[row + 2][col + 2] == "M" and vertical_lines[row + 1][col + 1] == "A":
                        count_valid += 1
                elif vertical_lines[row + 2][col] == "S":
                    if vertical_lines[row][col + 2] == "M" and vertical_lines[row + 2][col + 2] == "M" and vertical_lines[row + 1][col + 1] == "A":
                        count_valid += 1

    print(count_valid)

if __name__ == "__main__":
    main()