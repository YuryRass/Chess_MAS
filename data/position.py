"""Позиции шахм. фигур"""

from typing import Self
from data.vector2 import Vector2


class Position:
    """Позиции на шахматной доске"""
    def __init__(self, position: Vector2) -> None:
        self.position = position

    @property
    def vertical(self) -> int:
        return self.position.vertical

    @property
    def horizontal(self) -> int:
        return self.position.horizontal

    def __str__(self) -> str:
        return f'Position({self.position.vertical}, ' + \
            f'{self.position.horizontal})'

    def copy(self) -> Self:
        return Position(self.position.copy())

    def copy_with(self, other: Vector2 | None = None) -> Self:
        if other is None:
            return self.copy()
        return Position(other.copy())

    def __eq__(self, other: Self) -> bool:
        return self.position == other.position

    def __hash__(self) -> int:
        return hash(self.position)
