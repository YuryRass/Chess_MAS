"""
    Хранит значения номера ячейки по вертикали и горизонтали
"""
from typing import Self


class Vector2:
    """Двумерный вектор, описывающий координаты на шахм. доске"""

    def __init__(self, vertical: int, horizontal: int) -> None:
        """Инициализация вектора
        Args:
            vertical (int): вертикаль
            horizontal (int): горизонталь
        """
        self.vertical = vertical
        self.horizontal = horizontal

    def __str__(self) -> str:
        """Вывод вектора с координатами

        Returns:
            str: координаты вектора
        """
        return f'Vector2({self.vertical}, {self.horizontal})'

    def __add__(self, other: Self) -> Self:
        """Сумма двух векторов

        Args:
            other (Self): второй вектор

        Returns:
            Self: новый вектор
        """
        return Vector2(
            self.vertical + other.vertical,
            self.horizontal + other.horizontal
        )

    def __eq__(self, other: Self) -> bool:
        """Проверка векторов на равенство

        Args:
            other (Self): второй вектор

        Returns:
            bool: True, если вектора равны
        """
        return self.vertical == other.vertical and \
            self.horizontal == other.horizontal

    def __hash__(self) -> int:
        """Возвращает хеш кортежа, который представляет вектор

        Returns:
            int: хеш
        """
        return hash((self.vertical, self.horizontal))

    def copy(self) -> Self:
        """Копия вектора

        Returns:
            Self: объект класса Vector2
        """
        return Vector2(self.vertical, self.horizontal)
