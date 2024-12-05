from utils.load_file import File

def get_horizontal(lines: list[str]) -> list[str]:
    horizontal_lines: list[str] = []

    for column in range(len(lines[0])):
        line: str = ""
        for row in range(len(lines)):
            line += lines[row][column]
        horizontal_lines.append(line.strip())

    return horizontal_lines

def get_xmas(lines: list[str]) -> int:
    occurence: int = 0
    for line in lines:
        occurence += line.count("XMAS")
        occurence += line.count("SAMX")

    return occurence

def main() -> None:
    count_valid: int = 0
    vertical_lines: list[str] = []
    dummy_diagonal_up: list[str] = []
    dummy_diagonal_down: list[str] = []

    for line in File("day_04/data.txt").read():
        line = line.strip()
        if line == "":
            break
        
        vertical_lines.append(line)

    horizontal_lines: list[str] = get_horizontal(vertical_lines)
    
    for index in range(len(vertical_lines)):
        dummy_diagonal_up.append(" " * (len(vertical_lines) - index - 1) + vertical_lines[index] + " " * index)
    diagonal_up: list[str] = get_horizontal(dummy_diagonal_up)

    for index in range(len(vertical_lines)):
        dummy_diagonal_down.append(" " * index + vertical_lines[index] + " " * (len(vertical_lines) - index - 1)) 
    diagonal_down: list[str] = get_horizontal(dummy_diagonal_down)

    count_valid += get_xmas(vertical_lines)
    count_valid += get_xmas(horizontal_lines)
    count_valid += get_xmas(diagonal_up)
    count_valid += get_xmas(diagonal_down)

    print(count_valid)

if __name__ == "__main__":
    main()