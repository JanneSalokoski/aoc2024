"""AOC 2024 - Day X"""

from lib.solution import Solution
from lib.timer import timer, timer_ns

DAY = 1
REAL = True


@timer_ns
def p1_naive(text: list[str]):
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

    total = 0
    for pair in comb:
        total += max(pair) - min(pair)

    return total


@timer_ns
def p1_just_sum(text: list[str]):
    sum_1: int = 0
    sum_2: int = 0

    for line in text:
        parts: list[str] = line.split(" ")
        sum_1 += int(parts[0])
        sum_2 += int(parts[-1])

    return abs(sum_2 - sum_1)


@timer_ns
def p2_naive(text: list[str]) -> int:
    list_1: list[int] = []
    list_2: dict[int, int] = {}

    for line in text:
        parts: list[str] = line.split(" ")
        a: int = int(parts[0])
        b: int = int(parts[-1])

        list_1.append(a)

        if b in list_2:
            list_2[b] += 1
        else:
            list_2[b] = 1

    total: int = 0
    for x in list_1:
        if x in list_2:
            total += x * list_2[x]

    return total


class Day_1(Solution):
    def __init__(self):
        super().__init__(DAY, REAL)

    def run(self):
        text = self.get_input()[:-1]
        # print(f"part 1, naive: {p1_naive(text)}")
        # print(f"part 1, advanced: {p1_just_sum(text)}")

        print(f"part 2, naive: {p2_naive(text)}")
