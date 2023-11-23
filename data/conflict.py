"""
Отвечает за хранение данных о конфликтных ситациях
на шахматной доске
"""

from typing import Self
from data.chess_piece import ChessPiece


class Conflict:
    """Конфликтные ситуации на доске"""
    def __init__(
        self,
        source: ChessPiece,
        victim: ChessPiece,
    ) -> None:
        """
        Args:
            source (ChessPiece): текущая фигура
            victim (ChessPiece): фигура, находящаяся под атакой
        """
        self.source = source
        self.victim = victim

    def __eq__(self, other: Self) -> bool:
        return (
            self.source == other.source
            and self.victim == other.victim
        )

    def __hash__(self) -> int:
        return hash((self.source, self.victim))

    def __repr__(self) -> str:
        return f"Conflict(source: {self.source}, victim: {self.victim})"
