"""Отвечает за хранение данных о перемещениях на шахм. доске"""

from data.position import Position

InactivityBoardEvent = None


class ChessPieceMovedBoardEvent:
    """Перемещение шахм. фигур на доске"""
    
    def __init__(
        self,
        piece_id: str,
        position: Position,
        new_position: Position,
    ) -> None:
        """
        Args:
            piece_id (str): ID фигуры
            position (Position): текущая позиция фигуры
            new_position (Position): новая позиция фигуры
        """
        self.piece_id = piece_id
        self.position = position
        self.new_position = new_position

    def __str__(self) -> str:
        return f"Move(ID={self.piece_id}, from={self.position}, " + \
            f"to={self.new_position})"

    def __repr__(self) -> str:
        return str(self)


BoardEvent = InactivityBoardEvent | ChessPieceMovedBoardEvent
