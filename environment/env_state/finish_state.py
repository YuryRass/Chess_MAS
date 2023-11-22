from data.board import Board
from environment.env_state.env_state import EnvState
from environment.env_state.state_enum import EnvStateType


class FinishEnvState(EnvState):
    """Конечное ссотояние системы"""
    def __init__(self, board: Board, epoch_number: int):
        """
        Args:
            board (Board): шахм. доска
            epoch_number (int): кол-во переговорных эпох,
        за которые удалось достичь финального состояния
        """
        super().__init__(EnvStateType.FINISH)
        self._board = board
        self._epoch_number = epoch_number

    @property
    def board(self) -> Board:
        return self._board

    @property
    def epoch_number(self) -> int:
        return self._epoch_number
