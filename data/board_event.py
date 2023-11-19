"""Отвечает за хранение данных о перемещениях на шахм. доске"""

from data.position import Position

InactivityBoardEvent = None

class ChessPieceMovedBoardEvent:
    def __init__(
        self,
        piece_id: str,
        position: Position,
        new_position: Position,
    ):
        """
        Args:
            piece_id (str): ID фигуры
            position (Position): ткущая позиция фигуры
            new_position (Position): новая позиция фигуры
        """
        self.piece_id = piece_id
        self.position = position
        self.new_position = new_position

    def __str__(self):
        return f"Move(ID={self.piece_id}, from={self.position}, to={self.new_position})"

    def __repr__(self) -> str:
        return str(self)
