"""AOC 2024 - Day 7"""

from __future__ import annotations

import itertools
import math
import re
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from enum import Enum
from itertools import product

import lib.colors as colors
from lib.solution import Solution
from lib.timer import timer, timer_ns

DAY = 7
REAL = True


@dataclass
class Equation:
    test_value: int
    operands: list[int]

    def possible_pt1(self) -> bool:
        operator_amount: int = len(self.operands) - 1
        # print(f"Operator amount: {operator_amount}")

        operator_combinations: list[str] = list(
            itertools.product("*+", repeat=operator_amount)
        )

        # print(f"Possible operator combs: {operator_combinations}")
        for comb in operator_combinations:
            res: int = self.operands[0]
            for i, operator in enumerate(comb):
                if operator == "+":
                    res = res + self.operands[i + 1]
                    # print(res, "+", self.operands[i + 1])
                else:
                    res = res * self.operands[i + 1]
                    # print(res, "*", self.operands[i + 1])

            # print(res, comb)

            if res == self.test_value:
                # print(f"Yes, with comb: {comb}")
                return True

        # print("No!")
        # print()
        return False

    def possible_pt2(self) -> bool:
        operator_amount: int = len(self.operands) - 1

        operator_combinations: list[str] = list(
            itertools.product("*+|", repeat=operator_amount)
        )

        for comb in operator_combinations:
            res: int = self.operands[0]
            for i, operator in enumerate(comb):
                if operator == "+":
                    res = res + self.operands[i + 1]
                elif operator == "*":
                    res = res * self.operands[i + 1]
                else:
                    res = int(str(res) + str(self.operands[i + 1]))

            if res == self.test_value:
                return True

        return False

    @staticmethod
    def build(line: str) -> Equation:
        parts: list[str] = line.split(": ")
        test_value = int(parts[0])
        operands = [int(x) for x in parts[1].split()]

        return Equation(test_value, operands)


def check_eq(eq: Equation, part: int) -> int:
    if part == 1:
        if eq.possible_pt1():
            return eq.test_value
    else:
        if eq.possible_pt2():
            return eq.test_value

    return 0


@timer
def p1_async(text: list[str]) -> int:
    total: int = 0
    equations = [Equation.build(line) for line in text]

    with ProcessPoolExecutor(max_workers=8) as executor:
        futures = {
            executor.submit(check_eq, equation, 1): equation for equation in equations
        }

        for future in as_completed(futures):
            total += future.result()

    return total


@timer
def p2_async(text: list[str]) -> int:
    total: int = 0
    equations = [Equation.build(line) for line in text]

    with ProcessPoolExecutor(max_workers=8) as executor:
        futures = {
            executor.submit(check_eq, equation, 2): equation for equation in equations
        }

        for future in as_completed(futures):
            total += future.result()

    return total


@timer
def p1_naive(text: list[str]) -> int:
    correct_test_values: list[int] = []

    equations = [Equation.build(line) for line in text]
    for equation in equations:
        if equation.possible_pt1():
            correct_test_values.append(equation.test_value)

    return sum(correct_test_values)


@timer
def p2_naive(text: list[str]) -> int:
    correct_test_values: list[int] = []

    equations = [Equation.build(line) for line in text]
    amount: int = len(equations)
    for i, equation in enumerate(equations):
        print(f"Processing equation {i}/{amount} ({i/amount*100:.02f}%)")
        if equation.possible_pt2():
            correct_test_values.append(equation.test_value)

    return sum(correct_test_values)


class Day_7(Solution):
    def __init__(self):
        super().__init__(DAY, REAL)

    def run(self):
        text = self.get_input()[:-1]
        print(f"part 1, naive: {p1_naive(text)}")
        print(f"part 1, async: {p1_async(text)}")

        # print(f"part 2, naive: {p2_naive(text)}")
        print(f"part 2, async: {p2_async(text)}")
