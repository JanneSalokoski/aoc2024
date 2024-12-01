"""lib/input.py

Read input from file
"""


class Reader:
    def __init__(self, day: int, real: bool = False):
        self.day: int = day
        self.real: bool = real

    def read_file(self):
        input_type: str = "real" if self.real else "example"
        filename: str = f"inputs/day-{self.day}/{input_type}.txt"

        with open(filename, "r") as f:
            return f.read()

    def read_lines(self):
        return self.read_file().split("\n")
