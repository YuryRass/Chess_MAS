"""
    Реализация абстрактного класса, используемого для
    представления и парсинга шахматной доски
"""
from abc import ABC, abstractmethod

from data.board import Board
from utils.piece_storage import PieceStorage


class NotationParser(ABC):

    @abstractmethod
    def parse(self, fen_str: str, storage: PieceStorage) -> Board:
        ...

    @abstractmethod
    def serialize(self, board: Board) -> str:
        ...
