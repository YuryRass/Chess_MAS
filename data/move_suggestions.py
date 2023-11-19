"""Предложения по передвижению фигуры"""

from typing import Self
from data.position import Position


class MoveSuggestion:
    def __init__(
        self,
        piece_id: str,
        new_position: Position,
        number_of_conflicts: int,
    ):
        """Первичая инициализация

        Args:
            piece_id (str): ID шахматной фигуры

            new_position (Position): новая возможная позиция для фигуры
            
            number_of_conflicts (int): кол-во конфликтных ситуаций
        """
        self.piece_id = piece_id
        self.new_position = new_position
        self.number_of_conflicts = number_of_conflicts


    def __str__(self):
        return f"MoveSuggestion({self.piece_id}, {self.new_position}, {self.number_of_conflicts})"

    def __eq__(self, other: Self) -> bool:
        return (
            self.piece_id == other.piece_id
            and self.new_position == other.new_position
            and self.number_of_conflicts == other.number_of_conflicts
        )

    def __hash__(self) -> int:
        return hash((self.piece_id, self.new_position, self.number_of_conflicts))

    def copy(self) -> Self:
        return MoveSuggestion(
            self.piece_id,
            self.new_position.copy(),
            self.number_of_conflicts,
        )