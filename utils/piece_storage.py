"""Хранилище фигур"""
from typing import Callable

from data.chess_piece import ChessPiece
from data.pieces import (
    Queen,
)
from data.position import Position
from data.vector2 import Vector2


class PieceStorage:
    """Хранилище шахматных фигур"""

    def __init__(self, is_standart: bool = False):
        """
        Args:
            is_standart (bool, optional): стандартная конфигурация шахм. доски.
        Defaults to False.
        """
        self.pieces: list[ChessPiece] = []
        if is_standart:
            self.pieces.extend(
                [
                    Queen(
                        position=Position(
                            position=Vector2(vertical=0, horizontal=0),
                        ),
                    ),
                ]
            )

    def add(self, piece: ChessPiece):
        """Добавление шахм. фигуры
        Args:
            piece (ChessPiece): фигура
        """
        self.pieces.append(piece)

    def get_piece(self, name: str) -> Callable[[Position], ChessPiece]:
        """Возвращает функцию для получения шахм. фигуры

        Args:
            name (str): имя шахм. фигуры

        Returns:
            Callable[[Position], ChessPiece]
        """
        def func(position: Position) -> ChessPiece:
            """Возвращает копию шахм. фигуры с заданной позицией

            Args:
                position (Position): позиция шахм. фигуры

            Raises:
                NotImplementedError: отсутвие фигуры

            Returns:
                ChessPiece: шахм. фигура
            """
            for piece in self.pieces:
                if piece.name == name:
                    return piece.copy_with(position=position)
            raise NotImplementedError("Piece not found")

        return func
