"""AOC 2024 - Day X"""

from lib.solution import Solution


class Day_1(Solution):
    def __init__(self, real: bool = False):
        self.real: bool = real
        super().__init__(1, False)

    def run(self):
        print(self.get_input())
