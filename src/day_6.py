"""AOC 2024 - Day 6"""

from __future__ import annotations

import re
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from enum import Enum
from itertools import product

import lib.colors as colors
from lib.solution import Solution
from lib.timer import timer, timer_ns

DAY = 6
REAL = True


@dataclass
class Point:
    x: int
    y: int

    def to_tuple(self):
        return (self.x, self.y)


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

    def __str__(self) -> str:
        match self:
            case Direction.UP:
                return "^"
            case Direction.RIGHT:
                return ">"
            case Direction.DOWN:
                return "v"
            case Direction.LEFT:
                return "<"


@dataclass
class Guard:
    position: Point
    direction: Direction

    def turn(self) -> Guard:
        match self.direction:
            case Direction.UP:
                return Guard(self.position, Direction.RIGHT)
            case Direction.RIGHT:
                return Guard(self.position, Direction.DOWN)
            case Direction.DOWN:
                return Guard(self.position, Direction.LEFT)
            case Direction.LEFT:
                return Guard(self.position, Direction.UP)

    def __repr__(self) -> str:
        return str(self.direction)


class Maze:
    def __init__(self, width: int, height: int, obstacles: list[Point], guard: Guard):
        self.width: int = width
        self.height: int = height

        self.obstacles: list[Point] = obstacles
        self.guard: Guard = guard

        self.visited: set[tuple[int, int]] = set()

    def __repr__(self) -> str:
        string: str = " 0123456789\n"
        for y in range(self.height):
            string += str(y)
            for x in range(self.width):
                if Point(x, y) in self.obstacles:
                    string += colors.red("#")
                elif Point(x, y) == self.guard.position:
                    string += colors.bold(colors.blue(str(self.guard)))
                elif (x, y) in self.visited:
                    string += colors.blue("x")
                else:
                    string += "."

            string += "\n"

        return string

    def move_guard(self):
        delta_x: int = 0
        delta_y: int = 0

        match self.guard.direction:
            case Direction.UP:
                delta_y = -1
            case Direction.RIGHT:
                delta_x = 1
            case Direction.DOWN:
                delta_y = 1
            case Direction.LEFT:
                delta_x = -1

        new_position: Point = Point(
            self.guard.position.x + delta_x, self.guard.position.y + delta_y
        )

        if new_position in self.obstacles:
            self.guard = self.guard.turn()
        else:
            self.guard = Guard(new_position, self.guard.direction)

        self.visited.add(self.guard.position.to_tuple())

    def guard_in_bounds(self) -> bool:
        if (
            self.guard.position.x >= 0
            and self.guard.position.x < self.width
            and self.guard.position.y >= 0
            and self.guard.position.y < self.height
        ):
            return True

        return False

    @staticmethod
    def build(lines: list[str]):
        obstacles: list[Point] = []
        guard: Guard = Guard(Point(0, 0), Direction.UP)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == "^":
                    guard = Guard(Point(x, y), Direction.UP)
                elif char == ">":
                    guard = Guard(Point(x, y), Direction.RIGHT)
                elif char == "v":
                    guard = Guard(Point(x, y), Direction.DOWN)
                elif char == "<":
                    guard = Guard(Point(x, y), Direction.LEFT)
                elif char == "#":
                    obstacles.append(Point(x, y))

        height: int = len(lines)
        width: int = len(lines[0])

        return Maze(width, height, obstacles, guard)


@timer
def p1_naive(text: list[str]) -> int:
    maze = Maze.build(text)

    i: int = 0
    while maze.guard_in_bounds():
        maze.move_guard()
        # print(maze)
        print(f"Guard has visited {len(maze.visited)-1} squares")

        i += 1
        # time.sleep(0.05)
        # input("next?")
        colors.clear()

    print(maze)
    print(f"Guard has visited {len(maze.visited)-1} squares")

    return (
        len(maze.visited) - 1
    )  # But actually the result is +1 if the direction was up...

def check_for_loops(maze: Maze, curr: int) -> bool:
    maximum: int = maze.width * maze.height

    curr += 1
    # colors.clear()
    print(f"Running... {curr}/{maximum} ({(curr/maximum)*100:.02f}%)")

    last_change: int = 0
    i: int = 0
    while maze.guard_in_bounds():
        visited: int = len(maze.visited)
        maze.move_guard()

        i += 1
        if len(maze.visited) > visited:
            last_change = i
        else:
            if i > last_change + max(maze.width, maze.height):
                return True

    return False

@timer
def p2_naive(text: list[str]) -> int:
    loops: int = 0
    curr: int = 0

    maze = Maze.build(text)
    for y in range(10):
        for x in range(10):
            maze = Maze.build(text)
            maze.obstacles.append(Point(x,y))

            if Point(x, y) == maze.guard.position:
                break

            curr += 1

            if check_for_loops(maze, curr):
                loops += 1

    print(f"Loops found: {loops}")
    return loops

def process_point(x,y,text,curr):
    maze = Maze.build(text)
    maze.obstacles.append(Point(x,y))

    if Point(x,y) == maze.guard.position:
        return None

    curr += 1

    if check_for_loops(maze, curr):
        return True

    return False

@timer
def p2_async(text: list[str]) -> int:
    loops: int = 0
    curr: int = 0

    points = list(product(range(10), repeat=2))

    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_point, x, y, text, curr): (x, y) for x, y in points}

        for future in as_completed(futures):
            result = future.result()
            if result is None:
                print("None")
                continue
            if result:
                print(result)
                loops += 1

    print(f"Loops found: {loops}")
    return loops


class Day_6(Solution):
    def __init__(self):
        super().__init__(DAY, REAL)

    def run(self):
        text = self.get_input()[:-1]
        # print(f"part 1, naive: {p1_naive(text)}")
        # print(f"part 2, naive: {p2_naive(text)}")
        print(f"part 2, async: {p2_async(text)}")
