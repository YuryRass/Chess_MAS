"""Отвечает за объявления шахматных фигур"""

from copy import deepcopy

from typing import Self
from data.move import Move
from data.position import Position


class ChessPiece:
    def __init__(
        self,
        name: str,
        moves: list[Move],
        position: Position,
        additional_attacks: list[Move] | None = None,
        chess_id: str = "0",
    ):
        """Первичная инициализация

        Args:
            name (str): название шахм. фигуры

            moves (list[Move]): разрешенные пути перемещения

            position (Position): текущая позиция фигуры

            additional_attacks (list[Move] | None, optional): список ходов,
        когда фигуры находятся под атакой. Defaults to None.

            chess_id (str, optional): ID фигуры. Defaults to "0".
        """
        self.id = chess_id
        self.moves = moves
        self.position = position
        self.name = name

        if additional_attacks is not None:
            self.additional_attacks = additional_attacks
        else:
            self.additional_attacks = []

    def __eq__(self, other: Self) -> bool:
        return (
            self.id == other.id
            and self.name == other.name
            and self.moves == other.moves
            and self.position == other.position
            and self.additional_attacks == other.additional_attacks
        )

    def __hash__(self) -> int:
        return hash(
            (
                self.id, self.name, self.moves,
                self.position, self.additional_attacks
            )
        )

    def copy(self) -> Self:
        return ChessPiece(
            self.name,
            deepcopy(self.moves),
            self.position.copy(),
            chess_id=self.id,
        )

    def copy_with(
            self,
            name: str | None = None,
            moves: list[Move] | None = None,
            position: Position | None = None,
            additional_attacks: list[Move] | None = None,
            chess_id: str | None = None,
    ) -> Self:
        return ChessPiece(
            name if name is not None else self.name,
            moves if moves is not None else deepcopy(self.moves),
            position if position is not None else self.position,
            additional_attacks if additional_attacks is not None else deepcopy(
                self.additional_attacks
            ),
            chess_id if chess_id is not None else self.id,
        )
