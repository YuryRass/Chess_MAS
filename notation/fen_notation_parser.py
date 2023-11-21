"""
    Разбор шахматной доски, представленной по нотации Форсайта-Эдвардса
"""
from data.board import Board
from data.chess_piece import ChessPiece
from data.position import Position
from data.vector2 import Vector2
from notation.notation_parser import NotationParser
from utils.piece_storage import PieceStorage


class FenNotationParser(NotationParser):
    """Парсер FEN-строк"""

    def parse(self, fen_str: str, storage: PieceStorage) -> Board:
        """Парсит строку, представленную по нотации
        Форсайта-Эдвардса (FEN-строка)

        Args:
            fen_str (str): FEN-строка
            storage (PieceStorage): хранилище шахм. фигур

        Returns:
            Board: проинициализированная шахм. доска
        """
        piece_id = 0
        pieces: list[ChessPiece] = []

        # Определяем размер шахматной доски
        rows = fen_str.split("/")
        width = self.row_length(rows[0])
        size = Vector2(vertical=len(rows), horizontal=width)

        for row_index, row in enumerate(rows):
            list_pieces = self.get_chess_pieces_in_row(
                row, row_index + 1, storage
            )

            # последовтельно добавляем ID шахматных фигур
            for index, data in enumerate(list_pieces):
                list_pieces[index] = data.copy_with(chess_id=str(piece_id))
                piece_id += 1

            pieces.extend(list_pieces)
        return Board(size=size, pieces=pieces)

    def serialize(self, board: Board) -> str:
        """Обратная операция парсингу: представляет шахматную доску
        с фигурами в виде FEN-строки

        Args:
            board (Board): шахм. доска

        Returns:
            str: FEN-строка
        """
        fen = ""
        # список со списками фигур на каждой горизонтали шахм. доски
        chess_pieces_by_row: list[list[ChessPiece]] = [
            [] for _ in range(board.size.vertical)
        ]

        # инициализация chess_pieces_by_row
        for piece in board.pieces:
            chess_pieces_by_row[
                piece.position.position.vertical - 1
            ].append(piece)

        # расставляем по порядку все шахм. фигуры на их горизонталях
        for pieces_by_row in chess_pieces_by_row:
            pieces_by_row.sort(key=lambda x: x.position.position.horizontal)

            visited = 0
            for piece_index in range(len(pieces_by_row)):
                piece = pieces_by_row[piece_index]
                # check показывает кол-во пустых клеток на горизнтали доски
                check = piece.position.position.horizontal - visited - 1
                if check > 0:
                    fen += f"{check}"

                fen += piece.name
                visited = piece.position.position.horizontal

                # когда дошли до самой нижней горизонтали
                if piece_index == len(pieces_by_row) - 1:
                    if board.size.horizontal - visited > 0:
                        fen += f"{board.size.horizontal - visited}"

            # случай, когда нет фигур на горизонтали
            if len(pieces_by_row) == 0:
                fen += f'{board.size.horizontal}'

            # добавляем симвло '/' к концу строки
            if pieces_by_row != chess_pieces_by_row[:-1]:
                fen += "/"
        return fen[:-1]

    def row_length(self, row: str) -> int:
        """Определяет ширину шахматной доски

        Args:
            row (str): исходная строка для парсинга

        Returns:
            int: ширина доски
        """
        length = 0
        # единичные, десятые, сотые и т.д. натурального числа
        number_accumulator = 0
        symbols = list(row)

        for symbol in symbols:
            if symbol.isdigit():
                number_accumulator = number_accumulator * 10 + int(symbol)
            else:
                if number_accumulator != 0:
                    length += number_accumulator + 1
                    number_accumulator = 0
                else:
                    length += 1

        length += number_accumulator
        return length

    def get_chess_pieces_in_row(
        self,
        row: str,
        row_number: int,
        storage: PieceStorage,
    ) -> list[ChessPiece]:
        """Возвращает список шахматных фигур, разбирая указанную строку

        Args:
            row (str): шахматная строка для парсинга
            row_number (int): номер шахматной строки
            storage (PieceStorage): хранилище шахматных фигур

        Returns:
            list[ChessPiece]: список шахм. фигур
        """
        pieces: list[ChessPiece] = []
        length = 0
        number_accumulator = 0
        symbols = list(row)

        for symbol in symbols:
            if symbol.isdigit():
                number_accumulator = number_accumulator * 10 + int(symbol)
            else:
                if number_accumulator != 0:
                    length += number_accumulator + 1
                    number_accumulator = 0
                else:
                    length += 1

                piece = storage.get_piece(symbol.upper())(
                    Position(
                        position=Vector2(
                            vertical=row_number, horizontal=length
                        ),
                    ),
                )
                pieces.append(piece)

        return pieces
