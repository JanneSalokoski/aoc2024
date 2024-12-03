"""AOC 2024 - Day 2"""

from lib.solution import Solution
from lib.timer import timer, timer_ns

DAY = 2
REAL = True


runs = 0


def is_safe(levels: list[int]) -> bool:
    global runs
    runs += 1
    descending: bool = levels[0] > levels[1]
    for i in range(1, len(levels)):
        if abs(levels[i] - levels[i - 1]) > 3:
            return False

        if levels[i - 1] == levels[i]:
            return False

        if descending:
            if levels[i - 1] < levels[i]:
                return False
        else:
            if levels[i - 1] > levels[i]:
                return False

    return True


@timer
def p2_naive(text: list[str]):
    count: int = 0
    for report in text:
        levels: list[int] = [int(x) for x in report.split()]
        for i in range(len(levels)):
            lev = levels.copy()
            _ = lev.pop(i)
            if is_safe(lev):
                count += 1
                break

    return count


@timer
def p1_naive(text: list[str]):
    count: int = 0
    for report in text:
        levels: list[int] = [int(x) for x in report.split()]
        if is_safe(levels):
            count += 1

    return count


class Day_2(Solution):
    def __init__(self):
        super().__init__(DAY, REAL)

    def run(self):
        global runs

        text = self.get_input()[:-1]
        print(f"part 1, naive: {p1_naive(text)}")

        print(f"runs: {runs}")
        runs = 0

        print(f"part 2, naive: {p2_naive(text)}")
        print(f"runs: {runs}")
