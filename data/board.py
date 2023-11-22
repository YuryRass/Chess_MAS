"""Модуль, реализующий класс шахматной доски"""

from copy import deepcopy
from typing import Self
from data.board_event import \
    BoardEvent, ChessPieceMovedBoardEvent, InactivityBoardEvent

from data.chess_piece import ChessPiece
from data.conflict import Conflict
from data.move_suggestions import MoveSuggestion
from data.position import Position
from data.vector2 import Vector2


class Board:
    """Шахматная доска"""

    def __init__(self, pieces: list[ChessPiece], size: Vector2):
        """
        Args:
            pieces (list[ChessPiece]): список шахматных фигур
            size (Vector2): размер шахм. доски
        """
        self.pieces = pieces
        self.size = size

    def copy(self) -> Self:
        return Board(
            pieces=deepcopy(self.pieces),
            size=self.size.copy(),
        )

    def has_position(self, position: Position) -> bool:
        """Проверяет возможность присутствия переданной позиции
        на шахматной доске

        Args:
            position (Position): проверяемая позиция

        Returns:
            bool: True, если присутсвует. False - иначе.
        """
        return (
            1 <= position.vertical <= self.size.vertical and
            1 <= position.horizontal <= self.size.horizontal
        )

    def get_chess_piece(self, position: Position) -> ChessPiece | None:
        """Возвращает шахматную фигуру для указанной позиции

        Args:
            position (Position): указанная позиция

        Returns:
            ChessPiece | None: шахм. фигура или её отсутствие
        """
        for piece in self.pieces:
            if piece.position == position:
                return piece
        return None

    def position_empty(self, position: Position) -> bool:
        """Проверяет позицию на пустоту (отсутствие на ней фигуры)

        Args:
            position (Position): переданная позиция

        Returns:
            bool: True, если на переданной позиции нет фигуры, False - иначе
        """
        for piece in self.pieces:
            if piece.position == position:
                return False
        return True

    def find_piece_by_id(self, piece_id: str) -> ChessPiece | None:
        """Поиск фигуры по её ID

        Args:
            piece_id (str): ID шахматной фигуры

        Returns:
            ChessPiece | None: шахм. фигура или её отсутсвие
        """
        for piece in self.pieces:
            if piece.id == piece_id:
                return piece
        return None

    def get_chess_piece_moves(self, piece: ChessPiece) -> list[Position]:
        """Возвращает различные ходы шахматной фигуры

        Args:
            piece (ChessPiece): _description_

        Returns:
            list[Position]: _description_
        """
        positions: list[Position] = []

        for move in piece.moves:
            position = piece.position.copy()

            if move.is_direction:  # если возможны ходы более, чем на 1 клетку
                while True:
                    position = piece.position.copy_with(
                        position.position + move.change
                    )

                    if self.has_position(position):
                        positions.append(position)
                        # если позиция занята, закрываем цикл
                        if not self.position_empty(position):
                            break
                    else:  # вышли за края шахматной доски
                        break
            else:
                # новая позиция
                position = piece.position.copy_with(
                    position.position + move.change
                )

                # если позиция находится в рамках шахм. доски
                if self.has_position(position):
                    positions.append(position)

        return positions

    def get_movable_positions(self, piece: ChessPiece) -> list[Position]:
        """Возвращает различные ходы шахм. фигуры без пересечения
        с другими фигурами

        Args:
            piece (ChessPiece): шахм. фигура

        Returns:
            list[Position]: список ходов
        """
        positions = self.get_chess_piece_moves(piece)
        return [it for it in positions if self.position_empty(it)]

    def can_move(self, piece: ChessPiece, new_position: Position) -> bool:
        """Проверяет можно ли сдинуться на новую позицию шахм. фигуре

        Args:
            piece (ChessPiece): шахм. фигура
            new_position (Position): новая позиция

        Returns:
            bool: True, если можно поменять позицию. False - иначе
        """

        # если выли за рамки доски:
        if not self.has_position(new_position):
            return False

        # если уткнулись на фигуру на данной позиции
        if not self.position_empty(new_position):
            return False

        # получаем список различных ходов для шахм. фигуры
        positions = self.get_chess_piece_moves(piece)

        # перебираем всевозможные передвижения для конкретной шахм. фигуры
        # и если нашли совпадение с new_position, то возвращаем True,
        # иначе - False
        for position in positions:
            if self.has_position(position):
                if position == new_position:
                    return True

        return False

    def move(
        self,
        piece: ChessPiece,
        new_position: Position,
    ) -> ChessPiece | None:
        """Передвижение фигуры

        Args:
            piece (ChessPiece): фигура
            new_position (Position): новая позиция

        Returns:
            ChessPiece | None: Шахм. фигура с новой позицией
        """
        if self.can_move(piece, new_position):
            new_piece = piece.copy_with(position=new_position)
            self.pieces[self.pieces.index(piece)] = new_piece
            return new_piece

        return None

    def apply(self, message: MoveSuggestion) -> BoardEvent:
        """Применяет перемещение шахматной фигуры на доске

        Args:
            message (MoveSuggestion): сообщение с предложением о перемещении

        Returns:
            BoardEvent: ChessPieceMovedBoardEvent | None
        """
        piece = self.find_piece_by_id(message.piece_id)
        if isinstance(piece, ChessPiece):
            if self.can_move(piece, message.new_position):
                position = piece.position.copy_with()
                new_piece = self.move(piece, message.new_position)

                if new_piece is None:  # бездействие
                    return InactivityBoardEvent  # None

                # возвращаем данные для отображения на шахм. доске
                return ChessPieceMovedBoardEvent(
                    piece_id=piece.id,
                    position=position,
                    new_position=new_piece.position,
                )

        return InactivityBoardEvent  # None

    def get_chesspiece_attacks(self, piece: ChessPiece) -> list[Position]:
        """Возвращает список позиций фигур, которые находятся
        под атакой переданной фигуры piece

        Args:
            piece (ChessPiece): шахм. фигура

        Returns:
            list[Position]: список позиций
        """
        positions: list[Position] = []

        for move in piece.additional_attacks:
            position = piece.position.copy()
            if move.is_direction:
                while True:
                    position = piece.position.copy_with(
                        position.position + move.change
                    )

                    if self.has_position(position):
                        if not self.position_empty(position):
                            positions.append(position)
                            break
                    else:
                        break
            else:
                position = piece.position.copy_with(
                    position.position + move.change
                )

                if self.has_position(position):
                    if not self.position_empty(position):
                        positions.append(position)

        positions.extend(self.get_chess_piece_moves(piece))
        return positions

    def get_conflicts(self) -> list[Conflict]:
        """Возвращает конфликтные ситуации (шахм. фигура находится под ударом)

        Returns:
            list[Conflict]: список конфликтов
        """
        conflicts: list[Conflict] = []

        for piece in self.pieces:
            positions = self.get_chesspiece_attacks(piece)

            for position in positions:
                if self.has_position(position):
                    victim = self.get_chess_piece(position)
                    if victim is not None:
                        conflicts.append(Conflict(source=piece, victim=victim))
        return conflicts
