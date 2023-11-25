from data.chess_piece import ChessPiece
from data.move import Move
from data.position import Position
from data.vector2 import Vector2


class Knight(ChessPiece):

    """Шахматная фигура - Конь"""

    __name = 'N'

    __moves: list[Move] = [
        Move(change=Vector2(vertical=2, horizontal=-1), is_direction=False),
        Move(change=Vector2(vertical=2, horizontal=1), is_direction=False),
        Move(change=Vector2(vertical=1, horizontal=2), is_direction=False),
        Move(change=Vector2(vertical=-1, horizontal=2), is_direction=False),
        Move(change=Vector2(vertical=-2, horizontal=1), is_direction=False),
        Move(change=Vector2(vertical=-2, horizontal=-1), is_direction=False),
        Move(change=Vector2(vertical=-1, horizontal=-2), is_direction=False),
        Move(change=Vector2(vertical=1, horizontal=-2), is_direction=False),
    ]

    def __init__(
        self,
        position: Position,
        chess_id: str | None = None,
    ):
        if chess_id is None:
            super().__init__(
                name=Knight.__name,
                moves=Knight.__moves,
                position=position,
            )
        else:
            super().__init__(
                name=Knight.__name,
                moves=Knight.__moves,
                position=position,
                chess_id=chess_id,
            )
