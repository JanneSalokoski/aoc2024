"""AOC 2024 - Day X"""

from lib.solution import Solution

DAY = 1
REAL = True


class Day_1(Solution):
    def __init__(self):
        super().__init__(DAY, REAL)

    def run(self):
        text = self.get_input()[:-1]

        list_1: list[int] = []
        list_2: list[int] = []

        for line in text:
            parts: list[str] = line.split(" ")
            a: int = int(parts[0])
            b: int = int(parts[-1])

            list_1.append(a)
            list_2.append(b)

        list_1.sort()
        list_2.sort()

        comb: list[tuple[int, int]] = list(zip(list_1, list_2))
        print(comb)

        total = 0
        for pair in comb:
            total += max(pair) - min(pair)

        print(total)
