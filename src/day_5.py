"""AOC 2024 - Day 5"""

import lib.colors as color
from lib.solution import Solution
from lib.timer import timer, timer_ns

DAY = 5
REAL = True


def is_valid(pages: list[str], rules: dict[str, list[str]]) -> bool:
    for i, page in enumerate(pages):
        if page in rules:
            posteriors = rules[page]
            for number in posteriors:
                # print(number, pages)
                if number in pages:
                    if pages.index(number) < i:
                        # print(pages.index(number), i)
                        # print("FALSE")
                        return False

    # print("TRUE")
    return True


@timer
def p1_naive(t: str) -> int:
    rule_objects = {}

    rules, updates = t.split("\n\n")
    rules = rules.split("\n")
    updates = updates.split("\n")

    for rule in rules:
        prior, posterior = rule.split("|")
        if prior in rule_objects:
            rule_objects[prior].append(posterior)
        else:
            rule_objects[prior] = [posterior]

    correct = []
    incorrect = []
    for update in [update for update in updates if update != ""]:
        pages: list[str] = update.split(",")
        if is_valid(pages, rule_objects):
            correct.append(pages)

    total = 0
    for update in correct:
        n = len(update)
        mid = n // 2
        total += int(update[mid])

    return total


def correct_update(pages: list[str], rules: dict[str, list[str]]) -> list[str]:
    for i, page in enumerate(pages):
        if page in rules:
            posteriors = rules[page]
            for number in posteriors:
                if number in pages:
                    if pages.index(number) < i:
                        # print(f"page {page} should become before {number}")
                        # print("orig", pages)
                        pg = pages.copy()
                        _ = pg.pop(pg.index(page))
                        # print("pg", pg)
                        pos = pg.index(number)
                        # print("new", pg[:pos] + [page] + pg[pos:])
                        pages = pg[:pos] + [page] + pg[pos:]

    # print("TRUE")
    # print(pages)
    # print()
    return pages


@timer
def p2_naive(t: str) -> int:
    rule_objects = {}

    rules, updates = t.split("\n\n")
    rules = rules.split("\n")
    updates = updates.split("\n")

    for rule in rules:
        prior, posterior = rule.split("|")
        if prior in rule_objects:
            rule_objects[prior].append(posterior)
        else:
            rule_objects[prior] = [posterior]

    incorrect = []
    for update in [update for update in updates if update != ""]:
        pages: list[str] = update.split(",")
        if not is_valid(pages, rule_objects):
            incorrect.append(pages)

    total = 0
    for update in incorrect:
        # update = correct_update(update, rule_objects)
        # if not is_valid(update, rule_objects):
        # print(update)
        i = 0
        while not is_valid(update, rule_objects):
            i += 1
            update = correct_update(update, rule_objects)
            # print(i, end=" ")

        # print()

        n = len(update)
        mid = n // 2
        total += int(update[mid])

    return total


class Day_5(Solution):
    def __init__(self):
        super().__init__(DAY, REAL)

    def run(self):
        text = self.get_raw()
        print(f"part 1, naive: {p1_naive(text)}")
        print(f"part 2, naive: {p2_naive(text)}")
