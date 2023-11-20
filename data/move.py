"""Отвечает за возможность перемещения шахм. фигур"""

from typing import Self
from data.vector2 import Vector2


class Move:
    def __init__(self, change: Vector2, is_direction: bool = False):
        self.change = change
        # is_direction - возможность передвижения шахматной фигуры
        # до упора (конца шахматной доски)
        self.is_direction = is_direction

    def __str__(self):
        return f"Move({self.change}, {self.is_direction})"

    def copy(self) -> Self:
        return Move(self.change.copy(), self.is_direction)

    def __eq__(self, other: Self) -> bool:
        return self.change == other.change and \
            self.is_direction == other.is_direction

    def __hash__(self) -> int:
        return hash((self.change, self.is_direction))
