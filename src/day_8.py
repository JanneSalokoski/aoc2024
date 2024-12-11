"""AOC 2024 - Day 8"""

from __future__ import annotations

import itertools
import math
import re
import time
from concurrent.futures import (ProcessPoolExecutor, ThreadPoolExecutor,
                                as_completed)
from dataclasses import dataclass
from enum import Enum
from itertools import product

import lib.colors as colors
from lib.solution import Solution
from lib.timer import timer, timer_ns

DAY = 8
REAL = True


@dataclass
class Point:
    x: int
    y: int

    def d_x(self, other: Point) -> int:
        return max(self.x, other.x) - min(self.x, other.x)

    def d_y(self, other: Point) -> int:
        return max(self.y, other.y) - min(self.y, other.y)

    def delta(self, other: Point) -> Point:
        return Point(self.d_x(other), self.d_y(other))

    def __hash__(self):
        tup = (self.x, self.y)
        return hash(tup)

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def in_bounds(self, x_bounds: tuple[int, int], y_bounds: tuple[int, int]) -> bool:
        return (
            self.x >= x_bounds[0]
            and self.x < x_bounds[1]
            and self.y >= y_bounds[0]
            and self.y < y_bounds[1]
        )

    def __str__(self) -> str:
        return f"({self.x},{self.y})"

    def __repr__(self) -> str:
        return self.__str__()


def print_grid(
    nodes: list[tuple[str, Point]], antinodes: list[Point], width: int, height: int
):
    positions: dict[Point, str] = {}
    for node in nodes:
        positions[node[1]] = node[0]

    for antinode in antinodes:
        positions[antinode] = "#"

    print("\t0 1 2 3 4 5 6 7 8 9")
    for y in range(height):
        print(y, end="\t")
        for x in range(width):
            if Point(x, y) in positions:
                print(f"{positions[Point(x,y)]}", end=" ")
            else:
                print(".", end=" ")

        print()


@timer
def p1_naive(text: list[str]) -> int:
    nodes: dict[str, list[Point]] = {}

    height: int = len(text)
    width: int = len(text[0])

    for y, line in enumerate(text):
        for x, char in enumerate(line):
            if char != ".":
                if char not in nodes:
                    nodes[char] = [Point(x, y)]
                else:
                    nodes[char].append(Point(x, y))

    antinodes: set[Point] = set()

    for node in nodes:
        for pair in itertools.combinations(nodes[node], 2):
            # print("pair:", pair)
            delta: Point = pair[0].delta(pair[1])
            # print("delta: ", delta)

            d_x = pair[1].x - pair[0].x
            d_y = pair[1].y - pair[0].y

            a1_x = pair[0].x - d_x
            a1_y = pair[0].y - d_y

            a2_x = pair[1].x + d_x
            a2_y = pair[1].y + d_y

            a1: Point = Point(a1_x, a1_y)
            a2: Point = Point(a2_x, a2_y)

            # if rising:
            # a1 = pair[0] + delta
            # a2 = pair[1] - delta

            # print(f"a1: {a1}")
            # print(f"a2: {a2}")

            antinodes.add(a1)
            antinodes.add(a2)

    node_list: list[tuple[str, Point]] = []
    for node in nodes:
        for pos in nodes[node]:
            node_list.append((node, pos))

    # print_grid(node_list, list(antinodes), width, height)

    return len([node for node in antinodes if node.in_bounds((0, width), (0, height))])


@timer
def p2_naive(text: list[str]) -> int:
    nodes: dict[str, list[Point]] = {}

    height: int = len(text)
    width: int = len(text[0])

    for y, line in enumerate(text):
        for x, char in enumerate(line):
            if char != ".":
                if char not in nodes:
                    nodes[char] = [Point(x, y)]
                else:
                    nodes[char].append(Point(x, y))

    antinodes: set[Point] = set()

    for node in nodes:
        for pair in itertools.combinations(nodes[node], 2):
            # print("pair:", pair)
            delta: Point = pair[0].delta(pair[1])
            # print("delta: ", delta)

            d_x = pair[1].x - pair[0].x
            d_y = pair[1].y - pair[0].y

            steps: int = 0
            while steps < 100:
                steps += 1
                # print(steps)
                a1_x = pair[0].x - (d_x * steps)
                a1_y = pair[0].y - (d_y * steps)

                a2_x = pair[1].x + (d_x * steps)
                a2_y = pair[1].y + (d_y * steps)

                a1: Point = Point(a1_x, a1_y)
                a2: Point = Point(a2_x, a2_y)

                antinodes.add(a1)
                antinodes.add(a2)

                # if (not a1.in_bounds((0, width), (0, height))) or (
                #     not a2.in_bounds((0, width), (0, height))
                # ):
                #     break

    node_list: list[tuple[str, Point]] = []
    for node in nodes:
        for pos in nodes[node]:
            antinodes.add(pos)
            node_list.append((node, pos))

    # print_grid(node_list, list(antinodes), width, height)

    return len([node for node in antinodes if node.in_bounds((0, width), (0, height))])


class Day_8(Solution):
    def __init__(self):
        super().__init__(DAY, REAL)

    def run(self):
        text = self.get_input()[:-1]
        #         text = """..........
        # ..........
        # ..........
        # ..........
        # .....a....
        # ...a......
        # ....ab....
        # ..........
        # ......b...
        # ..........
        # """.split(
        #             "\n"
        #         )
        # print(f"part 1, naive: {p1_naive(text)}")
        print(f"part 2, naive: {p2_naive(text)}")
