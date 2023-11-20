"""
    Хранит значения номера ячейки по вертикали и горизонтали
"""
from typing import Self


class Vector2:
    def __init__(self, vertical: int, horizontal: int):
        self.vertical = vertical
        self.horizontal = horizontal

    def __str__(self):
        return f'Vector2({self.vertical}, {self.horizontal})'

    def __add__(self, other: Self) -> Self:
        return Vector2(
            self.vertical + other.vertical,
            self.horizontal + other.horizontal
        )

    def __eq__(self, other: Self) -> bool:
        return self.vertical == other.vertical and \
            self.horizontal == other.horizontal

    def __hash__(self) -> int:
        return hash((self.vertical, self.horizontal))

    def copy(self) -> Self:
        return Vector2(self.vertical, self.horizontal)
