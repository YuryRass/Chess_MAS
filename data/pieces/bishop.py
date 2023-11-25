from data.chess_piece import ChessPiece
from data.move import Move
from data.position import Position
from data.vector2 import Vector2


class Bishop(ChessPiece):
    """Шахматная фигура - Слон"""
    __name = 'B'

    __moves: list[Move] = [
        Move(change=Vector2(vertical=1, horizontal=1), is_direction=True),
        Move(change=Vector2(vertical=1, horizontal=-1), is_direction=True),
        Move(change=Vector2(vertical=-1, horizontal=-1), is_direction=True),
        Move(change=Vector2(vertical=-1, horizontal=1), is_direction=True),
    ]

    def __init__(
        self,
        position: Position,
        chess_id: str | None = None,
    ):
        if chess_id is None:
            super().__init__(
                name=Bishop.__name,
                moves=Bishop.__moves,
                position=position,
            )
        else:
            super().__init__(
                name=Bishop.__name,
                moves=Bishop.__moves,
                position=position,
                chess_id=chess_id,
            )
