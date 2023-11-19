"""Отвечает за хранение кол-ва конфликтов в эпохе.
Позволяет сравнивать конфликты между собой.
"""

from typing import Self


class EpochInfo:
    def __init__(self, number_of_conflicts: int = 0):
        self.number_of_conflicts = number_of_conflicts

    def __str__(self):
        return f"EpochInfo({self.number_of_conflicts})"

    def __eq__(self, other: Self) -> bool:
        return self.number_of_conflicts == other.number_of_conflicts

    def __lt__(self, other: Self) -> bool:
        return self.number_of_conflicts < other.number_of_conflicts

    def __hash__(self) -> int:
        return hash(self.number_of_conflicts)