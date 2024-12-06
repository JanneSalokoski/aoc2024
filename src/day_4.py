"""AOC 2024 - Day 3"""

import re
import time

from lib.solution import Solution
from lib.timer import timer, timer_ns

DAY = 4
REAL = True


class CC:
    RED: str = "\033[91m"
    BLUE: str = "\033[94m"
    GREEN: str = "\033[92m"
    BOLD: str = "\033[1m"
    UNDER: str = "\033[4m"
    END: str = "\033[0m"

    CLEAR: str = "\033c"


def print_text(
    text: list[str],
    red: list[tuple[int, int]],
    blue: list[tuple[int, int]],
    green: list[tuple[int, int]],
    bold: list[tuple[int, int]],
    curr: tuple[int, int],
):
    height: int = len(text)
    width: int = len(text[0])

    for y in range(height - 1):
        for x in range(width):
            if (y, x) in bold:
                print(CC.BOLD, end="")

            if (y, x) == curr:
                print(CC.UNDER, end="")

            if (y, x) in red:
                print(CC.RED, end="")

            if (y, x) in blue:
                print(CC.BLUE, end="")

            if (y, x) in green:
                print(CC.GREEN, end="")


            print(text[y][x], end=" ")
            print(CC.END, end="")

        print()


# (y-3,x-3) (y-3,x-2) (y-3,x-1) (y-3, x ) (y-3,x+1) (y-3,x+2) (y-3,x+3)
# (y-2,x-3) (y-2,x-2) (y-2,x-1) (y-2, x ) (y-2,x+1) (y-2,x+2) (y-2,x+3)
# (y-1,x-3) (y-1,x-2) (y-1,x-1) (y-1, x ) (y-1,x+1) (y-1,x+2) (y-1,x+3)
# ( y ,x-3) ( y ,x-2) ( y ,x-1) ( y , x ) ( y ,x+1) ( y ,x+2) ( y ,x+3)
# (y+1,x-3) (y+1,x-2) (y+1,x-1) (y+1, x ) (y+1,x+1) (y+1,x+2) (y+1,x+3)
# (y+2,x-3) (y+2,x-2) (y+2,x-1) (y+2, x ) (y+2,x+1) (y+2,x+2) (y+2,x+3)
# (y+3,x-3) (y+3,x-2) (y+3,x-1) (y+3, x ) (y+3,x+1) (y+3,x+2) (y+3,x+3)


def get_lines(t: list[str], y: int, x: int, size: int) -> list[str]:
    res: list[str] = []

    if y >= 3:
        res.append(t[y][x] + t[y - 1][x] + t[y - 2][x] + t[y - 3][x])
    else:
        res.append("")

    if y >= 3 and x < size - 3:
        res.append(t[y][x] + t[y - 1][x + 1] + t[y - 2][x + 2] + t[y - 3][x + 3])
    else:
        res.append("")

    if x < size - 3:
        res.append(t[y][x] + t[y][x + 1] + t[y][x + 2] + t[y][x + 3])
    else:
        res.append("")

    if y < size - 3 and x < size - 3:
        res.append(t[y][x] + t[y + 1][x + 1] + t[y + 2][x + 2] + t[y + 3][x + 3])
    else:
        res.append("")

    if y < size - 3:
        res.append(t[y][x] + t[y + 1][x] + t[y + 2][x] + t[y + 3][x])
    else:
        res.append("")

    if y < size - 3 and x >= 3:
        res.append(t[y][x] + t[y + 1][x - 1] + t[y + 2][x - 2] + t[y + 3][x - 3])
    else:
        res.append("")

    if x >= 3:
        res.append(t[y][x] + t[y][x - 1] + t[y][x - 2] + t[y][x - 3])
    else:
        res.append("")

    if y >= 3 and x >= 3:
        res.append(t[y][x] + t[y - 1][x - 1] + t[y - 2][x - 2] + t[y - 3][x - 3])
    else:
        res.append("")

    return res


@timer
def p1_naive(t: list[str]) -> int:
    height: int = len(t)
    width: int = len(t[0])

    count: int = 0

    # red: list[tuple[int, int]] = []
    # blue: list[tuple[int, int]] = []
    # green: list[tuple[int, int]] = []
    # bold: list[tuple[int, int]] = []

    # print_text(t, red, blue, green, bold, (0, 0))

    for y in range(height - 1):
        for x in range(width):
            # blue = []
            # print(CC.CLEAR)
            if t[y][x] == "X":
                # red.append((y, x))
                #
                # blue.extend(((y - 1, x), (y - 2, x), (y - 3, x)))
                # blue.extend(((y - 1, x + 1), (y - 2, x + 2), (y - 3, x + 3)))
                # blue.extend(((y, x + 1), (y, x + 2), (y, x + 3)))
                # blue.extend(((y + 1, x + 1), (y + 2, x + 2), (y + 3, x + 3)))
                # blue.extend(((y + 1, x), (y + 2, x), (y + 3, x)))
                # blue.extend(((y + 1, x - 1), (y + 2, x - 2), (y + 3, x - 3)))
                # blue.extend(((y, x - 1), (y, x - 2), (y, x - 3)))
                # blue.extend(((y - 1, x - 1), (y - 2, x - 2), (y - 3, x - 3)))

                # idx = [
                #     (((y - 1, x), (y - 2, x), (y - 3, x))),
                #     (((y - 1, x + 1), (y - 2, x + 2), (y - 3, x + 3))),
                #     (((y, x + 1), (y, x + 2), (y, x + 3))),
                #     (((y + 1, x + 1), (y + 2, x + 2), (y + 3, x + 3))),
                #     (((y + 1, x), (y + 2, x), (y + 3, x))),
                #     (((y + 1, x - 1), (y + 2, x - 2), (y + 3, x - 3))),
                #     (((y, x - 1), (y, x - 2), (y, x - 3))),
                #     (((y - 1, x - 1), (y - 2, x - 2), (y - 3, x - 3))),
                # ]

                lines: list[str] = get_lines(t, y, x, width)
                for i, line in enumerate(lines):
                    if line == "XMAS":
                        count += 1
                        # bold.extend(idx[i])
                        # green.extend(idx[i])

            # print_text(t, red, blue, green, bold, (y, x))

    #         if t[y][x] == "X":
    #             time.sleep(0.5)
    #         else:
    #             time.sleep(0.1)

    return count


KERNELS: list[list[str]] = [
["M.S",
".A.",
"M.S,"],

["M.M",
".A.",
"S.S"],

["S.S",
".A.",
"M.M"],

["S.M",
".A.",
"S.M"],

#
#
# [".M.",
# "MAS",
# ".S."],
#
# [".S.",
# "SAM",
# ".M."],
#
# [".M.",
# "SAM",
# ".S."],
#
# [".S.",
# "MAS",
# ".M."],
# #
#
# ["MAS",
# "A..",
# "S.."],
#
# ["..M",
# "..A",
# "MAS"],
#
# ["MAS",
# "..A",
# "..M"],
#
# ["S..",
# "A..",
# "MAS"],
#
# ["SAM",
# "A..",
# "M.."],
#
# ["..S",
# "..A",
# "SAM"],
#
# ["SAM",
# "..A",
# "..S"],
#
# ["M..",
# "A..",
# "SAM"],
]

def kernel_matches(a: list[str], b: list[str]) -> bool:
    size: int = len(a)
    for y in range(size):
        for x in range(size):
            if a[y][x] == "." or b[y][x] == ".":
                continue
            elif a[y][x] != b[y][x]:
                return False

    return True


@timer
def p2_naive(t: list[str]) -> int:
    height: int = len(t)
    width: int = len(t[0])

    count: int = 0

    for y in range(1, height - 2):
        for x in range(1, width - 1):
            kernel: list[str] = [
                    t[y-1][x-1:x+2],
                    t[y][x-1:x+2],
                    t[y+1][x-1:x+2]
            ]

            for kern in KERNELS:
                if kernel_matches(kernel, kern):
                    count += 1

    return count


class Day_4(Solution):
    def __init__(self):
        super().__init__(DAY, REAL)

    def run(self):
        text = self.get_input()
        print(f"part 1, colors: {p1_naive(text)}")
        print(f"part 2, kernel: {p2_naive(text)}")

