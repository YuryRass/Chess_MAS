"""Визуализация в консоле шахматной доски"""
from data.board import Board


def board_visualizer(board: Board) -> str:
    """Визуализация шахм. доски с фигурами

    Args:
        board (Board): объект класса Доски

    Returns:
        str: строковая визуализация шахм. доски
    """
    string_board: list[list[str]] = []
    for row in range(board.size.vertical):
        string_board.append(["[-]"] * board.size.horizontal)

    for piece in board.pieces:
        position = piece.position.position
        string_board[position.vertical - 1][position.horizontal - 1] = \
            f'[{piece.name}]'

    # string_board.reverse()
    return "\n".join([" ".join(row) for row in string_board])
