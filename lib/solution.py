"""solution.py

Implement a general solution class
"""

from lib import input


class Solution:
    def __init__(self, day: int, real: bool = False):
        self.day: int = day
        self.real: bool = real

    def get_input(self) -> list[str]:
        reader = input.Reader(self.day, self.real)
        return reader.read_lines()
