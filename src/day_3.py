"""AOC 2024 - Day 3"""

import re

from lib.solution import Solution
from lib.timer import timer, timer_ns

DAY = 3
REAL = True


@timer
def p1_naive(text: str) -> int:
    pattern: re.Pattern[str] = re.compile(r"mul\((\d+?),(\d+?)\)")
    instructions: list[str] = re.findall(pattern, text)
    pairs: list[tuple[int, int]] = [(int(a), int(b)) for a, b in instructions]
    sums: list[int] = [a * b for a, b in pairs]
    return sum(sums)


@timer
def p1_alloc_less(text: str) -> int:
    pattern: re.Pattern[str] = re.compile(r"mul\((\d+?),(\d+?)\)")
    return sum([int(a) * int(b) for a, b in re.findall(pattern, text)])


@timer
def p1_no_regex(text: str) -> int:
    length: int = len(text)

    numbers: str = "0123456789"
    reading_first_number: bool = False
    reading_second_number: bool = False
    number1: str = ""
    number2: str = ""

    count: int = 0

    for i in range(4, length - 1):
        buff = text[i - 3 : i + 1]
        if buff == "mul(":
            reading_first_number = True
            continue

        c: str = text[i]
        if reading_first_number:
            if c in numbers:
                number1 += c
                continue
            elif c == ",":
                reading_first_number = False
                reading_second_number = True
                continue
            else:
                reading_first_number = False
                number1 = ""
                continue

        if reading_second_number:
            if c in numbers:
                number2 += c
                continue
            elif c == ")":
                # print(number1, " ", number2)
                reading_second_number = False
                count += int(number1) * int(number2)
                number1 = ""
                number2 = ""
                continue
            else:
                reading_first_number = False
                reading_second_number = False
                number1 = ""
                number2 = ""
                continue

    return count


re_pairs = []
no_pairs = []


@timer
def p2_naive(text: str) -> int:
    inst_pat: re.Pattern[str] = re.compile(r"mul\((\d+?),(\d+?)\)")
    do_pat: re.Pattern[str] = re.compile(r"(?:do\(\)|^)(.*?)(?:don't\(\)|$)")

    do_blocks: list[str] = re.findall(do_pat, text)
    counter: int = 0
    for block in do_blocks:
        pairs = [(int(a), int(b)) for a, b in re.findall(inst_pat, block)]
        # print(pairs)
        global re_pairs
        for pair in pairs:
            re_pairs.append(pair)

        counter += sum([int(a) * int(b) for a, b in re.findall(inst_pat, block)])

    return counter


@timer
def p2_no_regex(text: str) -> int:
    length: int = len(text)

    numbers: str = "0123456789"
    reading_first_number: bool = False
    reading_second_number: bool = False
    number1: str = ""
    number2: str = ""

    in_do: bool = True

    count: int = 0

    for i in range(4, length - 1):
        if in_do:
            if i > 7 and text[i - 6 : i + 1] == "don't()":
                in_do = False
                continue

            buff = text[i - 3 : i + 1]
            if buff == "mul(":
                reading_first_number = True
                continue

            c: str = text[i]
            if reading_first_number:
                if c in numbers:
                    number1 += c
                    continue
                elif c == ",":
                    reading_first_number = False
                    reading_second_number = True
                    continue
                else:
                    reading_first_number = False
                    number1 = ""
                    continue

            if reading_second_number:
                if c in numbers:
                    number2 += c
                    continue
                elif c == ")":
                    # print(number1, " ", number2)
                    global no_pairs
                    no_pairs.append((int(number1), int(number2)))
                    reading_second_number = False
                    count += int(number1) * int(number2)
                    number1 = ""
                    number2 = ""
                    continue
                else:
                    reading_first_number = False
                    reading_second_number = False
                    number1 = ""
                    number2 = ""
                    continue
        else:
            if i > 4 and text[i - 3 : i + 1] == "do()":
                in_do = True
                continue

    return count


class Day_3(Solution):
    def __init__(self):
        super().__init__(DAY, REAL)

    def run(self):
        text = self.get_raw()
        # print(f"part 1, naive: {p1_naive(text)}")
        # print(f"part 1, alloc less: {p1_alloc_less(text)}")
        # print(f"part 1, no regex: {p1_no_regex(text)}")

        print(f"part 2, naive: {p2_naive(text)}")
        print(f"part 2, no_regex: {p2_no_regex(text)}")

        # for i in range(len(no_pairs)):
        # print(f"{re_pairs[i]}\t{no_pairs[i]}\t{re_pairs[i]==no_pairs[i]}")
