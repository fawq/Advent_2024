from pathlib import Path

class File:
    def __init__(self, path: Path):
        self.path = path

    def read(self) -> list[str]:
        with open(self.path, 'r') as file:
            return file.readlines()